import fortypoints as fp
from fortypoints.players import create_player
from fortypoints.games.models import Game

db = fp.db


def get_game(game_id):
  return Game.get(id=game_id)
 
 
def create_game(users):
  game = Game(len(users))
  db.session.add(game)
  db.session.commit()
  for user in users:
    create_player(game, user)
  return game
  

class Play(object):
  def __init__(self, game, player, cards, plays):
    if self.eligible(self, game, player, cards, plays):
        self.game == game
        self.player = player
        self.cards = cards
    else:
      raise Exception
        
  def __eq__(self, other):
    same = self.game == other.game
    same = same and self.player == other.player
    same = same and self.cards == other.cards
    return same
 
class SingleCardPlay(Play):
  def eligible(self, game, player, cards, plays):
    first = plays[0].cards[0]
    el = lambda card: card.trump if first.trump else first.suit == card.suit
    canplay = filter(el, player.hand)
   
    if not canplay:
     canplay=cards
    return cards[0] in canplay
    
  
  def __eq__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.cards[0]
    suit = first_card.suit
    if self.cards[0].suit == other.cards[0].suit:
      return self.cards[0] < other.cards[0]
    if other.cards[0].suit == suit and self.cards[0].suit != suit:
      if self.cards[0].suit != trump_suit:
        return False
      elif self.cards[0].suit == trump_suit:
        return True
    if other.cards[0].suit != suit and self.cards[0].suit == suit:
      if other.cards[0].suit != trump_suit:
        return True
      elif other.cards[0].suit == trump_suit:
        return False
    if other.cards[0].suit != suit and self.cards[0].suit != suit:
      if other.cards[0].suit == trump_suit:
        return True
      if self.cards[0].suit == trump_suit:
        return False
    return False
    
  def __gt__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.cards[0]
    suit = first_card.suit
    if self.cards[0].suit == other.cards[0].suit:
      return self.cards[0] > other.cards[0]
    if other.cards[0].suit == suit and self.cards[0].suit != suit:
      if self.cards[0].suit != trump_suit:
        return Truee
      elif self.cards[0].suit == trump_suit:
        return False
    if other.cards[0].suit != suit and self.cards[0].suit == suit:
      if other.cards[0].suit != trump_suit:
        return False
      elif other.cards[0].suit == trump_suit:
        return True
    if other.cards[0].suit != suit and self.cards[0].suit != suit:
      if other.cards[0].suit == trump_suit:
        return False
      if self.cards[0].suit == trump_suit:
        return True
    return False

class PairCardsPlay(Play):
  def eligible(self, game, player, cards, plays):

    first_suit = plays[0].cards[0].gamesuit
    hand = player.hand
    num_suit = 0
    num_pairs_suit = 0
    cards_in_suit = defaultdict(int)
    for card in hand:
      if card.gamesuit == first_suit:
        cards_in_suit[card] += 1
        num_suit += 1
        
    # if out of that suit, you can play anything
    if num_suit == 0:
      return True
    
    # count the num of pairs
    card_list = sorted(cards_in_suit.keys())
    for (index, card) in enumerate(card_list):
      if card_table[card] == 2:
        num_pairs_suit += 1
   
    #count the number of cards in current play that match suit with first play
    num_suit_in_play = 0
    for card in cards:
      if card.gamesuit == first_suit:
        num_suit_in_play += 1
        
    # play must be a pair of the same suit if you have it
    if num_pairs_suit > 0:
      if num_suit_in_play == 2:
        return self.is_pair(cards)
      else:
        return False

    # if no pairs of that suit, play must be of that suit
    if num_pairs_suit == 0 and num_suit > 1:
      return num_suit_in_play == 2
   
     # if exactly 1 card of that suit, play must have that card in it
    if num_suit == 1:
      return num_suit_in_play == 1    
    
  def is_pair(self):
    return self.play[0] == self.play[1]
    
  def cards_share_suit(self):
    return self.play[0].suit == self.play[1].suit
  
  def __eq__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    """if they're 1) not pairs or 2) not in the current or trump suit, they're equally bad"""
    if not self.is_pair() and not other.is_pair():
      return True
    if self.cards[0].suit != suit and other.cards[0].suit != suit:
      if self.cards[0].suit != trump_suit and other.cards[0].suit != trump_suit:
        return True
    return False    

  def __lt__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    """if other play is a pair, check to see that self is either not a pair or a lower pair"""
    if other.is_pair:
      if other.cards[0].suit == suit or other.cards[0].suit == trump_suit:
        if not self.is_pair:
          return True
        elif self.cards[0].number < other.cards[0].number:
          return True
    return False
    
  def __gt__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    if self.is_pair:
      if self.cards[0].suit == suit or self.cards[0].suit == trump_suit:
        if not other.is_pair:
          return True
        elif other.cards[0].number < self.cards[0].number:
          return True
    return False

