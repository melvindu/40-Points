from functools import wraps
import logging

from flask import g, jsonify, redirect, request, url_for
from flask.ext.login import current_user, login_required

from fortypoints.cards.decorators import get_cards_from_form
from fortypoints.cards.exceptions import CardError
from fortypoints.games import get_game
from fortypoints.games.exceptions import GameError
from fortypoints.games.updates import update_game_client
from fortypoints.players import get_player, get_player_by_id

def game_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not current_user:
      return login_required(func)(*args, **kwargs)
    player_id = kwargs.get('player_id')
    game_id = kwargs.get('game_id')
    if player_id:
      player = get_player_by_id(player_id)
      game = player.game
    elif game_id:
      game = get_game(game_id)
    player = get_player(game, current_user)
    if player:
      return login_required(func)(*args, **kwargs)
    else:
      return redirect(url_for('index'))
  return wrapper

def game_response(updates):
  def wrapper(func):
    @wraps(func)
    def decorator(*args, **kwargs):
      player_id = kwargs.get('player_id')
      game_id = kwargs.get('game_id')
      if player_id:
        player = get_player_by_id(player_id)
        game = player.game
      elif game_id:
        game = get_game(game_id)
      try:
        result = func(*args, **kwargs)
        for update in updates:
          update_game_client(game.id, update, result)
        return jsonify({'status': True, 'data': result})
      except (GameError, CardError) as e:
        logging.exception(e)
        return jsonify({'status': False, 'data': e.message})
      except Exception as e:
        logging.exception(e)
        return jsonify({'status': False, 'error': True})
    return decorator
  return wrapper

def requires(*requirements):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      if not current_user:
        return login_required(func)(*args, **kwargs)
      player_id = kwargs.get('player_id')
      game_id = kwargs.get('game_id')

      #prioritize player id
      if player_id:
        req_player = get_player_by_id(player_id)
        game = player.game
      elif game_id:
        game = get_game(game_id)
      
      curr_player = get_player(game, current_user)

      if 'game' in requirements:
        if not curr_player:
          return redirect(url_for('index'))

      if 'player' in requirements:
        if req_player.user.id != current_user.id:
          return redirect(url_for('index'))

      if 'cards' in requirements:
        cards = get_cards_from_form(request.form)
        curr_player.get_cards(cards)

      if 'active' in requirements:
        if not curr_player.active:
          raise GameError('You are not the currently active player')

      if 'lead' in requirements:
        if not curr_player.lead:
          raise GameError('You are not the game lead.')

      if 'house' in requirements:
        if not curr_player.house:
          raise GameError('You are not on the house team.')

      return login_required(func)(*args, **kwargs)
    return wrapper
  return decorator
