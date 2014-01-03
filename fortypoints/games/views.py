import simplejson as json
from collections import defaultdict

from flask import Blueprint, flash, get_template_attribute, redirect, render_template, request, url_for
from flask_login import current_user, login_required

import fortypoints as fp
from fortypoints.template import templated
from fortypoints.cards import Flip
from fortypoints.cards.exceptions import FlipError
from fortypoints.games import create_game, get_game, constants as GAME
from fortypoints.games.forms import NewGameForm
from fortypoints.games.updates import update_game_client
from fortypoints.request import WebSocketManager, websocket
from fortypoints.players import get_player
from fortypoints.players.decorators import player_required
from fortypoints.users import get_user

game = Blueprint('games', __name__, template_folder='templates/games')

db = fp.db

@game.route('/play/<int:game_id>')
@player_required
def play(game_id):
  """
  Play a game.
  """
  players = get_game(game_id).players
  return render_template('games/play.html', game_id=game_id, players=players)


@game.route('/new', methods=['GET', 'POST'])
@login_required
def new():
  """
  New Game Form.
  """
  form = NewGameForm(request.form)
  # make sure data are valid, but doesn't validate password is right
  if form.validate_on_submit():
    if form.add_player.data:
      form.players.append_entry()
      return render_template('games/new.html', form=form)
    else:
      usernames = [field.data for field in form.players.entries] + [current_user.name]
      users = set()
      for username in usernames:
        user = get_user(name=username)
        if not user:
          flash('Invalid User {username}'.format(username=username), 'danger')
          return render_template('games/new.html', form=form)
        users.add(user)
      users = list(users)

      if len(users) < GAME.MIN_PLAYERS:
        flash('Must invite at least {min} players'.format(min=GAME.MIN_PLAYERS), 'danger')
        return render_template('games/new.html', form=form)
      game = create_game(users, level=2, first=True)
      return redirect(url_for('games.play', game_id=game.id))
  return render_template('games/new.html', form=form)


@game.route('/draw-card/<int:game_id>', methods=['POST'])
@player_required
def draw_card(game_id):
  game = get_game(game_id)
  player = get_player(game, current_user)
  if player.active:
    card = player.draw()
    player.next_player.active = True
    if game.undealt_cards == game.bottom_size:
      if game.flipped_cards:
        game.house_lead.active = True
        while game.undealt_cards:
          game.house_lead.draw()
    db.session.commit()

  update_game_client(game_id, 'hand:update', {})


@game.route('/flip-card/<int:game_id>', methods=['POST'])
@player_required
def flip_card(game_id):
  game = get_game(game_id)
  player = get_player(game, current_user)
  cards = request.form['cards']
  to_flip_cards = []
  for card in cards:
    for player_card in player.cards:
      if card['num'] == player_card.num and card['suit'] == player_card.suit:
        to_flip_cards.append(player_card)
        break
    raise ValueError('Player doesn\'t own requested card to flip')
  flipped_cards = lambda c: c.flipped, game.cards
  flipped = Flip(flipped_cards)
  to_flip = Flip(to_flip_cards)
  if to_flip > flipped:
    for card in flipped_cards:
      card.flipped = False
    for card in to_flip_cards:
      card.flipped = True

    #set house if this is the first flip of all games
    if not game.house_players:
      player.house = True
      player.lead = True
    db.session.commit()
  else:
    raise ValueError('Can\'t flip weaker cards')


@game.route('/play-cards/<int:game_id>')
@player_required
def play_cards(game_id):
  players = get_game(game_id).players
  render_scores = get_template_attribute('games/macros.html', 'render_scores')
  update_game_client(game_id, 'scoreboard:update', render_scores(players))


@game.route('/update/<int:game_id>', methods=['GET', 'POST'])
@player_required
def update(game_id):
  updater = GameClientUpdater.factory(game_id)
  updater.update(json.dumps(dict(event='scoreboard:update')))


@websocket(game, '/update-stream/<int:game_id>')
def update_stream(ws, game_id):
  print game_id
  try:
    updater = GameClientUpdater.factory(game_id)
    updater.connect(ws)
    updater.listen()
    while ws.receive():
      print 'receiving'
  except Exception as e:
    print e