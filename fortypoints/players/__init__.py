import fortypoints as fp
from fortypoints.players.models import Player

db = fp.db

def create_player(game, user):
  player = Player(game, user)
  db.session.add(player)
  db.session.commit()