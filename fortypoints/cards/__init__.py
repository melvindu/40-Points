import random

from fortypoints.cards import constants as CARD
from fortypoints.cards.models import CardMixin as Card


class Deck(object):
  def __init__(self, size=1):
    deck = []
    for index in range(size):
      for suit in CARD.SUITS:
        for num in CARD.NUMBERS:
          card = Card(num, suit)
          deck.append(card)
      for joker in CARD.JOKERS:
        deck.append(Card(joker, joker))
    self.cards = deck

  def shuffle(self):
    random.shuffle(self.cards)

  def sort(self):
    self.cards.sort()
