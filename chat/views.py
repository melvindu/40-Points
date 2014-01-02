import simplejson as json

from flask import Blueprint, get_template_attribute
from flask.ext.login import current_user

from fortypoints.games.views import game
from fortypoints.players.decorators import player_required
from fortypoints.request import websocket

chat = Blueprint('chats', __name__)


@websocket(chat, '/game/<int:game_id>')
#@player_required
def game_chat_handler(ws, game_id):
  while True:
    message = ws.receive()
    if message is None:
      print 'None message, closing socket'
      break
    else:
      message = json.loads(message)
      render_chat = get_template_attribute('games/macros.html', 'render_chat')
      ws.send(render_chat(message['user'], message['message']))