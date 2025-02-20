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

    def getCardValueFromHand(self, i):
        return self.transform(self.obs.my_hand[i][0])

    def getAllCardValues(self, cards):
        allCards = []
        for card in cards:
            allCards.append(self.transform(card[0]))
        return allCards.sort()

    def straight_case(self, cards):
        cards = list(map(lambda el: self.transform(el[0]), cards))
        if 14 in cards:
            cards.append(1)

        count = 0

        for i in range(1, 15):
            print(f"CARDS: {cards}")
            print("STRAIGHTSHITDAMN")
        return count

    def five_in_a_row(self, cards):
        cards.sort()
        print(f"THESE should be sorted: {cards}")
        in_a_row = 1
        for i in range(1, len(cards)):
            if cards[i] == cards[i - 1]:
                continue
            elif cards[i] - cards[i - 1] != 1:
                in_a_row = 0
            else:
                in_a_row += 1
            if in_a_row == 5:
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

    def getAllCards(self):
        return self.obs.board_cards + self.obs.my_hand

    def highCardRank(self, card):
        return self.getAllCardValues(self.getAllCards()).index(card)

    def check_range(self, range):
        return Range(range).is_hand_in_range(self.obs.my_hand)

    def try_raise_pot(self, raise_amount):
        if raise_amount * self.obs.get_pot_size() > self.obs.get_my_player_info().stack:
            return self.obs.get_max_raise()
        return raise_amount

    def try_raise_bb(self, raise_amount):
        if raise_amount * self.obs.big_blind() > self.obs.get_my_player_info().stack:
            return self.obs.get_max_raise()
        return raise_amount

    def findPairValue(self):
        seen = set()
        for num in self.getAllCardValues(self.getAllCards()):
            if num in seen:
                return num
            seen.add(num)

    def foldElseRaiseBB(self, bbToFold, bbToRaise):
        if self.obs.get_call_size() > bbToFold * self.obs.big_blind:  ##calls
            return 0
        else:
            return self.try_raise_bb(bbToRaise)

    def foldElseRaisePot(self, potToFold, potToRaise):
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
        handHighCard = max(self.getCardValueFromHand(0), self.getCardValueFromHand(1))

        match self.obs.get_player_count():
            case 2:
                match self.obs.get_my_hand_type():
                    case 1:

                    case 2:

                    case 3:

                    case 4:

                    case 5:

                    case 6:

                    case 7:

                    case 8:

                    case 9:

            case _:
                match self.obs.get_my_hand_type():
                    case 1:
                        if self.flush_cards_count(self.getAllCards()) == 4:  # flush
                            if self.straight_case(self.getAllCards()) != 0:  # straight
                                self.foldElseRaiseBB(6, 4)
                            else:
                                if self.highCardRank(handHighCard) == 4:
                                    self.foldElseRaiseBB(6, 4)
                                elif self.highCardRank(handHighCard) == 3:
                                    self.foldElseRaiseBB(3, 4)
                                else:
                                    return 0
                        else:
                            if self.straight_case(self.getAllCards()) != 0:  # straight
                                if self.highCardRank(handHighCard) == 4:
                                    self.foldElseRaiseBB(3, 4)
                                elif self.highCardRank(handHighCard) == 3:
                                    self.foldElseRaiseBB(2, 4)
                                else:
                                    return 0
                            else:
                                if self.highCardRank(handHighCard) == 4:
                                    self.foldElseRaiseBB(2, 4)
                    case 2:
                        if self.obs.get_board_hand_type() != 2:  # par not on table
                            if self.highCardRank(self.findPairValue()) < 3:  # par is highest card
                                if self.flush_cards_count(self.getAllCards()) == 4:  # flush
                                    if self.straight_case(self.getAllCards()) != 0:  # straight
                                        return self.try_raise_pot(1)
                                    else:
                                        return self.try_raise_pot(0.5)
                                else:
                                    if self.straight_case(self.getAllCards()) != 0:  # straight
                                        return self.try_raise_pot(0.5)
                                    else:
                                        self.foldElseRaisePot(0.5, 0.5)
                            else:
                                if self.flush_cards_count(self.getAllCards()) == 4:  # flush
                                    if self.straight_case(self.getAllCards()) != 0:  # straight
                                        if self.obs.get_call_size() > 11 * self.obs.big_blind:  ##calls
                                            return 0
                                        else:
                                            return self.try_raise_pot(0.5)
                                    else:
                                        self.foldElseRaiseBB(5, 4)
                                else:
                                    if self.straight_case(self.getAllCards()) != 0:  # straight
                                        self.foldElseRaiseBB(3, 4)
                                    else:
                                        self.foldElseRaiseBB(2, 4)
                        else:

                    case 3:

                    case 4:

                    case 5:

                    case 6:

                    case 7:

                    case 8:

                    case 9:

        print("WE IN")
        print(f"FLUSH count board: {self.flush_cards_count(boardCards)}")
        print(f"FLUSH count full: {self.flush_cards_count(self.getAllCards())}")
        print(self.straight_case(self.getAllCards()))

        if self.obs.get_player_count() == 2 or self.obs.get_player_count() == 3:
            x = 2

        return play

    def turn(self):
        print(self.straight_case(self.obs.board_cards + self.obs.my_hand))
        return self.obs.get_max_raise()  # All-in

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
