from lib.cards import constants as CARD
from lib.cards.exceptions import InvalidCardError

class Card(object):
    """
    Represents a normal Card. Holds a suit and a value.

    Joker cards have an equal suit/value of big or little joker.
    """
    def __init__(self, suit, value):
        # joker suit and value must be equal
        if (suit in CARD.JOKERS) or (value in CARD.JOKERS):
            if suit != value:
                raise InvalidCardError('Joker suit and value must be equal')

        self.suit = suit
        self.value = value