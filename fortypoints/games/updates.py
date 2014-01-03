import simplejson as json

from multiprocessing import Queue
from weakref import WeakValueDictionary

from fortypoints.request import WebSocketUpdater


def update_game_client(game_id, event, update):
  message = {
    'event': event,
    'data': update
  }
  GameClientUpdater.factory(game_id).update(json.dumps(message))

class GameClientUpdater(WebSocketUpdater):
  game_map = WeakValueDictionary()
  @classmethod
  def factory(cls, game_id):
    if game_id in cls.game_map:
      return cls.game_map[game_id]
    else:
      manager = GameClientUpdater()
      cls.game_map[game_id] = manager
      return cls.game_map[game_id]

  @classmethod
  def clean_all(cls):
    for game_client_manager in cls.game_map.values():
      game_client_manager.clean()