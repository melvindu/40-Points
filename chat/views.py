import simplejson as json

from flask import Blueprint

from fortypoints.games.views import game
from fortypoints.players.decorators import player_required
from fortypoints.request import websocket

chat = Blueprint('chats', __name__)


@websocket(chat, '/game/<int:game_id>')
#@player_required
def game_chat_handler(ws, game_id):
  while True:
    message = ws.receive()
    print message
    if message is None:
      print 'broke'
      break
    else:
      #message = json.loads(message)

      r  = "I have received this message from you : %s" % message
      r += "<br>Glad to be your webserver."
      print 'sending'
      ws.send(json.dumps({'output': r}))
      print 'sent'