from collections import defaultdict
import simplejson as json

from flask import Blueprint, get_template_attribute
from flask.ext.login import current_user

from fortypoints.games.views import game
from fortypoints.players.decorators import player_required
from fortypoints.request import WebSocketManager, websocket

chat = Blueprint('chats', __name__)

game_chat_sockets = defaultdict(lambda: WebSocketManager(100))


def cleanup_sockets(max_size):
  size = sum([len(manager) for manager in game_chat_sockets.values()], 0)
  if size > max_size:
    for manager in game_chat_sockets.values():
      manager.clean()


@websocket(chat, '/game/<int:game_id>')
#@player_required
def game_chat_handler(ws, game_id):
  websocket_manager = game_chat_sockets[game_id]
  websocket_manager.clean()
  websocket_manager.add_socket(ws)
  cleanup_sockets(10000)
  while True:
    message = ws.receive()
    print message
    if message is None:
      print 'None message, closing socket'
      game_chat_sockets[game_id].remove(ws)
      break
    else:
      try:
        message = json.loads(message)
        render_chat = get_template_attribute('games/macros.html', 'render_chat')
        websocket_manager.broadcast(render_chat(message['user'], message['message']))
      except Exception as e:
        print e