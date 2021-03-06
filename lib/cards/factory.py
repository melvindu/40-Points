from lib.cards import constants as CARD
from lib.cards.card import Card, Suit, Value
from lib.cards.exceptions import InvalidCardError, InvalidSuitError, InvalidValueError


class CardFactory(object):
  """
  Factory class for creating cards. The factory contains validations to ensure that cards generated by this class
  are valid cards and contain valid suits and values.
  """
  @classmethod
  def card(cls, suit, value):
    """
    Create a card object with validations.

    :param suit: The card suit.
    :type suit: int or None
    :param value: The card value.
    :type value: int
    :return: a :class:`lib.cards.card.Card`.
    """
    if value in CARD.JOKERS and suit is not None:
      raise InvalidCardError

    if suit is None and value not in CARD.JOKERS:
      raise InvalidCardError

    if suit not in CARD.SUITS + tuple(None):
      raise InvalidSuitError

    if value not in CARD.VALUES:
      raise InvalidValueError

    if suit is None:
      return Card(None, Value(value))
    else:
      return Card(Suit(suit), Value(value))

  @classmethod
  def big_joker(cls):
    """
    :return: a big joker :class:`lib.cards.card.Card`.
    """
    return cls.card(None, CARD.BIG_JOKER)

  @classmethod
  def small_joker(cls):
    """
    :return: a small joker :class:`lib.cards.card.Card`.
    """
    return cls.card(None, CARD.SMALL_JOKER)
