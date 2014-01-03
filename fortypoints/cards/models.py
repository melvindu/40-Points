import random

import fortypoints as fp
from fortypoints.cards import Card
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME

db = fp.db


class Card(db.Model, ModelMixin, Card):
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  player_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('player.id'))
  _num = db.Column(db.Integer(unsigned=True), nullable=False)
  _suit = db.Column(db.Integer(unsigned=True), nullable=False)

  player = db.relationship('Player', backref=db.backref('cards', lazy='dynamic'))

  def __init__(self, player, num, suit):
    self.player_id = player.id
    Card.__init__(num, suit)