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
        trans = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3,
                 "2": 2}
        return trans.get(char)

    def get_card_value_from_hand(self, i):
        return self.transform(self.obs.my_hand[i][0])

    def get_card_values(self, cards):
        allCards = []
        for card in cards:
            allCards.append(self.transform(card[0]))
        return allCards.sort(reverse=True)

    def straight_case(self, cards):
        cards = list(map(lambda el: self.transform(el[0]), cards))
        if 14 in cards:
            cards.append(1)

        count = 0

        for i in range(1, 15):
            if self.in_a_row(cards + [i], 5):
                count += 1
        return count

    def in_a_row(self, cards, to_check):
        cards.sort()
        in_a_row = 1
        for i in range(1, len(cards)):
            if cards[i] == cards[i - 1]:
                continue
            elif cards[i] - cards[i - 1] != 1:
                in_a_row = 0
            else:
                in_a_row += 1
            if in_a_row == to_check:
                return True
        return False

    def flush_cards_count(self, cards):
        # c s d h
        arr = [0, 0, 0, 0]

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

    def get_all_cards(self):
        return self.obs.board_cards + self.obs.my_hand

    def get_card_rank_from_cards(self, card, cards):
        return self.get_card_values(cards).index(card)

    def check_range(self, range):
        return Range(range).is_hand_in_range(self.obs.my_hand)

    def try_raise_pot(self, raise_amount):
        if raise_amount * self.obs.get_pot_size() > self.obs.get_my_player_info().stack:
            return self.obs.get_max_raise()
        return raise_amount - 1

    def try_raise_bb(self, raise_amount):
        if raise_amount * self.obs.big_blind() > self.obs.get_my_player_info().stack:
            return self.obs.get_max_raise()
        return raise_amount

    def get_pair_value_not_on_board(self):
        val = get_pair_value(self, self.obs.board_cards)
        cards = (self.get_card_values(self.get_all_cards()).remove(val)).remove(val)
        return self.get_pair_value(cards)

    def get_pair_value(self, cards):
        seen = set()
        for num in self.get_card_values(cards):
            if num in seen:
                return num
            seen.add(num)

    def fold_else_call(self, bb_to_fold):
        if seelf.obs.get_call_size() > bb_to_fold * elf.obs.big_blind:
            return 0
        return 1

    def fold_else_raise_bb(self, bbToFold, bbToRaise):
        if self.obs.get_call_size() > bbToFold * self.obs.big_blind:  ##calls
            return 0
        else:
            return self.try_raise_bb(bbToRaise)

    def fold_else_raise_pot(self, potToFold, potToRaise):
        if self.obs.get_call_size() > potToFold * self.obs.get_pot_size():  ##calls
            return 0
        else:
            return self.try_raise_pot(potToRaise)

    def pre_flop(self):
        play = 0

        match self.obs.get_player_count():
            case 2:
                if self.obs.get_call_size() > 8 * self.obs.big_blind:
                    if self.check_range("77+, A8s+, KTs+, QJs, AJo+, KQo"):
                        play = self.try_raise_pot(2)
                elif self.obs.get_call_size() > 4 * self.obs.big_blind:
                    if self.check_range("55+, A4s+, K9s+, Q9s+, JTs, A9o+, KTo+, QJo"):
                        play = self.try_raise_pot(2)
                elif self.check_range("44+, A2s+, K3s+, Q6s+, J8s+, T8s+, 98s, A4o+, K8o+, Q9o+, JTo"):
                    play = self.try_raise_pot(2)
            case 3:
                if self.obs.get_call_size() > 8 * self.obs.big_blind:
                    if self.check_range("77+, ATs+, KQs, AQo+"):
                        play = self.try_raise_pot(2)
                elif self.obs.get_call_size() > 4 * self.obs.big_blind:
                    if self.check_range("77+, A8s+, KTs+, QJs, AJo+, KQo"):
                        play = self.try_raise_pot(2)
                elif self.check_range("55+, A4s+, K9s+, Q9s+, JTs, A9o+, KTo+, QJo"):
                    play = self.try_raise_pot(2)
            case _:
                if self.obs.get_call_size() > 4 * self.obs.big_blind:
                    if self.check_range("77+, ATs+, KQs, AQo+"):
                        play = self.try_raise_pot(2)
                elif self.check_range("77+, A8s+, KTs+, QJs, AJo+, KQo"):
                    play = self.try_raise_pot(2)
        return play  # All-in

    def post_flop(self):
        play = 0

        boardCards = self.obs.board_cards
        handHighCard = max(self.get_card_value_from_hand(0), self.get_card_value_from_hand(1))

        match self.obs.get_player_count():
            case 2:
                match self.obs.get_my_hand_type():
                    case 1:
                        return self.obs.get_max_raise()
                    case 2:
                        return self.obs.get_max_raise()
                    case 3:
                        return self.obs.get_max_raise()
                    case 4:
                        return self.obs.get_max_raise()
                    case 5:
                        return self.obs.get_max_raise()
                    case 6:
                        return self.obs.get_max_raise()
                    case 7:
                        return self.obs.get_max_raise()
                    case 8:
                        return self.obs.get_max_raise()
                    case 9:
                        return self.obs.get_max_raise()
            case _:
                # Need to take chance of opponent flush and straight into account
                # need to make changes to high card
                #stfu
                match self.obs.get_my_hand_type():
                    case 1: # have high card
                        if self.flush_cards_count(self.get_all_cards()) == 4:  # flush
                            if self.straight_case(self.get_all_cards()) != 0:  # straight
                                play = self.fold_else_call(6)
                            else:
                                if self.get_card_rank_from_cards(handHighCard, self.get_all_cards()) == 0:
                                    play = self.fold_else_raise_bb(6, 2)
                                elif self.get_card_rank_from_cards(handHighCard, self.get_all_cards()) == 1:
                                    play = self.fold_else_call(3)
                                else:
                                    play = 0
                        else:
                            if self.straight_case(self.get_all_cards()) != 0:  # straight
                                if self.get_card_rank_from_cards(handHighCard, self.get_all_cards()) == 0:
                                    play = self.fold_else_raise_bb(3, 4)
                                elif self.get_card_rank_from_cards(handHighCard, self.get_all_cards()) == 1:
                                    play = self.fold_else_raise_bb(2, 4)
                                else:
                                    play = 0
                            else:
                                if self.get_card_rank_from_cards(handHighCard, self.get_all_cards()) == 0:
                                    play = self.fold_else_raise_bb(2, 4)
                    case 2: # have pair
                        if self.obs.get_board_hand_type() != 2:  # par not on table
                            if self.get_card_rank_from_cards(self.get_pair_value(self.get_all_cards())) == 0:  # par is highest card
                                if self.flush_cards_count(self.get_all_cards()) == 4:  # flush
                                    if self.straight_case(self.get_all_cards()) != 0:  # straight
                                        play = self.try_raise_pot(1)
                                    else:
                                        play = self.try_raise_pot(0.5)
                                else:
                                    if self.straight_case(self.get_all_cards()) != 0:  # straight
                                        play = self.try_raise_pot(0.5)
                                    else:
                                        play = self.fold_else_raise_pot(0.5, 0.5)
                            else:
                                if self.flush_cards_count(self.get_all_cards()) == 4:  # flush
                                    if self.straight_case(self.get_all_cards()) != 0:  # straight
                                        if self.obs.get_call_size() > 11 * self.obs.big_blind:  ##calls
                                            play = 0
                                        else:
                                            play = self.try_raise_pot(0.5)
                                    else:
                                        play = self.fold_else_raise_bb(5, 4)
                                else:
                                    if self.straight_case(self.get_all_cards()) != 0:  # straight
                                        play = self.fold_else_raise_bb(3, 4)
                                    else:
                                        play = self.fold_else_raise_bb(2, 4)
                        else: # pair on table
                            if self.flush_cards_count(self.get_all_cards()) == 4:  # flush
                                if self.straight_case(self.get_all_cards()) != 0:  # straight
                                    play = self.fold_else_raise_bb(4, 4)
                                else: # not close to straight
                                    if self.get_card_rank_from_cards(handHighCard, self.get_all_cards()) == 0: # has highest card
                                        play = self.fold_else_raise_bb(3, 4)
                                    else: # does not have highest card
                                        play = 0
                            else: # not close to flush
                                if self.straight_case(self.get_all_cards()) != 0:  # straight
                                    if self.get_card_rank_from_cards(handHighCard, self.get_all_cards()) == 0: # have highest card
                                        play = self.fold_else_raise_bb(3, 4)
                                    else: # does not have highest card
                                        play = 0
                                else: # not close to straight
                                    play = 0
                    case 3: # have two pairs
                        if self.obs.get_board_hand_type() != 2: # pair not on table
                            if self.flush_cards_count(boardCards) == 3:  # opponent flush chance
                                if self.in_a_row(boardCards, 3):  # opponent straight chance
                                    play = self.fold_else_raise_bb(4,4)
                                else: # opponent not straight
                                    play = self.fold_else_raise_bb(6,4)
                            else: # opponent not flush
                                if self.in_a_row(boardCards, 3):  # opponent straight chance
                                    play = self.fold_else_raise_pot(0.5,0.5)
                                else: # opponent not straight
                                    play = self.try_raise_pot(2)
                        else: # pair on table
                            if self.get_card_rank_from_cards(self.get_pair_value_not_on_board()) == 0: # our pair is higher than board pair
                                play = self.fold_else_raise_bb(8,4)
                            else: # pair on table is is better than our
                                play = self.fold_else_raise_bb(4,4)
                    case 4: # have set
                        if self.obs.get_board_hand_type() == 4: # set on table
                            play = self.fold_else_call(2)
                        elif self.obs.get_board_hand_type() == 2: # pair on table
                            play = self.try_raise_pot(1)
                        else: # pair on hand
                            if self.flush_cards_count(boardCards) == 3:  # opponent flush chance
                                if self.in_a_row(boardCards, 3):  # opponent straight chance
                                    play = self.fold_else_call(4)
                                else: # no chance for straight
                                    play = self.fold_else_raise_bb(6,4)
                            else: # no flush chance
                                if self.in_a_row(boardCards, 3):  # opponent straight chance
                                    play = self.fold_else_raise_bb(8,4)
                                else: # no chance for straight
                                    play = self.try_raise_pot(1.1)        
                    case 5: # have straight
                        if self.flush_cards_count(boardCards) == 3: # opponent flush chance
                            play = self.fold_else_raise_pot(0.5,0.5)
                        else:
                            play = self.try_raise_pot(1)
                    case 6: # flush
                        play = self.try_raise_pot(1)
                    case 7: # full house
                        if self.obs.get_board_hand_type() == 4: # set on table
                            play = self.fold_else_raise_pot(0.5,0.5)
                        else: # knep dem 
                            play = self.try_raise_pot(1)
                    case 8: # four in a row - knep dem
                        play = self.try_raise_pot(1)
                    case 9: # straight flush - KNEP DEM
                        play = self.try_raise_pot(1)

        if self.obs.get_player_count() == 2 or self.obs.get_player_count() == 3:
            x = 2

        return play

    def turn(self):
        play = 0

        boardCards = self.obs.board_cards
        handHighCard = max(self.get_card_value_from_hand(0), self.get_card_value_from_hand(1))

        match self.obs.get_player_count():
            case 2:
                match self.obs.get_my_hand_type():
                    case 1:
                        return self.obs.get_max_raise()
                    case 2:
                        return self.obs.get_max_raise()
                    case 3:
                        return self.obs.get_max_raise()
                    case 4:
                        return self.obs.get_max_raise()
                    case 5:
                        return self.obs.get_max_raise()
                    case 6:
                        return self.obs.get_max_raise()
                    case 7:
                        return self.obs.get_max_raise()
                    case 8:
                        return self.obs.get_max_raise()
                    case 9:
                        return self.obs.get_max_raise()
            case _:
                match self.obs.get_my_hand_type():
                    case 1: # have high card
                        if self.flush_cards_count(self.get_all_cards()) == 4:  # flush
                            if self.straight_case(self.get_all_cards()) != 0:  # straight
                                play = self.fold_else_raise_bb(2, 4)
                            else: # no chance for straight
                                play = 0
                        else:
                            play = 0
                    case 2: # have pair
                        if self.obs.get_board_hand_type() != 2:  # par not on table
                            if self.get_card_rank_from_cards(self.get_pair_value(self.get_all_cards())) == 0:  # par is highest card
                                if self.flush_cards_count(self.get_all_cards()) == 4:  # flush
                                    if self.flush_cards_count(boardCards) == 4: # if flush chance is on board
                                        if self.straight_case(self.get_all_cards()) != 0:  # straight
                                            if self.straight_case(boardCards) != 0: # if straight chance is on board
                                                play = 0
                                            else: # straight chance not on board
                                                play = 0
                                        else: # we have no straight chance
                                            play = 0
                                    elif self.flush_cards_count(boardCards) == 3: # flush chance lower on board
                                        if self.straight_case(self.get_all_cards()) != 0:  # straight
                                            if self.straight_case(boardCards) != 0: # if straight chance is on board
                                                    play = 0
                                            else: # straight chance not on board
                                                play = self.fold_else_call(2)
                                        else: # we have no straight chance
                                            play = 0
                                    else: # no flush chance of board
                                        if self.straight_case(self.get_all_cards()) != 0:  # straight
                                            if self.straight_case(boardCards) != 0: # if straight chance is on board
                                                    play = self.fold_else_call(4)
                                            else: # straight chance not on board
                                                play = self.fold_else_raise_bb(8,4)
                                        else: # we have no straight chance
                                            play = self.fold_else_raise_bb(4,4)                                    
                                else: # if we have no flush chance
                                    if self.straight_case(self.get_all_cards()) != 0:  # straight
                                        if self.straight_case(boardCards) != 0: # if straight chance is on board
                                                play = 0
                                        else: # straight chance not on board
                                            play = self.fold_else_call(2)
                                    else: # if no straight chance
                                        play = self.fold_else_call(2)
                            else: # pair is no longer highest
                                if self.flush_cards_count(self.get_all_cards()) == 4:  # flush
                                    if self.flush_cards_count(boardCards) == 4: # if flush chance is on board
                                        if self.straight_case(self.get_all_cards()) != 0:  # straight
                                            if self.straight_case(boardCards) != 0: # if straight chance is on board
                                                play = 0
                                            else: # straight chance not on board
                                                play = 0
                                        else: # we have no straight chance
                                            play = 0
                                    elif self.flush_cards_count(boardCards) == 3: # flush chance lower on board
                                        if self.straight_case(self.get_all_cards()) != 0:  # straight
                                            if self.straight_case(boardCards) != 0: # if straight chance is on board
                                                    play = 0
                                            else: # straight chance not on board
                                                play = self.fold_else_call(2)
                                        else: # we have no straight chance
                                            play = 0
                                    else: # no flush chance of board
                                        if self.straight_case(self.get_all_cards()) != 0:  # straight
                                            if self.straight_case(boardCards) != 0: # if straight chance is on board
                                                    play = self.fold_else_call(2)
                                            else: # straight chance not on board
                                                play = self.fold_else_call(4)
                                        else: # we have no straight chance
                                            play = self.fold_else_call(2)                                   
                                else: # if we have no flush chance
                                    if self.straight_case(self.get_all_cards()) != 0:  # straight
                                        if self.straight_case(boardCards) != 0: # if straight chance is on board
                                                play = 0
                                        else: # straight chance not on board
                                            play = 0
                                    else: # if no straight chance
                                        play = 0
                        else: # pair on table
                            if self.flush_cards_count(self.get_all_cards()) == 4:  # flush
                                if self.flush_cards_count(boardCards) != 4: # if flush chance is on board
                                    if self.straight_case(self.get_all_cards()) != 0:  # straight
                                        if self.straight_case(boardCards) == 0:
                                            play = self.fold_else_call(4)
                                        else:
                                            play = 0
                                    else:
                                        play = 0
                                else:
                                    play = 0
                            else:
                                play = 0

                    case 3: # have two pairs
                        if self.obs.get_board_hand_type() != 2: # pair not on table
                            if self.flush_cards_count(boardCards) == 3:  # opponent flush chance
                                if self.in_a_row(boardCards, 3):  # opponent straight chance
                                    play = self.fold_else_raise_bb(4,4)
                                else: # opponent not straight
                                    play = self.fold_else_raise_bb(6,4)
                            else: # opponent not flush
                                if self.in_a_row(boardCards, 3):  # opponent straight chance
                                    play = self.fold_else_raise_pot(0.5,0.5)
                                else: # opponent not straight
                                    play = self.try_raise_pot(2)
                        else: # pair on table
                            if self.get_card_rank_from_cards(self.get_pair_value_not_on_board()) == 0: # our pair is higher than board pair
                                play = self.fold_else_raise_bb(8,4)
                            else: # pair on table is is better than our
                                play = self.fold_else_raise_bb(4,4)
                    case 4: # have set
                        if self.obs.get_board_hand_type() == 4: # set on table
                            play = self.fold_else_call(2)
                        elif self.obs.get_board_hand_type() == 2: # pair on table
                            play = self.try_raise_pot(1)
                        else: # pair on hand
                            if self.flush_cards_count(boardCards) == 3:  # opponent flush chance
                                if self.in_a_row(boardCards, 3):  # opponent straight chance
                                    play = self.fold_else_call(4)
                                else: # no chance for straight
                                    play = self.fold_else_raise_bb(6,4)
                            else: # no flush chance
                                if self.in_a_row(boardCards, 3):  # opponent straight chance
                                    play = self.fold_else_raise_bb(8,4)
                                else: # no chance for straight
                                    play = self.try_raise_pot(1.1)        
                    case 5: # have straight
                        if self.flush_cards_count(boardCards) == 3: # opponent flush chance
                            play = self.fold_else_raise_pot(0.5,0.5)
                        else:
                            play = self.try_raise_pot(1)
                    case 6: # flush
                        play = self.try_raise_pot(1)
                    case 7: # full house
                        if self.obs.get_board_hand_type() == 4: # set on table
                            play = self.fold_else_raise_pot(0.5,0.5)
                        else: # knep dem 
                            play = self.try_raise_pot(1)
                    case 8: # four in a row - knep dem
                        play = self.try_raise_pot(1)
                    case 9: # straight flush - KNEP DEM
                        play = self.try_raise_pot(1)

        if self.obs.get_player_count() == 2 or self.obs.get_player_count() == 3:
            x = 2

        return play

    def river(self):
        print(self.straight_case(self.obs.board_cards + self.obs.my_hand))
        return self.obs.get_max_raise()  # All-in

    def showdown(self):
        print(self.straight_case(self.obs.board_cards + self.obs.my_hand))
        return self.obs.get_max_raise()  # All-in

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
                play = self.showdown()
            case _:
                play = obs.get_max_raise()
        return play
