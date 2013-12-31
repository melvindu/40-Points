class Round(object):
  """
  Round class. Base class and factory for 40 point game rounds.
  Each subclass, given a set of cards, should be able to return
  a list of eligible card plays. 
  """
  @classmethod
  def factory(cls, game, player, cards):
    # TODO(yjohnmei): create the appropriate round type given the cards and game.
    if len(cards) == 1:
      return SingleCardRound(game, player, cards)
    if len(cards) > 1:
      cards.sort()
      
      """if number of cards > 1, checks to see if all cards are the same"""
      for i in range(len(cards) - 1):
        cur = cards[i]
        next = cards[i + 1]
        if cur.__eq__(next):
          allSame = True
        else allSame = False          
      if (allSame):
        return TupleCardsRound(game, player, cards)
      
      """if number of cards > 1 && cards not the same, check if hand is all (non)consecutive tuples"""
      tupleChecker = defaultdict(int)
      for j in range(len(cards)):
        cur = cards[j]
        tupleChecker[cur] += 1
      keys = tupleChecker.keys()
      curKey = keys[0]
      tuples = True
      for key in keys: 
        int copies = keys[key]
        if curKey != copies:
          tuples = False
      if (tuples): # if tuples is true, check if they're consecutive
        consecutiveTuples = True
        for (index, key) in enumerate(keys.sort()):
          if key.suit != keys[index + 1].suit or key.number != keys[index + 1].number - 1:
            consecutiveTuples = False
        if (consecutiveTuples)
          return ConsecutiveTupleCardsRound(game, player, cards)
        else:
          return TupleCardsRound(game, player, cards)
     
    """   
    else check that the cards being are the highest cards in that suit
    look at the card "groups" that are in play and then check to see that there's no group in someone's hand that's higher than the current group
    is there a tuple? how many? if there is, mark this as a tuple with n tuples is there a consectuple? if there is, mark it as a consectuple
    """  
     remainder = []
     for player in games.players:
       hand = player.hand
       for card in hand:
         remainder.append(card)
     remainderHash = defaultdict(int)
     for k in range(len(remainder)):
       cur2 = remainder[k]
       remainderHash[cur2] += 1
     
     remainderKeys = remainderHash.keys()
     intTuples = 0
     
     for key in keys: # go through each card being played
       for remainderKey in remainderKeys: # go through each card in the remainder of deck 
       if key.suit != remainderKey.suit:
         continue
       if key.number < remainderKey.number:
         if tupleChecker[key] <= remainderHash[remainderKey]:
           
           return TopCardsRound(game, player, cards)
         

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

  def add_play(self, player, cards):
    if cards not in self.eligible_plays(player):
      raise ValueError('Cannot add illegal play to round')
    self._plays[player] = cards

  def eligible_plays(player):
    raise NotImplementedError


class SingleCardRound(Round):
  pass

class ConsecutiveTupleCardsRound(Round):
  pass

class TupleCardsRound(Round):
  pass

class TopCardsRound(Round):
  pass
  
class TopConsectutiveTupleCardsRound(TopCardsRound):
  pass
  
class TopTupleCardsRound(TupleCardsRound, TopCardsRound):
  pass
