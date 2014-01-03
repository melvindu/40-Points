from multiprocessing import Pool, Process, Queue

from flask import make_response, request
from functools import update_wrapper, wraps

def nocache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)

def flask_context(app):
  def wrapper(func):
    def decorator(*args, **kwargs):
      with app.app_context():
        with app.request_context(request.environ):
          return func(*args, **kwargs)
    return decorator
  return wrapper

def websocket(blueprint, *args, **kwargs):
  def wrapper(func):
    @blueprint.route(*args, **kwargs)
    @wraps(func)
    def decorator(*args, **kwargs):
      ws = request.environ['wsgi.websocket']
      return func(ws, *args, **kwargs)
    return decorator
  return wrapper


class WebSocketManager(object):
  def __init__(self, max_size):
    self._max_size = max_size
    self._sockets = []

  @property
  def sockets(self):
    return self._sockets

  def add_socket(self, socket):
    if len(self.sockets) > self._max_size:
      self.clean()
    self._sockets.append(socket)

  def clean(self):
    sockets = []
    for socket in self.sockets:
      if not socket.closed:
        sockets.append(socket)
    self._sockets = sockets

  def broadcast(self, message):
    for socket in self.sockets:
      socket.send(message)

  def __len__(self):
    return len(self._sockets)

  def __iter__(self):
    return iter(self._sockets)

  def __nonzero__(self):
    return bool(self._sockets)


class WebSocketUpdater(object):
  def __init__(self, workers=25):
    self._websocket_manager = WebSocketManager(100)
    self._update_stream = Queue()

  def connect(self, ws):
    self._websocket_manager.add_socket(ws)

  def listen(self):
    def _listen(updater):
      while True:
        update = updater._update_stream.get()
        updater._websocket_manager.broadcast(update)
        if not updater._websocket_manager:
          break
    Process(target=_listen, args=(self, )).start()

  def clean(self):
    self._websocket_manager.clean()

  def update(self, message):
    self._update_stream.put(message)

