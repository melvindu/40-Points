import random

from lib.cards import constants as CARD
from lib.cards.card import Card

class Deck(object):
	def __init__(self):
		deck = []
		for suit in CARD.SUITS:
			for num in CARD.NUMBERS:
				card = Card(suit, num)
				deck.append(card)
		for joker in CARD.JOKERS:
			deck.append(Card(joker, joker))
		self.cards = deck

	def shuffle(self):
		random.shuffle(self.cards)

	def sort(self):
		self.cards.sort()

	def pop(self):
		return self.cards.pop()