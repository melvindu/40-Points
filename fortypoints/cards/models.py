import random

from fortypoints.cards import constants as CARD
from fortypoints.cards.exceptions import CardError
from fortypoints.core import db
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME


class CardMixin(object):
  def __init__(self, num, suit):
    self._num = num
    self._suit = suit
    if self.num in CARD.JOKERS or self.suit in CARD.JOKERS:
      if self.num != self.suit:
        raise CardError('Card() joker initialization failed')

  @property
  def name(self):
    if self.num in (CARD.SMALL_JOKER, CARD.BIG_JOKER):
      return CARD.NUMBER[self.num].replace('_', ' ').title()
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

  @property
  def points(self):
    if self.num == CARD.FIVE:
      return 5
    elif self.num in (CARD.TEN, CARD.KING):
      return 10
    else:
      return 0

  def __repr__(self):
    return '<Card \'{name}\'>'.format(name=self.name)

  def __eq__(self, other):
    return self.suit == other.suit and self.num == other.num

  def __lt__(self, other):
    if self.suit > other.suit:
      return False
    elif self.suit < other.suit:
      return True
    if self.num < other.num:
      return True
    else:
      return False

  def __gt__(self, other):
    if self.suit < other.suit:
      return False
    elif self.suit > other.suit:
      return True
    if self.num > other.num:
      return True
    else:
      return False


class Card(db.Model, ModelMixin, CardMixin):
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  game_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('game.id'), nullable=True, index=True)
  player_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('player.id'), nullable=True, index=True)
  play_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('play.id'), nullable=True, index=True)
  _num = db.Column('num', db.Integer(unsigned=True), nullable=False)
  _suit = db.Column('suit', db.Integer(unsigned=True), nullable=False)
  bottom = db.Column(db.Boolean(), default=False)
  flipped = db.Column(db.Boolean(), default=False)

  game = db.relationship('Game', foreign_keys=game_id, backref=db.backref('cards', lazy='dynamic'))
  player = db.relationship('Player', backref=db.backref('cards', lazy='dynamic'))
  play = db.relationship('Play', backref=db.backref('cards', lazy='dynamics'))

  def __init__(self, num, suit):
    CardMixin.__init__(self, num, suit)

  def to_dict(self):
    return {
      'num': self.num,
      'suit': self.suit,
      'points': self.points,
      'bottom': self.bottom,
      'flipped': self.flipped
    }