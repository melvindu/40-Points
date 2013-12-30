import fortypoints as fp

from fortypoints.cards import Card
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME

db = fp.db

class Game(db.Model, ModelMixin):
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  trump_number = db.Column(db.SmallInteger(unsigned=True), nullable=True)
  trump_suit = db.Column(db.SmallInteger(unsigned=True), nullable=True)
  size = db.Column(db.SmallInteger(unsigned=True))
  
  def __init__(self, num_players):
    self.size = num_players

  @property
  def trump(self):
    return Card(self.trump_number, self.trump_suit)

  @trump.setter
  def trump(self, card):
    self.trump_number = card.num
    self.trump_suit = card.suit

  def __repr__(self):
    return '<Game size={size} trump={trump}>'.format(size=self.size, trump=self.trump)