from functools import wraps

from flask import redirect, url_for
from flask.ext.login import current_user, login_required

from fortypoints.games import get_game
from fortypoints.players import get_player

def player_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    game_id = kwargs['game_id']
    game = get_game(game_id)
    if not current_user:
      return login_required(func)(*args, **kwargs)
    player = get_player(game, current_user)
    if player:
      return login_required(func)(*args, **kwargs)
    else:
      return redirect(url_for('index'))
  return wrapper