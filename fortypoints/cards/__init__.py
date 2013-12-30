from random import shuffle
from fortypoints.cards.constants import NUMBERS, SUITS, Number, Suit

class Deck(object):
	def __init__(self):
		deck = []
		for suit in SUITS:
			for num in NUMBERS:
				card = Card(num, suit)
				deck.append(card)
		self.cards = deck

	def shuffle(self):
		random.shuffle(self.cards)

class Card(object):
  def __init__(self, num, suit):
	  self.num = num
	  self.suit = suit

	def __eq__(self, other):
		if self.suit != other.suit:
			return False
		if self.num == other.num:
			return True
		else:
			return False

	def __lt__(self, other):
		if SUITS.index(self.suit) >= SUITS.index(other.suit):
			return False
		if self.num < other.num:
			return True
		else:
			return False

	def __gt__(self, other):
		if SUITS.index(self.suit) <= SUITS.index(other.suit):
			return False
		if self.num > other.num:
			return True
		else:
			return False

  @property
  def num(self):
    return self._num

  @num.setter
  def num(self, num):
    if num not in NUMBERS:
      raise ValueError('Card() value is invalid')
    self._num = num

  @property
  def suit(self):
    return self._suit

  @suit.setter
  def suit(self, suit):
    if suit not in SUITS:
      raise ValueError('Card() suit is invalid')
    self._suit = suit

  @property
  def points(self):
    if self.num == Number.FIVE:
      return 5
    elif self.num in (Number.TEN, Number.KING):
      return 10
    else:
      return 0
