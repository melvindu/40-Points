from functools import wraps

from flask import g, redirect, url_for
from flask.ext.login import current_user, login_required

from fortypoints.games import get_game
from fortypoints.players import get_player, get_player_by_id

def player_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not current_user:
      return login_required(func)(*args, **kwargs)

    player_id = kwargs.get('player_id')
    game_id = kwargs.get('game_id')
    if player_id:
      player = get_player_by_id(player_id)
      if player.user.id == current_user.id:
        return login_required(func)(*args, **kwargs)
      else:
        return redirect(url_for('index'))
    elif game_id:
      game = get_game(game_id)
      player = get_player(game, current_user)
      if player:
        return login_required(func)(*args, **kwargs)
      else:
        return redirect(url_for('index'))
    else:
      return redirect(url_for('index'))
  return wrapper

def player_required_ws(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    game_id = kwargs['game_id']
    game = get_game(game_id)
    if not g.user:
      return login_required(func)(*args, **kwargs)
    player = get_player(game, g.user)
    if player:
      return login_required(func)(*args, **kwargs)
    else:
      return redirect(url_for('index'))
  return wrapper
