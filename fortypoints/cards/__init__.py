class Card(object):
	def __init__ (self, num, suit):
		self.num = num
		self.suit = suit
		if num == 5:
			self.points = 5
		elif num == 10 or num == KING:
			self.points = 10
		else:
			self.points = 0