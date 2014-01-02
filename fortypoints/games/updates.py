from multiprocessing import Queue
from weakref import WeakValueDictionary

from fortypoints.request import WebSocketUpdater


class GameClientUpdater(WebSocketUpdater):
  game_map = WeakValueDictionary()
  @classmethod
  def factory(cls, game_id):
    GameClientManager.clean_all()
    if game_id in cls.game_map:
      return cls.game_map[game_id]
    else:
      manager = GameClientManager()
      cls.game_map[game_id] = manager
      return cls.game_map[game_id]

  @classmethod
  def clean_all(cls):
    for game_client_manager in cls.game_map.values():
      game_client_manager.clean()