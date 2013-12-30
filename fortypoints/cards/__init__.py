from fortypoints.cards.constants import Number
from fortypoints.cards.constants import Suit

class Card(object):
	def __init__ (self, num, suit):
		self.num = num
		self.suit = suit
		if num == FIVE:
			self.points = 5
		elif num == TEN or num == KING:
			self.points = 10
		else:
			self.points = 0

  @property
  def num(self):
    return self._num

  @num.setter
  def num(self, num):
    if num not in Number:
      raise ValueError('Card() value is invalid')
    self._num = num

  @property
  def suit(self):
  	return self._suit

  @suit.setter
  def suit(self, suit):
  	if suit not in Suit:
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
