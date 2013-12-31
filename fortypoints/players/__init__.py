import fortypoints as fp
from fortypoints.players.models import Player

db = fp.db

def get_player(game, user):
  return Player.get(game_id=game.id, user_id=user.id)

def get_player_by_id(player_id):
  return Player.get(id=player_id)

def create_player(game, user):
  player = Player(game, user)
  db.session.add(player)
  db.session.commit()