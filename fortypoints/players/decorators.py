from functools import wraps

from flask import redirect, url_for
from flask.ext.login import current_user, login_required

from fortypoints.games import get_game
fomr fortypoints.player import get_player

@login_required
def player_required(func)
  @wraps(func)
  def wrapper(*args, **kwargs):
    game_id = locals()['game_id']
    game = get_game(game_id)
    player = get_player(game, current_user)
    if player:
      return func(*args, **kwargs)
    else:
      return redirect(url_for('index'))