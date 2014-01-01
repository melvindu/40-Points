from flask import make_response, request
from functools import update_wrapper

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