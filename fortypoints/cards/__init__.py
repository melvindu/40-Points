from random import randrange
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
		shuffled = []
		unshuffled = self
		for card in self:
			temp = unshuffled.pop()
			shuffled.insert(randrange(len[self]), temp)
		return shuffled

class Card(object):
  def __init__(self, num, suit):
	  self.num = num
	  self.suit = suit

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
