from fortypoints.core import db
from fortypoints.players.models import Player


class Player(object):

  def __init__(self, level):
    """
    :param level: card level constant
    :return:
    """
    self.score = 0
    self.level = level
    self.house = False
    self.hand = Hand()

  def draw(self, deck):
    card = deck.deal()
    self.hand.add_card(card)

  def draw_all(self, deck):
    while deck:
      card = deck.deal()
      self.hand.add_card(card)

  def flip(self, cards):
    # TODO(mdu)
    pass

  def play(self, cards):
    # TODO(mdu)
    pass


class Hand(object):
  def __init__(self, cards=None):
    self._cards = cards or []

  @property
  def cards(self):
    return self._cards

  def add_card(self, card):
    self.cards.append(card)


def get_player(game, user):
  return Player.get(game_id=game.id, user_id=user.id)

def get_player_by_id(player_id):
  return Player.get(id=player_id)

def create_player(game, user, number, active=False):
  player = Player(game, user, number, active)
  db.session.add(player)
  db.session.commit()