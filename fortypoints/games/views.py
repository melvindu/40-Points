from collections import defaultdict

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from fortypoints.template import templated
from fortypoints.games import create_game, constants as GAME
from fortypoints.games.forms import NewGameForm
from fortypoints.games.updates import GameClientUpdater
from fortypoints.request import WebSocketManager, websocket
from fortypoints.players.decorators import player_required
from fortypoints.users import get_user

game = Blueprint('games', __name__, template_folder='templates/games')


@game.route('/play/<int:game_id>')
@player_required
def play(game_id):
  """
  Play a game.
  """
  return render_template('games/play.html', game_id=game_id)


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
      users = []
      for username in usernames:
        user = get_user(name=username)
        if not user:
          flash('Invalid User {username}'.format(username=username), 'danger')
          return render_template('games/new.html', form=form)
        users.append(user)

      if len(users) < GAME.MIN_PLAYERS:
        flash('Must invite at least {min} players'.format(min=GAME.MIN_PLAYERS), 'danger')
        return render_template('games/new.html', form=form)
      game = create_game(users)
      return redirect(url_for('games.play', game_id=game.id))
  return render_template('games/new.html', form=form)


@game.route('/update/<int:game_id>', methods=['POST'])
@player_required
def update(game_id):
  updater = GameClientUpdater.factory(game_id)
  updater.update(dict(request.form))


@websocket(game, '/update-stream/<int:game_id>')
def update_stream(ws, game_id):
  print game_id
  try:
    updater = GameClientUpdater.factory(game_id)
    print updater
    updater.connect(ws)
    updater._websocket_manager.broadcast('hello')
    updater.listen()
    while ws.receive():
      print 'receiving'
  except Exception as e:
    print e