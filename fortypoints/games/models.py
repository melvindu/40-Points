import fortypoints as fp

from fortypoints.cards import Card
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME
from fortypoints.players import get_player, get_player_by_id

db = fp.db

class Game(db.Model, ModelMixin):
  __tablename__ = 'game'
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  trump_number = db.Column(db.SmallInteger(unsigned=True), nullable=True)
  trump_suit = db.Column(db.SmallInteger(unsigned=True), nullable=True)
  size = db.Column(db.SmallInteger(unsigned=True))
  current_player_id = db.Column(db.Integer(unsigned=True), 
                                db.ForeignKey('player.id', 
                                              use_alter=True, 
                                              name='current_player_id'), 
                                nullable=True)

  def __init__(self, num_players):
    self.size = num_players

  @property
  def trump(self):
    return Card(self.trump_number, self.trump_suit)

  @trump.setter
  def trump(self, card):
    self.trump_number = card.num
    self.trump_suit = card.suit

  @property
  def current_player(self):
    return get_player_by_id(self.current_player_id)

  @current_player.setter
  def current_player(self, player):
    self.current_player_id = player.id

  def get_player(self, user):
    return get_player(self, user)

  def __repr__(self):
    return '<Game size={size} trump_number={num} trump_suit={suit}>'.format(
            size=self.size, 
            num=self.trump_number,
            suit=self.trump_suit
    )