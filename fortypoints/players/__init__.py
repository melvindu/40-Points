from fortypoints.core import db
from fortypoints.players.models import Player


def get_player(game, user):
  return Player.get(game_id=game.id, user_id=user.id)

def get_player_by_id(player_id):
  return Player.get(id=player_id)

def create_player(game, user, number, active=False):
  player = Player(game, user, number, active)
  db.session.add(player)
  db.session.commit()