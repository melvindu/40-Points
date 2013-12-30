class Suit(object):
	HEART = 1
	SPADE = 2
	CLUB = 3
	DIAMOND = 4

class Number(object):
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	SIX = 6
	SEVEN = 7
	EIGHT = 8
	NINE = 9
	TEN = 10
	JACK = 11
	QUEEN = 12
	KING = 13
	ACE = 14
	SMALL_JOKER = 15
	BIG_JOKER = 16

NUM_SUITS = 4
NUM_NUMBERS = 15

NUMBERS = (Number.TWO, Number.THREE, Number.FOUR, Number.FIVE, Number.SIX, 
	Number.SEVEN, Number.EIGHT, Number.NINE, Number.TEN, Number.JACK, 
	Number.QUEEN, Number.KING, Number.ACE, Number.SMALL_JOKER, Number.BIG_JOKER)

SUITS = (Suit.HEART, Suit.SPADE, Suit.CLUB, Suit.DIAMOND)