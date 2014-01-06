from functools import wraps

from flask import request
from flask_login import current_user

from fortypoints.cards.models import CardMixin
from fortypoints.games import get_game
from fortypoints.players import get_player


def get_cards_from_form(form):
  def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
  cards = chunks(form.values(), 2)
  return [CardMixin(int(num), int(suit)) for (num, suit) in cards]


def cards_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    player_id = kwargs.get('player_id')
    game_id = kwargs.get('game_id')
    if player_id:
      player = get_player_by_id(player_id)
      game = player.game
    elif game_id:
      game = get_game(game_id)
    player = get_player(game, current_user)

    cards = get_cards_from_form(request.form)
    player.get_cards(cards)
    return func(*args, **kwargs)
  return wrapper
