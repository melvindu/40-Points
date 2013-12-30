class Card:
	def __init__ (self, num, suit, trump):
		self.num = num
		self.suit = suit
		self.trump = trump
	def changeTrump (self):
		if self.trump == True:
			self.trump = False
		else:
			self.trump = True
