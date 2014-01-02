from collections import defaultdict
import simplejson as json

from flask import Blueprint, get_template_attribute
from flask.ext.login import current_user

from fortypoints.games.views import game
from fortypoints.players.decorators import player_required
from fortypoints.request import websocket

chat = Blueprint('chats', __name__)

game_chat_sockets = defaultdict(list)

@websocket(chat, '/game/<int:game_id>')
#@player_required
def game_chat_handler(ws, game_id):
  game_chat_sockets[game_id].append(ws)
  while True:
    message = ws.receive()
    if message is None:
      print 'None message, closing socket'
      game_chat_sockets[game_id].remove(ws)
      break
    else:
      message = json.loads(message)
      render_chat = get_template_attribute('games/macros.html', 'render_chat')
      for socket in game_chat_sockets[game_id]:
        socket.send(render_chat(message['user'], message['message']))