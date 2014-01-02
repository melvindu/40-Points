from multiprocessing import Queue
from weakref import WeakValueDictionary

from fortypoints.request import WebSocketManager


class GameClientManager(object):
  game_map = WeakValueDictionary()
  @classmethod
  def factory(cls, game_id):
    cls.clean()
    if game_id in game_map:
      return game_map[game_id]
    else:
      game_map[game_id] = GameClientManager()
      return game_map[game_id]

  @classmethod
  def clean(cls):
    for game_client_manager in game_map.values():
      game_client_manager.clean()

  def __init__(self):
    self._websocket_manager = WebSocketManager(100)
    self._update_stream = GameUpdateStream()

  def connect(self, ws):
    self._websocket_manager.add_socket(ws)

  def listen(self):
    while True:
      update = self._update_stream.get()
      self._websocket_manager.broadcast(update)

  def clean(self):
    self._websocket_manager.clean()

  def update(message):
    self._update_stream.put(message)


class GameUpdateStream(object):
  def __init__(self):
    self._stream = Queue()

update_queue = Queue()