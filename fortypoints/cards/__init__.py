import random

import fortypoints as fp
from fortypoints.cards import constants as CARD
from fortypoints.cards.models import Card as CardModel, CardMixin as Card

db = fp.db


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

  def __iter__(self):
    return iter(self.cards)


def create_deck(size=1, game_id=None):
  deck = Deck(size)
  deck.shuffle()
  cards = []
  for card in deck:
    print card
    card_model = CardModel(card.num, card.suit)
    print card_model
    if game_id:
      card_model.game_id = game_id
    cards.append(card_model)
  db.session.add_all(cards)
  fp.db.session.commit()
  return cards
