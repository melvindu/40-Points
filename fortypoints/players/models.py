from collections import defaultdict

from fortypoints.cards import Card, constants as CARD, Flip, GameCard
from fortypoints.cards.exceptions import CardError
from fortypoints.core import db
from fortypoints.models import ModelMixin
from fortypoints.games import constants as GAME
from fortypoints.games.exceptions import GameError


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
      play = Play.Play(self.game, self, cards)
    for card in self.get_cards(cards):
      card.play_id = play.id

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
  def name(self):
    return self.user.name

  @property
  def hand(self):
    return sorted(filter(lambda c: not c.bottom and not c.play, self.cards))

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

  @property
  def current_play(self):
    plays = filter(lambda p: p.round == self.game.round, self.plays)
    if plays:
      return plays[0]

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'game_id': self.game_id,
      'user_id': self.user_id,
      'number': self.number,
      'active': self.active,
      'score': self.score,
      'level': self.level,
      'house': self.house,
      'lead': self.lead,
      'cards': [card.to_dict() for card in self.hand],
      'play': [card.to_dict() for card in self.current_play.cards] if self.current_play else []
    }

  def __str__(self):
    return '<Player \'{user}\' level={level} house={house} game_id={game_id}>'.format(
                      user=self.user.name,
                      level=self.level,
                      house=self.house,
                      game_id=self.game_id
    )


class Play(db.Model, ModelMixin):
  __tablename__ = 'play'
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  round = db.Column(db.Integer(unsigned=True), nullable=False)
  number = db.Column(db.SmallInteger(unsigned=True), nullable=False)
  game_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('game.id'), nullable=True, index=True)
  player_id = db.Column(db.Integer(unsigned=True), db.ForeignKey('player.id'), nullable=True, index=True)

  game = db.relationship('Game', foreign_keys=game_id, backref=db.backref('plays', lazy='dynamic'))
  player = db.relationship('Player', backref=db.backref('plays', lazy='dynamic'))

  @classmethod
  def Play(cls, game, player, cards):
    plays = game.round_plays
    first_play = plays[0]
    if len(cards) != len(first_play.cards):
      raise GameError('Must play the same number of cards as the leading play')

    num_cards_in_suit = len([card for card in cards if \
                             GameCard(game, card).same_game_suit(GameCard(game, first_play.cards[0]))])

    for first_card in first_play.cards:
      first_game_card = GameCard(game, first_card)
      for card in cards:
        game_card = GameCard(game, card)
        if not first_game_card.same_game_suit(game_card):
          if num_cards_in_suit > len(first_play.cards):
            raise GameError('Must play cards of the same suit as the leading play')

    play_number = max([play.number for play in plays]) + 1
    play = cls(round=game.round, number=play_number, game_id=game.id, player_id=player.id)
    db.session.add(play)
    db.session.flush()
    return play

  @classmethod
  def Round(cls, game, player, cards):
    play = None
    if not cards:
      raise GameError('Can\'t create play without cards')

    game_cards = [GameCard(game, card) for card in cards]
    # make sure cards are all the same suit
    if not len(set([card.suit for card in cards])) == 1:
      if not all(game_card.is_trump for game_card in game_cards):
        raise GameError('Cannot start a round with cards in multiple suits')

    if not cls.numerically_linked(cards):
      raise GameError('Cards are not numerically linked')
    else:
      tuple_sizes = [len(tup) for tup in cls.tuples(cards)]
      diff_tuple_sizes = len(set(tuple_sizes))
      has_onetuple = any(tuple_size == 1 for tuple_size in tuple_sizes)
      if not diff_tuple_sizes == 1 or has_onetuple:
        if not cls.is_top_k(game, player, cards):
          raise GameError('Cards are not topK cards')


    play = cls(round=game.round, number=1, game_id=game.id, player_id=player.id)
    db.session.add(play)
    db.session.flush()
    return play

  @classmethod
  def numerically_linked(cls, cards):
    prev_card = None
    for card in sorted(cards):
      if not prev_card:
        prev_card = card
      elif card.num - prev_card.num > 1:
        return False
      else:
        prev_card = card

    return True

  @classmethod
  def tuples(cls, cards):
    tup = []
    tuples = []
    for card in sorted(cards):
      if not tup:
        tup.append(card)
      else:
        if all(card == tup_card for tup_card in tup):
          tup.append(card)
        else:
          tuples.append(tup)
          tup = []
    return tuples


  @classmethod
  def is_top_k(cls, game, player, cards):
    game_cards = [GameCard(game, card) for card in cards]
    compare_game_cards = lambda card, other: other.is_trump if card.is_trump else card.suit == other.suit

    other_cards = []
    for other_player in game.players:
      if player.id == other_player.id:
        continue
      else:
        other_cards.extend(other_player.hand)

    other_game_cards = []
    for game_card in game_cards:
      for other_card in other_cards:
        other_game_card = GameCard(game, other_card)
        if compare_game_cards(game_card, other_game_card):
          other_game_cards.append(other_game_card)

    for game_card in game_cards:
      for other_game_card in other_game_cards:
        if not game_card > other_game_card:
          return False

    return True