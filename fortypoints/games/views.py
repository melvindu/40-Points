from collections import defaultdict

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from fortypoints.template import templated
from fortypoints.games import create_game, constants as GAME
from fortypoints.games.forms import NewGameForm
from fortypoints.games.updates import update_queue
from fortypoints.request import WebSocketManager, websocket
from fortypoints.players.decorators import player_required
from fortypoints.users import get_user

game = Blueprint('games', __name__, template_folder='templates/games')


_game_update_sockets = defaultdict(lambda: WebSocketManager(100))


def _cleanup_sockets(max_size):
  size = sum([len(manager) for manager in _game_update_sockets.values()], 0)
  if size > max_size:
    for manager in _game_update_sockets.values():
      manager.clean()


@game.route('/play/<int:game_id>')
@player_required
def play(game_id):
  """
  Play a game.
  """
  return render_template('games/play.html')


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


@websocket(game, '/game/update-stream/<int:game_id>')
def update_stream(ws, game_id):
  _game_update_sockets[game_id].append(ws)
  _cleanup_sockets(10000)
  while True:
    message = update_queue.get()
    if message is None:
      print 'None message, closing socket'
      _game_update_sockets[game_id].remove(ws)
      break
    else:
      message = json.loads(message)
      render_chat = get_template_attribute('games/macros.html', 'render_chat')
      for socket in _game_update_sockets[game_id]:
        socket.send(render_chat(message['user'], message['message']))
