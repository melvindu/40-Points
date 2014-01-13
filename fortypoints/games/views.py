import random
import simplejson as json
from collections import defaultdict

from flask import Blueprint, flash, get_template_attribute, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

import fortypoints as fp
from fortypoints.template import templated
from fortypoints.cards import Flip
from fortypoints.cards.decorators import cards_required, get_cards_from_form
from fortypoints.cards.exceptions import CardError, FlipError
from fortypoints.cards.models import CardMixin
from fortypoints.games import create_game, get_game, constants as GAME
from fortypoints.games.decorators import game_required, game_response, requires
from fortypoints.games.exceptions import GameError
from fortypoints.games.forms import NewGameForm
from fortypoints.games.updates import update_game_client, GameClientUpdater
from fortypoints.request import WebSocketManager, websocket
from fortypoints.players import get_player
from fortypoints.players.decorators import player_required
from fortypoints.users import get_user

game = Blueprint('games', __name__, template_folder='templates/games')

db = fp.db


@game.route('/<int:game_id>')
@game_required
def game_status(game_id):
  game = get_game(game_id)
  return jsonify(game.to_dict())


@game.route('/play/<int:game_id>')
@game_required
def play(game_id):
  """
  Play a game.
  """
  game = get_game(game_id)
  players = game.players
  others = []
  me = None
  # sort order others relative to me
  for player in players:
    if player.user_id == current_user.id:
      me = player
    else:
      if me:
        others.append(player)
  for player in players:
    if player.id == me.id:
      break
    else:
      others.append(player)
  return render_template('games/play.html', game=game, game_id=game_id, me=me, others=others, players=[me] + others)


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
@game_response(['game:update', 'player:update'])
@game_required
def draw_card(game_id):
  game = get_game(game_id)
  player = get_player(game, current_user)

  if player.active and game.undealt_cards:
    card = player.draw()
    player.next_player.active = True

    if len(game.undealt_cards) == game.bottom_size:
    # all cards are drawn
      if not game.house_lead:
        game.house_lead = random.choice(list(game.players))
      game.house_lead.active = True
      game.house_lead.draw_all()
      game.state = GAME.COVERING

    db.session.commit()
    return None
  else:
    if not game.undealt_cards:
      raise GameError('No cards to draw')
    else:
      raise GameError('It is not your turn to draw')


@game.route('/flip-card/<int:game_id>', methods=['POST'])
@game_response(['game:update', 'player:update'])
@cards_required
@game_required
def flip_card(game_id):
  game = get_game(game_id)
  player = get_player(game, current_user)
  if game.state != GAME.DRAWING:
    raise GameError('It is too late to flip')
  cards = get_cards_from_form(request.form)

  if not cards:
    raise GameError('No cards selected to flip')

  to_flip_cards = player.get_cards(cards)
  flipped_cards = filter(lambda c: c.flipped, game.cards)

  if to_flip_cards == flipped_cards:
    raise GameError('Card(s) already flipped.')

  if not flipped_cards:
    player.flip(to_flip_cards)
    db.session.commit()
    return {
      'alert': 'Flip Successful!'
    }

  flipped = Flip(game, flipped_cards)
  to_flip = Flip(game, to_flip_cards)
  if to_flip > flipped:
    player.flip(to_flip_cards)
    db.session.commit()

    alert_msg = '{player} flipped {num} {card}(s)'.format(
        player=player.user.name,
        num=len(to_flip_cards),
        card=to_flip_cards[0].name
    )
    update_game_client(game_id, 'alert', {'status': True, 'data': alert_msg})
    return {
      'alert': 'Flip Successful!'
    }
  else:
    raise GameError('Can\'t flip weaker cards')


@game.route('/play-cards/<int:game_id>', methods=['POST'])
@requires('game', 'cards', 'active')
def play_cards(game_id):
  game = get_game(game_id)
  if game.state != GAME.PLAYING:
    raise GameError('Game State is {state}, not {play}'.format(state=game.state, play=GAME.PLAYING))
  
  current_player = get_player(game, current_user)
  cards = get_cards_from_form(request.form)
  current_player.play(cards)
  db.session.commit()
  render_scores = get_template_attribute('games/macros.html', 'render_scores')
  update_game_client(game_id, 'scoreboard:update', render_scores(players))
  return {'alert': 'PLAY SUCCESS'}


@game.route('/cover-cards/<int:game_id>', methods=['POST'])
@game_response(['game:update', 'player:update'])
@requires('game', 'cards', 'lead', 'active')
def cover_cards(game_id):
  game = get_game(game_id)
  if game.state != GAME.COVERING:
    raise GameError('It is not time to cover.')
  current_player = get_player(game, current_user)
  cards = get_cards_from_form(request.form)

  if len(cards) != game.bottom_size:
    raise GameError('Must cover {num} cards'.format(num=game.bottom_size))

  for card in current_player.get_cards(cards):
    card.bottom = True
  game.state = GAME.PLAYING
  db.session.commit()
  return {'alert': 'Cover Successful!'}


@game.route('/update/<int:game_id>', methods=['GET', 'POST'])
@game_required
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