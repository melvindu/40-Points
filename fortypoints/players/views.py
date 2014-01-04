import simplejson as json
from collections import defaultdict

from flask import Blueprint, flash, get_template_attribute, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

import fortypoints as fp
from fortypoints.template import templated
from fortypoints.cards import Flip
from fortypoints.cards.exceptions import FlipError
from fortypoints.games import create_game, get_game, constants as games
from fortypoints.games.decorators import game_required
from fortypoints.games.forms import NewGameForm
from fortypoints.games.updates import update_game_client
from fortypoints.request import WebSocketManager, websocket
from fortypoints.players import get_player, get_player_by_id
from fortypoints.players.decorators import player_required
from fortypoints.users import get_user

player = Blueprint('players', __name__, template_folder='templates/players')

db = fp.db

@player.route('/<int:player_id>')
@game_required
def player_status(player_id):
  """
  Get player status
  """
  player = get_player_by_id(player_id)
  player_dict = player.to_dict()
  if player.user_id != current_user.id:
    del player_dict['cards']
  player_dict['cards'] = [{'num': '2', 'suit': 'D'}, {'num': '3', 'suit': 'C'}]
  return jsonify(player_dict)
