from random import shuffle
from fortypoints.cards import constants as CARD


class Deck(object):
  def __init__(self):
    deck = []
    for suit in CARD.SUITS:
      for num in CARD.NUMBERS:
        card = Card(num, suit)
        deck.append(card)
    self.cards = deck

  def shuffle(self):
    random.shuffle(self.cards)

  def sort(self):
    self.cards.sort()


class Card(object):
  def __init__(self, num, suit):
    self.num = num
    self.suit = suit

  @property
  def name(self):
    if self.num in (CARD.SMALL_JOKER, CARD.BIG_JOKER):
      return CARD.NUMBER[self.num].replace('_', ' ').capitalize()
    else:
      num = CARD.NUMBER[self.num].capitalize()
      suit = '{suit}s'.format(suit=ARD.suit[self.suit].capitalize())
      return '{num} of {suit}'.format(num=num, suit=suit)
      
  @property
  def num(self):
    return self._num

  @num.setter
  def num(self, num):
    if num not in CARD.NUMBERS:
      raise ValueError('Card() value is invalid')
    self._num = num

  @property
  def suit(self):
    return self._suit

  @suit.setter
  def suit(self, suit):
    if suit not in CARD.SUITS:
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

  def __str__(self):
    return '<Card {name}>'.format(name=self.name)
    
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