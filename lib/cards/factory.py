from lib.cards.card import Card
from lib.cards import constants as CARD

class CardFactory(object):
  @classmethod
  def card(cls, suit, value):
    return Card(suit, value)

  @classmethod
  def big_joker(cls):
    return Card(CARD.BIG_JOKER, CARD.BIG_JOKER)

  @classmethod
  def small_joker(cls):
    return Card(CARD.SMALL_JOKER, CARD.SMALL_JOKER)