class ConsecutivePairCardsPlay(Play):
  def all_same_suit(self):
    first_suit = self.play[0].suit
    for card in self.play:
      if card.suit != first_suit:
        return False
    return True
  
  def is_consecutive_pairs(self):
    if not self.all_same_suit:
      return False
    card_table = defaultdict(int)
    for i in range(len(self.play)):
      card_table[self.play[i]] += 1
    card_list = sorted(card_table.keys())
    for (index, card) in enumerate(card_list):
      if card_table[card] != 2:
        return False
      if index != card_list - 1:
        if card_list[index].number != card_list[index+1].number - 1:
          return False
    return True
  
  def __eq__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    if not self.is_consecutive_pairs() and not other.is_consecutive_pairs():
      return True
    if self.is_consecutive_pairs() and other.is_consecutive_pairs():
      if self.play[0].suit != suit and other.play[0].suit != suit:
        if self.play[0].suit != trump_suit and other.play[0].suit != trump_suit:
          return True
    return False

  def __lt__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    if not self.is_consecutive_pairs() and other.is_consecutive_pairs():
      return True
    if self.is_consecutive_pairs() and other.is_consecutive_pairs():
      self_cards = sorted(self.play, reverse=True)
      other_cards = sorted(other.play, reverse=True)
      if self_cards[0] < other_cards[0]:
        return True
    return False
      
  
  def __gt__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    if not other.is_consecutive_pairs() and self.is_consecutive_pairs():
      return True
    if self.is_consecutive_pairs() and other.is_consecutive_pairs():
      self_cards = sorted(self.play, reverse=True)
      other_cards = sorted(other.play, reverse=True)
      if self_cards[0] > other_cards[0]:
        return True
    return False

class TopCardsPlay(Play):
  def all_same_suit(self):
    first_suit = self.play[0].suit
    for card in self.play:
      if card.suit != first_suit:
        return False
    return True
    
  def num_pairs(self):
    num_pairs = 0
    card_table = defaultdict(int)
    for i in range(len(self.play)):
      card_table[self.play[i]] += 1
    card_list = sorted(card_table.keys())
    num_pairs = 0
    for (index, card) in enumerate(card_list):
      if card_table[card] == 2:
        num_pairs += 1
    return num_pairs
  
  def num_consecutive_pairs(self):
    num_consecutive_pairs = 0
    card_table = defaultdict(int)
    for i in range(len(self.play)):
      card_table[self.play[i]] += 1
    card_list = sorted(card_table.keys())
    for (index, card) in enumerate(card_list):
      if index != card_list - 1:
        if card_list[index].number == card_list[index+1].number - 1:
          num_next_card = card_table[card_list[index+1]]
          if card_table[card] == 2 and num_next_card == 2:
            num_consecutive_pairs += 1
    return num_consecutive_pairs
  
  def __eq__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    original_num_pairs = current_play.num_pairs()
    original_consecutive_pairs = current_play.num_consecutive_pairs()
    # equally bad if they both have fewer pairs and consecutive pairs than the original
    if original_num_pairs > self.play.num_pairs() and original_num_pairs > other.play.num_pairs():
      return True
    if original_num_consecutive_pairs > self.play.num_consecutive_pairs() and original_num_consecutive_pairs > other.play.num_consecutive_pairs():
      return True
    # equally bad if they're not all-same-suited
    if not self.play.all_same_suit() and not other.play.all_same_suit():
      return True
    # equally bad if they're all same suit and not original suit not trump suit
    if self.play.all_same_suit() and other.play.all_same_suit():
      if self.play[0].suit != trump_suit and other.play[0].suit != trump_suit:
        return True
    return False

  def __lt__(self,other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    original_num_pairs = current_play.num_pairs()
    original_consecutive_pairs = current_play.num_consecutive_pairs()
    if self.play.all_same_suit and other.play.all_same_suit:
      if self.play.num_pairs() >= original_num_pairs and self.play.num_consecutive_pairs() >= original_consecutive_pairs:
        if other.play.num_pairs() >= original_num_pairs and other.play.num_consecutive_pairs() >= original_consecutive_pairs:
          self_cards = sorted(self.play, reverse=True)
          other_cards = sorted(other.play, reverse=True) 
          if self_cards[0] < other_cards[0]:
            return True
      if self.play.num_pairs() < original_num_pairs or self.play.num_consecutive_pairs() < original_num_pairs:
        if other.play.num_pairs >= original_num_pairs or other.play.num_consecutive_pairs() >= original_consecutive_pairs:
          return True
    if not self.play.all_same_suit and other.play.all_same_suit:
      return True
    return False

  def __gt__(self, other):
    trump_suit = self.game.trump_suit
    current_round = self.game.current_round
    current_play = current_round.plays[0]
    first_card = current_play.play[0]
    suit = first_card.suit
    original_num_pairs = current_play.num_pairs()
    original_consecutive_pairs = current_play.num_consecutive_pairs()
    if self.play.all_same_suit and other.play.all_same_suit:
      if self.play.num_pairs() >= original_num_pairs and self.play.num_consecutive_pairs() >= original_consecutive_pairs:
        if other.play.num_pairs() < original_num_pairs or other.play.num_consecutive_pairs() < original_consecutive_pairs:
          return True
        else:
          self_cards = sorted(self.play, reverse=True)
          other_cards = sorted(other.play, reverse=True) 
          if self_cards[0] > other_cards[0]:
            return True
    if self.play.all_same_suit and not other.play.all_same_suit:
      return True
    return False
    
          
class Round(object):
  """
  Round class. Base class and factory for 40 point game rounds.
  Each subclass, given a set of cards, should be able to return
  a list of eligible card plays. 
  """
  @classmethod
  def profactory(cls, game, player, play):
    SingleCardPlay(self.plays[0])
    PairCardsPlay(self.plays[0])

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
            elif pairTracker[card] == 2 and pairTracker[cardValueList[index + 1]] == 2:
              numConsecutivePairs += 1
          if (isTopConsec2utivePairsCardsRound):
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
      raise ValueError('Cannot play illegal play to round')
      
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