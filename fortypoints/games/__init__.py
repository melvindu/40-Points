class Round(object):
  """
  Round class. Base class and factory for 40 point game rounds.
  Each subclass, given a set of cards, should be able to return
  a list of eligible card plays. 
  """
  @classmethod
  def profactory(cls, game, player, play):
    """check for single card play"""
    if len(play) == 1:    
      return SingleCardRound(game, player, play)

    if len(play) > 1:
      play.sort()
     
      """if number of cards > 1, checks to see if all cards are the same"""
      for i in range(len(play) - 1):
        if play[i].__eq__(play[i + 1]):
          allSame = True
        else:
          allSame = False          
      if (allSame):
        return PairCardsRound(game, player, play)   
        
      """if number of cards > 1 && cards not the same, check if play is all consecutive tuples"""
      pairTracker = defaultdict(int)
      for j in range(len(play)):
        pairTracker[play[j]] += 1
      cardValueList = cardTracker.keys()
      numPairs = cardValueList[0]
      containsPairs = True
      for cardValue in cardValueList: 
        numCopies = cardValueList[cardValue]
        if numPairs != numCopies:
          containsPairs = False
      if (containsPairs): # if hand is all tuples, see if they're consecutive
        isConsecutivePairCardsRound = True
        numConsecutivePairs = 1
        for (index, key) in enumerate(cardValueList.sort()):
          if key.suit != keys[index + 1].suit or key.number != keys[index + 1].number - 1:
            isConsecutivePairCardsRound = False
          else:
            numConsecutivePairs += 1
        if (isConsecutivePairCardsRound):
          return ConsecutivePairCardsRound(game, player, play)

      remainder = []
      for player in games.players:
        hand = player.hand
        for card in hand:
          remainder.append(card)
         
      remainderHash = defaultdict(int)
      for k in range(len(remainder)):
        remainderHash[remainder[k]] += 1

      """below, check cardgroup against cardgroups in the remainderdeck to see if there's any higher cardgroups there"""
      isTopCardsRound = True
      numPairs = defaultdict(int)
      for card in cardValueList: 
        """this shit is not immediately useful. it just counts the number of tuples"""
        if pairTracker[card] == 2:
          numPairs[pairTracker[card]] += 1 #numTuples is actually hash table for init play
      
        for remainderCard in remainder: 
          if card.suit != remainderCard.suit:
            continue
          if card.number < remainderCard.number:
            if pairTracker[card] <= remainderHash[remainderCard]:
              isTopCardsRound = False # if any cardgroup is higher, then topGame is false
 
      """by now this is definitely a topcardround, now to see if there's any tuples and how many tuples up in here"""
      if isTopCardsRound:
        if numPairs:
          numConsecutivePairs = 0
          isTopConsecutivePairsRound = True
          for (index, card) in enumerate(cardValueList.sort()):
            if card.suit != cardValueList[index + 1].suit or card.number != cardValueList[index + 1].number - 1:
              isTopConsecutivePairsCardsRound = False
            elif pairTracker[card] == 2 && pairTracker[cardValueList[index + 1]] == 2:
              numConsecutivePairs += 1
          if (isTopConsecutivePairsCardsRound):
            return TopConsecutivePairCardsRound(game, player, play)
          else:
            return TopCardsRound(game, player, play)
     
      """if gets to here without returning something, this is a failed play"""
    
  @classmethod
  def factory(cls, game, player, play): # RIP n decks ;_; 
    """check for single card play"""
    if len(play) == 1:    
      return SingleCardRound(game, player, play)
    
    if len(play) > 1:
      play.sort()
      
      """if number of cards > 1, checks to see if all cards are the same"""
      for i in range(len(play) - 1):
        if play[i].__eq__(play[i + 1]):
          allSame = True
        else:
          allSame = False          
      if (allSame):
        return TupleCardsRound(game, player, play)
      
      """if number of cards > 1 && cards not the same, check if play is all consecutive tuples"""
      tupleTracker = defaultdict(int)
      for j in range(len(play)):
        tupleTracker[play[j]] += 1
      cardValueList = tupleTracker.keys()
      numTuples = cardValueList[0]
      constainsTuples = True
      for cardValue in cardValueList: 
        numCopies = cardValueList[tuple]
        if numTuples != numCopies:
          containsTuples = False
      if (containsTuples): # if hand is all tuples, see if they're consecutive
        isConsecutiveTupleCardsRound = True
        numConsecutiveTuples = 0
        for (index, key) in enumerate(cardValueList.sort()):
          if key.suit != keys[index + 1].suit or key.number != keys[index + 1].number - 1:
            isConsecutiveTupleCardsRound = False
          else:
            numConsecutiveTuples += 1
        if (isConsecutiveTupleCardsRound):
          return ConsecutiveTupleCardsRound(game, player, play)
     
      """   
      else check that the cards are the highest cards in that suit:
      look at the card "groups" that are in play and then check to see that there's no group in someone's hand that's higher than the current group
      is there a tuple? how many? if there is, mark this as a tuple with n tuples is there a consectuple? if there is, mark it as a consectuple
      """  
      """making hash table for remainder of deck"""
      remainder = []
      for player in games.players:
        hand = player.hand
        for card in hand:
          remainder.append(card)
         
      remainderHash = defaultdict(int)
      for k in range(len(remainder)):
        remainderHash[remainder[k]] += 1
     
      """below, check cardgroup against cardgroups in the remainderdeck to see if there's any higher cardgroups there"""
      isTopCardsRound = True
      numTuples = defaultdict(int)
      for card in cardValueList: 
      
        """this shit is not immediately useful. it just counts the number of tuples"""
        if tupleTracker[card] > 1:
          numTuples[tupleTracker[card]] += 1 #numTuples is actually hash table for init play
      
        for remainderCard in remainder: 
          if card.suit != remainderCard.suit:
            continue
          if card.number < remainderCard.number:
            if tupleTracker[card] <= remainderHash[remainderCard]:
              isTopCardsRound = False # if any cardgroup is higher, then topGame is false
 
      """by now this is definitely a topcardround, now to see if there's any tuples and how many tuples up in here"""
      if isTopCardsRound:
        if numTuples:
          isTopConsecutiveTuplesRound = True
          for (index, card) in enumerate(cardValueList.sort()):
            if card.suit != cardValueList[index + 1].suit or card.number != cardValueList[index + 1].number - 1: # problem
              isTopConsecutiveTupleCardsRound = False
          if (isTopConsecutiveTupleCardsRound):
            return TopConsecutiveTupleCardsRound(game, player, play)
          else:
            return TopCardsRound(game, player, play)
     
      """if gets to here without returning something, this is a failed play"""

  def __init__(game, player, play):
    self._game = game
    self._plays = {player: play}

  @property
  def size(self):
    return self._game.size

  @property
  def game(self):
    return self.game

  @property
  def plays(self):
    return self._plays

  def add_play(self, player, play):
    if play not in self.eligible_plays(player):
      raise ValueError('Cannot add illegal play to round')
    self._plays[player] = play

  def eligible_plays(player):
    eligible = []
    """if it is a single card non-trump round, add in all cards of the same suit. if out of that suit, add in all trump cards. if it is out of that suit and it is a TRUMP round then add in all cards."""
    FOR SingleCardRound CASE #dunno syntax
        hand = player.hand
        suit = SingleCardRound.play.suit
        for card in hand:
          if card.suit = suit: #dunno syntax
            eligible.append(card)
        if eligible IS BLANK #dunno syntax
          if suit != TRUMP
            for card in hand where card.suit = TRUMP #dunno syntax
            eligible.append(card) #add in all  trump cards as eligible play if they're out of the suit  
            if suit = TRUMP
              for eligible.
              
              
      hand = player.hand
            for player in games.players:
        hand = player.hand
        for card in hand:
          remainder.append(card)
      add to eligiblePlays;
      return eligiblePlays; 
    raise NotImplementedError


class SingleCardRound(Round):
  pass

class ConsecutivePairCardsRound(Round):
  pass

class PairCardsRound(Round):
  pass

class TopCardsRound(Round):
  pass
  
class TopConsectutivePairCardsRound(TopCardsRound):
  pass
  
class TopPairCardsRound(PairCardsRound, TopCardsRound):
  pass
