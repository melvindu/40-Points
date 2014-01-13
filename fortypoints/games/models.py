from collections import defaultdict
import random
import fortypoints as fp

from fortypoints.cards import Card, constants as CARD, GameCard
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME
from fortypoints.games.exceptions import GameError
from fortypoints.players import get_player, get_player_by_id

db = fp.db

class Game(db.Model, ModelMixin):
  __tablename__ = 'game'
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  trump_number = db.Column(db.SmallInteger(unsigned=True), nullable=False)
  trump_suit = db.Column(db.SmallInteger(unsigned=True), nullable=True)
  size = db.Column(db.SmallInteger(unsigned=True))
  first = db.Column(db.Boolean, nullable=False, default=False)
  _state = db.Column('state', db.SmallInteger(unsigned=True), nullable=False)
  next_game_id = db.Column(db.Integer(unsigned=True), db.ForeignKey(id), index=True)

  next_game = db.relationship('Game', 
                              uselist=False, 
                              remote_side=[id], 
                              backref=db.backref('previous_game', uselist=False))

  def __init__(self, num_players, level, first=False):
    self.size = num_players
    self.trump_number = level
    self.first = first
    self.state = GAME.DRAWING

  @property
  def name(self):
    return 'Game #{game_id}'.format(game_id=self.id)

  @property
  def state(self):
    return self._state

  @state.setter
  def state(self, game_state):
    if game_state not in GAME.STATES:
      raise GameError('Unknown game state {0}'.format(game_state))
    self._state = game_state

  @property
  def trump(self):
    return Card(self.trump_number, self.trump_suit)

  @trump.setter
  def trump(self, card):
    self.trump_number = card.num
    self.trump_suit = card.suit

  @property
  def trump_letters(self):
    if self.trump_suit is None:
      return ''
    if self.trump_number == CARD.SMALL_JOKER:
      return 'SJ'
    elif self.trump_number == CARD.BIG_JOKER:
      return 'BJ'
    else:
      return '{0}{1}'.format(CARD.NUMBER[self.trump_number], 
                             CARD.SUIT[self.trump_suit]).upper()

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
  def house_lead(self):
    lead = filter(lambda p: p.lead, self.players)
    return lead[0] if lead else None

  @house_lead.setter
  def house_lead(self, player):
    for other_player in self.players:
      other_player.lead = False
    player.lead = True

  def get_player(self, user):
    return get_player(self, user)

  @property
  def round(self):
    if not len(self.plays):
      return 1
    current_round = max([play.round for play in self.plays])
    plays = filter(lambda p: p.round == current_round, self.plays)
    if len(plays) == len(self.players):
      return current_round + 1
    return current_round

  @property
  def round_plays(self):
    plays = filter(lambda p: p.round == self.round, self.plays)
    return sorted(plays, key=lambda p: p.number)

  @property
  def round_suit(self):
    if not self.round_plays:
      return None
    return self.round_plays[0].cards[0].suit

  @property
  def deck(self):
    return self.cards

  @property
  def undealt_cards(self):
    return filter(lambda c: c.player_id is None, self.deck)

  @property
  def hand_cards(self):
    cards = []
    for player in self.players:
      cards.extend(player.hand)
    return cards

  @property
  def flipped_cards(self):
    return filter(lambda c: c.flipped, self.deck)

  @property
  def bottom_size(self):
    num_players = len(list(self.players))
    num_left = len(list(self.deck)) % num_players
    return num_left % num_players + num_players

  def deal(self, player):
    card = random.choice(self.undealt_cards)
    card.player_id = player.id
    return card

  def to_dict(self):
    return {
      'id': self.id,
      'trump_number': self.trump_number,
      'trump_suit': self.trump_suit,
      'trump_letters': self.trump_letters,
      'size': self.size,
      'first': self.first,
      'state': self.state,
      'next_game_id': self.next_game_id
    }

  def __repr__(self):
    return '<Game size={size} trump_number={num} trump_suit={suit}>'.format(
            size=self.size, 
            num=self.trump_number,
            suit=self.trump_suit
    )