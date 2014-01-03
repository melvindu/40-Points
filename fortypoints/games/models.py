import random
import fortypoints as fp

from fortypoints.cards import Card
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME
from fortypoints.players import get_player, get_player_by_id

db = fp.db

class Game(db.Model, ModelMixin):
  __tablename__ = 'game'
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  trump_number = db.Column(db.SmallInteger(unsigned=True), nullable=False)
  trump_suit = db.Column(db.SmallInteger(unsigned=True), nullable=True)
  size = db.Column(db.SmallInteger(unsigned=True))
  first = db.Column(db.Boolean, nullable=False, default=False)

  def __init__(self, num_players, level, first=False):
    self.size = num_players
    self.trump_number = level
    self.first = first

  @property
  def trump(self):
    return Card(self.trump_number, self.trump_suit)

  @trump.setter
  def trump(self, card):
    self.trump_number = card.num
    self.trump_suit = card.suit

  @property
  def current_player(self):
    active = lambda p: p.active
    active_players = filter(active, self.players)
    return active_players[0] if active_players else None

  @current_player.setter
  def current_player(self, player):
    self.current_player_id = player.id

  @property
  def house_players(self):
    return filter(lambda p: p.house, self.players)

  @property
  def  house_lead(self):
    lead = filter(lambda p: p.lead, self.players)
    return lead[0] if lead else None

  def get_player(self, user):
    return get_player(self, user)

  @property
  def deck(self):
    return self.cards

  @property
  def undealt_cards(self):
    return filter(lambda c: c.player_id is None, self.deck)

  @property
  def flipped_cards(self):
    return filter(lambda c: c.flipped, self.deck)

  @property
  def round(self):
    return max([0]+ [play.round or 0 for play in self.plays])

  @property
  def bottom_size(self):
    num_left = len(self.deck) % len(self.player)
    return num_left % GAME.BOTTOM_MODULO + num_left

  def deal(self, player):
    card = random.choice(self.undealt_cards)
    card.player_id = player.id
    db.session.commit()
    return card

  def __repr__(self):
    return '<Game size={size} trump_number={num} trump_suit={suit}>'.format(
            size=self.size, 
            num=self.trump_number,
            suit=self.trump_suit
    )

class Play(db.Model, ModelMixin):
  __tablename__ = 'play'
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  round = db.Column(db.Integer(unsigned=True), nullable=False)
  game_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('game.id'), nullable=True)
  player_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('player.id'), nullable=True)

  game = db.relationship('Game', foreign_keys=game_id, backref=db.backref('plays', lazy='dynamic'))
  player = db.relationship('Player', backref=db.backref('plays', lazy='dynamic'))