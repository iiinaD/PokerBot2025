from poker_game_runner.state import Observation
from poker_game_runner.utils import Range, HandType
import time
import random

#############################################################
# QUESTIONS:
# - 
#############################################################

class Bot:

  obs: Observation

  def get_name(self):
    return "kʁupəsɛks"

  def transform(self, char):
    trans = {"A":14, "K":13, "Q":12, "J":11, "T":10, "9":9, "8":8, "7":7, "6":6, "5":5, "4":4, "3":3, "2":2}
    return trans.get(char)

  def straight_case(self, cards):
    cards = list(map(lambda el: self.transform(el[0]), cards))
    if 14 in cards:
      cards.append(1)
    
    count = 0

    for i in range(1, 15):= 0
      print(f"CARDS: {cards}")
      print("STRAIGHTSHITDAMN")
    return count

  def five_in_a_row(self,cards):
    cards.sort()
    print(f"THESE should be sorted: {cards}")
    in_a_row = 1
    for i in range(1,len(cards)):
      if cards[i] == cards[i-1]:
        continue
      elif cards[i] - cards[i-1] != 1:
        in_a_row = 0
      else:
        in_a_row += 1
      if in_a_row == 5:
        return True
    return False

  def flush_cards_count(self, cards):
    # c s d h
    arr = [0,0,0,0]

    for card in cards:
      match card[1]:
        case 'c':
          arr[0] += 1
        case 's':
          arr[1] += 1
        case 'd':
          arr[2] += 1
        case 'h':
          arr[3] += 1
    return max(arr)

  def check_range(self,range):
    return Range(range).is_hand_in_range(self.obs.my_hand)

  def try_raise(self, raise_amount):
    if raise_amount*self.obs.get_pot_size() > self.obs.get_my_player_info().stack:
      return self.obs.get_max_raise()
    return raise_amount
      
  def pre_flop(self):
    play = 0

    match self.obs.get_player_count():
      case 2:
        if self.obs.get_call_size() > 8*self.obs.big_blind:
          if self.check_range("77+, A8s+, KTs+, QJs, AJo+, KQo"):
            play = self.try_raise(2)
        elif self.obs.get_call_size() > 4*self.obs.big_blind:
          if self.check_range("55+, A4s+, K9s+, Q9s+, JTs, A9o+, KTo+, QJo"):
            play = self.try_raise(2)
        elif self.check_range("44+, A2s+, K3s+, Q6s+, J8s+, T8s+, 98s, A4o+, K8o+, Q9o+, JTo"):
          play = self.try_raise(2)
      case 3:
        if self.obs.get_call_size() > 8*self.obs.big_blind:
          if self.check_range("77+, ATs+, KQs, AQo+"):
            play = self.try_raise(2)
        elif self.obs.get_call_size() > 4*self.obs.big_blind:
          if self.check_range("77+, A8s+, KTs+, QJs, AJo+, KQo"):
            play = self.try_raise(2)
        elif self.check_range("55+, A4s+, K9s+, Q9s+, JTs, A9o+, KTo+, QJo"):
          play = self.try_raise(2)
      case _:
        if self.obs.get_call_size() > 4*self.obs.big_blind:
          if self.check_range("77+, ATs+, KQs, AQo+"):
            play = self.try_raise(2)
        elif self.check_range("77+, A8s+, KTs+, QJs, AJo+, KQo"):
          play = self.try_raise(2)

    return play # All-in

  def post_flop(self):
    play = 0
    print("WE IN")
    print(f"FLUSH count board: {self.flush_cards_count(self.obs.board_cards)}")
    print(f"FLUSH count full: {self.flush_cards_count(self.obs.board_cards + self.obs.my_hand)}")
    print(self.straight_case(self.obs.board_cards + self.obs.my_hand))
    return 0
    


    if self.obs.get_player_count() == 2 or self.obs.get_player_count() == 3:
      x=2

    return play



  def turn(self):
    print(self.straight_case(self.obs.board_cards + self.obs.my_hand))
    return self.obs.get_max_raise() # All-in
  def river(self):
    print(self.straight_case(self.obs.board_cards + self.obs.my_hand))
    return self.obs.get_max_raise() # All-in
  def showdown(self):
    print(self.straight_case(self.obs.board_cards + self.obs.my_hand))
    return self.obs.get_max_raise() # All-in

  def act(self, obs: Observation):

    self.obs = obs

    play = obs.get_min_raise()
    
    match obs.current_round:
      case 0:
        play = self.pre_flop()
      case 1:
        play = self.post_flop()
      case 2:
        play = self.turn()
      case 3:
        play = self.river()
      case 4:
        play = self.howdown()
      case _:
        play = obs.get_max_raise()
    return play
