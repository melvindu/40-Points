import fortypoints as fp

from fortypoints.cards import Card, constants as CARD, Flip
from fortypoints.cards.exceptions import CardError
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME
from fortypoints.games.models import Play

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
      raise CardError('Inactive player cannot draw.')

  def draw_all(self):
    while self.game.undealt_cards:
      self.draw()

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

    #modify game trumps
    self.game.trump_suit = card.suit

  def play(self, cards):
    if not self.game.round_plays:
      play = Play.Round(self.game, self, cards)
    else:
      # do play validation
      pass

  def get_cards(self, cards):
    my_cards = self.hand
    ret_cards = []
    for card in cards:
      for my_card in my_cards:
        if card.num == my_card.num and card.suit == my_card.suit:
          my_cards.remove(my_card)
          ret_cards.append(my_card)
          break
    if not len(ret_cards) == len(cards):
      raise CardError('Player doesn\'t own requested cards')
    return ret_cards

  @property
  def hand(self):
    return sorted(filter(lambda c: not c.bottom, self.cards))

  @property
  def active(self):
    return self._active

  @active.setter
  def active(self, status):
    if status:
      for player in self.game.players:
        player.active = False
    self._active = status

  @property
  def next_player(self):
    players = sorted(self.game.players, key=lambda p: p.number)
    next_players = filter(lambda p: p.number == self.number + 1, players)
    if not next_players:
      return players[0]
    else:
      return next_players[0]

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
      'cards': [card.to_dict() for card in self.hand]
    }

  def __str__(self):
    return '<Player \'{user}\' level={level} house={house} game_id={game_id}>'.format(
                      user=self.user.name, 
                      level=self.level,
                      house=self.house,
                      game_id=self.game_id
    )