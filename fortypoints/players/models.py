import fortypoints as fp

from fortypoints.cards import Card, constants as CARD, Flip
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME

db = fp.db

class Player(db.Model, ModelMixin):
  __tablename__ = 'player'
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  game_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('game.id'), index=True)
  user_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('user.id'), index=True)
  number = db.Column(db.Integer(unsigned=True), nullable=False)
  _active = db.Column('active', db.Boolean, nullable=False)
  score = db.Column(db.SmallInteger(unsigned=True), nullable=False)
  level = db.Column(db.SmallInteger(unsigned=True), nullable=False)
  house = db.Column(db.Boolean, nullable=False)
  lead = db.Column(db.Boolean, nullable=False, default=False)

  game = db.relationship('Game', foreign_keys=game_id, backref=db.backref('players', lazy='dynamic'))
  user = db.relationship('User', backref=db.backref('players', lazy='dynamic'))

  def __init__(self, game, user, number, active=False):
    self.game_id = game.id
    self.user_id = user.id
    self.number = number
    self._active = active
    self.score = 0
    self.level = CARD.TWO
    self.house = False

  def draw(self):
    if self.active:
      return self.game.deal(self)
    else:
      raise ValueError('Inactive player cannot draw.')

  def flip(self, cards):
    flip = Flip(self.game, cards)
    for card in self.game.cards:
      if card.flipped == True:
        card.flipped = False
    for card in cards:
      card.flipped = True

    #set house if this is the first flip of all games
    if not self.game.house_players:
      for player in self.game.players:
        player.lead = False
      self.house = True
      self.lead = True

  @property
  def active(self):
    return self._active

  @active.setter
  def active(self, status):
    self._active = status
    if status:
      for player in self.game.players:
        player.active = False

  @property
  def next_player(self):
    players = sorted(self.game.players, key=lambda p: p.number)
    next_players = filter(lambda p: p.number == self.number + 1, players)
    if not next_players:
      return players[0]
    else:
      return players[self.number + 1]

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.user.name,
      'game_id': self.game_id,
      'user_id': self.user_id,
      'number': self.number,
      'active': self.active,
      'score': self.score,
      'level': self.level,
      'house': self.house,
      'lead': self.lead,
      'cards': [card.to_dict() for card in self.cards]
    }

  def __str__(self):
    return '<Player \'{user}\' level={level} house={house} game_id={game_id}>'.format(
                      user=self.user.name, 
                      level=self.level,
                      house=self.house,
                      game_id=self.game_id
    )