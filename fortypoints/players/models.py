import fortypoints as fp

from fortypoints.cards import Card
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME

db = fp.db

class Player(db.Model, ModelMixin):
  __tablename__ = 'player'
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  game_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('game.id'))
  user_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('user.id'))
  level = db.Column(db.SmallInteger(unsigned=True), nullable=False)
  house = db.Column(db.Boolean, nullable=False)

  game = db.relationship('Game', backref=db.backref('players', lazy='dynamic'))
  user = db.relationship('User', backref=db.backref('players', lazy='dynamic'))

  def __init__(self, game, user):
    self.game_id = game.id
    self.user_id = user.id

  def __repr__(self):
    return '<Player size={size} trump={trump}>'.format(size=self.size, trump=self.trump)