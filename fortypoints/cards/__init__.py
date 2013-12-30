import random
from fortypoints.cards import constants as CARD


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


class Card(object):
  def __init__(self, num, suit):
    self.num = num
    self.suit = suit
    if self.num in CARD.JOKERS or self.suit in CARD.JOKERS:
      if self.num != self.suit:
        raise ValueError('Card() joker initialization failed')

  @property
  def name(self):
    if self.num in (CARD.SMALL_JOKER, CARD.BIG_JOKER):
      return CARD.NUMBER[self.num].replace('_', ' ').title()
    else:
      num = CARD.NUMBER[self.num]
      suit = '{suit}s'.format(suit=CARD.SUIT[self.suit])
      return '{num} of {suit}'.format(num=num, suit=suit).title()
      
  @property
  def num(self):
    return self._num

  @num.setter
  def num(self, num):
    if num not in (CARD.NUMBERS + CARD.JOKERS):
      raise ValueError('Card() value is invalid')
    self._num = num

  @property
  def suit(self):
    return self._suit

  @suit.setter
  def suit(self, suit):
    if suit not in (CARD.SUITS + CARD.JOKERS):
      raise ValueError('Card() suit is invalid')
    self._suit = suit

  @property
  def points(self):
    if self.num == CARD.FIVE:
      return 5
    elif self.num in (CARD.TEN, CARD.KING):
      return 10
    else:
      return 0

  def __repr__(self):
    return '<Card \'{name}\'>'.format(name=self.name)
    
  def __eq__(self, other):
    return self.suit == other.suit and self.num == other.num

  def __lt__(self, other):
    if self.suit > other.suit:
      return False
    elif self.suit < other.suit:
      return True
    if self.num < other.num:
      return True
    else:
      return False

  def __gt__(self, other):
    if self.suit < other.suit:
      return False
    elif self.suit > other.suit:
      return True
    if self.num > other.num:
      return True
    else:
      return False