import random

from fortypoints.cards import constants as CARD
from fortypoints.cards.exceptions import FlipError
from fortypoints.cards.models import Card as CardModel, CardMixin as Card
from fortypoints.core import db


class BaseCard(object):
  def __init__(self, num, suit):
    self.num = num
    self.suit = suit

  @property
  def name(self):
    if self.num == CARD.SMALL_JOKER:
      return 'Small Joker'
    elif self.name == CARD.BIG_JOKER:
      return 'Big Joker'
    else:
      num = CARD.NUMBER[self.num]
      suit = '{suit}s'.format(suit=CARD.SUIT[self.suit])
      return '{num} of {suit}'.format(num=num, suit=suit).title()

  @property
  def num(self):
    return self._num

  @num.setter
  def num(self, num):
    if num not in (CARD.NUMBERS + CARD.JOKERS):
      raise CardError('Card() value is invalid')
    self._num = num

  @property
  def suit(self):
    return self._suit

  @suit.setter
  def suit(self, suit):
    if suit not in (CARD.SUITS + CARD.JOKERS):
      raise CardError('Card() suit is invalid')
    self._suit = suit

  def __repr__(self):
    return '<BaseCard \'{name}\'>'.format(name=self.name)

  def __eq__(self, other):
    return type(self) == type(other) and self.suit == other.suit and self.num == other.num


class FortyPointsCard(BaseCard):
  def __init__(self, num, suit):
    super(FPCard, self).__init__(num, suit)

  @property
  def points(self):
    if self.num == CARD.FIVE:
      return 5
    elif self.num in (CARD.TEN, CARD.KING):
      return 10
    else:
      return 0

  def __repr__(self):
    return '<FPCard \'{name}\'>'.format(name=self.name)


class Flip(object):
  def __init__(self, game, cards):
    # check unflippable
    flippable_nums = (game.trump_number, CARD.SMALL_JOKER, CARD.BIG_JOKER)
    if not cards:
      raise FlipError('No cards to flip')
    if not all(card.num in flippable_nums for card in cards):
      raise FlipError('Can\'t flip non-level card')

    # check nonequal cards
    if len(cards) > 1:
      if len(set(cards)) > 1:
        raise FlipError('Can\'t flip nonequivalent cards')
    self.game = game
    self.cards = cards

  def __len__(self):
    return len(self.cards)

  def __eq__(self, other):
    return self.cards == other.cards

  def __lt__(self, other):
    return not (self == other) and len(self) < len(other)

  def __gt__(self, other):
    return not self == other and len(self) > len(other)


class GameCard(Card):
  def __init__(self, game, card):
    self.game = game
    Card.__init__(self, card.num, card.suit)

  @property
  def trump_number(self):
    return self.game.trump_number

  @property
  def trump_suit(self):
    return self.game.trump_number

  @property
  def is_trump(self):
    return self.num == self.trump_number or \
           self.suit == self.trump_suit or \
           self.num in CARD.JOKERS

  def same_game_suit(self, game_card):
    return game_card.is_trump if self.is_trump else game_card.suit == self.suit

  def __repr__(self):
    return '<GameCard \'{name}\'>'.format(name=self.name)

  def __eq__(self, other):
    return self.suit == other.suit and self.num == other.num

  def __lt__(self, other):
    if self.is_trump and other.is_trump:
      return self.num < other.num
    elif self.is_trump and not other.is_trump:
      return False
    elif not self.is_trump and other.is_trump:
      return True
    else:
      if self.game.plays:
        if self.suit == self.game.round_suit:
          return self.num < other.num
        else:
          return True
      else:
        return False

  def __gt__(self, other):
    if self.is_trump and other.is_trump:
      return self.num > other.num
    elif self.is_trump and not other.is_trump:
      return True
    elif not self.is_trump and other.is_trump:
      return False
    else:
      if self.game.plays:
        if self.suit == self.game.round_suit:
          return self.num > other.num
        else:
          return False
      else:
        return True


class CardGroup(object):
  def __init__(self, cards):
    self.cards = cards

  def add_card(self, card):
    self.cards.append(card)


class Deck(object):
  def __init__(self, size=1):
    deck = []
    for index in range(size):
      for suit in CARD.SUITS:
        for num in CARD.NUMBERS:
          card = Card(num, suit)
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

  def deal(self):
    return self.pop()

  def __iter__(self):
    return iter(self.cards)

  def __len__(self):
    return len(self.cards)

  def __nonzero__(self):
    return bool(self.cards)


def create_deck(size=1, game_id=None):
  deck = Deck(size)
  deck.shuffle()
  cards = []
  for card in deck:
    print card
    card_model = CardModel(card.num, card.suit)
    print card_model
    if game_id:
      card_model.game_id = game_id
    cards.append(card_model)
  db.session.add_all(cards)
  db.session.commit()
  return cards
