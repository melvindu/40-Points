import random

import fortypoints as fp
from fortypoints.cards import constants as CARD
from fortypoints.cards.models import Card as CardModel, CardMixin as Card

db = fp.db


class Flip(object):
  def __init__(self, game, cards):
    # check unflippable
    flippable_nums = (game.trump_number, CARD.SMALL_JOKER, CARD.BIG_JOKER)
    if not all(card.num in flippable_nums for card in cards):
      raise ValueError('Can\'t flip non-level card')
    # check nonequal cards
    if len(cards) > 1:
      if len(set(cards)) > 1:
        raise ValueError('Can\'t flip nonequivalent cards')
    self.game = game
    self.cards = cards

  def __eq__(self, other):
    self.cards == other.cards

  def __lt__(self, other):
    return not (self == other) and len(self) < len(other)

  def __gt__(self, other):
    return not self == other and len(self) > len(other)


class GameCard(Card):
  def __init__(self, game, card):
    self.game = game
    Card.__init__(card.num, card.suit)

  @property
  def trump_number(self):
    return self.game.trump_number

  @property
  def trump_suit(self):
    return self.game.trump_number

  @property
  def is_trump(self):
    return self.num == self.trump_number or \
           self.suit == self.trump_suit or \
           self.num in CARD.JOKERS

  def __repr__(self):
    return '<GameCard \'{name}\'>'.format(name=self.name)
    
  def __eq__(self, other):
    return self.suit == other.suit and self.num == other.num

  def __lt__(self, other):
    if self.is_trump and other.is_trump:
      return self.num < other.num
    elif self.is_trump and not other.is_trump:
      return False
    elif not self.is_trump and other.is_trump:
      return True
    else:
      return False

  def __gt__(self, other):
    if self.is_trump and other.is_trump:
      return self.num > other.num
    elif self.is_trump and not other.is_trump:
      return True
    elif not self.is_trump and other.is_trump:
      return False
    else:
      return False

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
