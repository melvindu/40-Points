class Round(object):
  """
  Round class. Base class and factory for 40 point game rounds.
  Each subclass, given a set of cards, should be able to return
  a list of eligible card plays. 
  """
  @classmethod
  def factory(cls, game, player, cards):
    # TODO(yjohnmei): create the appropriate round type given the cards and game.
    # raise an Exception if the cards are not allowed to be played given game state.
    pass

  def __init__(game, player, cards):
    self._game = game
    self._plays = {player: cards}

  @property
  def size(self):
    return self._game.size

  @property
  def game(self):
    return self.game

  @property
  def plays(self):
    return self._plays

  def add_play(player, cards):
    if cards not in self.eligible_plays(player):
      raise ValueError('Cannot add illegal play to round')
    self._plays[player] = cards

  def eligible_plays(player):
    raise NotImplementedError


class SingleCardRound(Round):
  pass


class TupleCardsRound(Round):
  pass


class TopCardsRound(Round):
  pass