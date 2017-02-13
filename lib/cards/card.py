class Card(object):
  """
  Represents a basic Card. Holds a suit and a value.

  All cards should have a suit and value, with exception for jokers. Jokers have a value with no suit.
  :param `Suit` suit: the card suit.
  :param `Value` value: the card value.
  """
  def __init__(self, suit, value):
    self.suit = suit
    self.value = value


class Suit(object):
  """
  Represents a basic card suit.

  Suit values are stored as integers.
  Diamonds is represented by 0.
  Club is represented by 1.
  Heart is represented by 2.
  Spade is represented by 3.

  :param int suit: A suit value (0-3).
  """
  def __init__(self, suit):
    self.suit = suit


class Value(object):
  """
  Represents a basic card value.

  Two through ten are represented by their actual numerical values.
  A Jack is represented by 11.
  A Queen is represented by 12.
  A King is represented by 13.
  An Ace is represented by 14.
  A Small Joker is represented by 15.
  A Big Joker is represented by 16.
  """
  def __init__(self, value):
    self.value = value