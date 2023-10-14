"""
Created on Sun 17 Jul 11:26 2022
Finished on
@author: Cpt.Ender

https://www.codewars.com/kata/5739174624fc28e188000465/train/python

A famous casino is suddenly faced with a sharp decline of their revenues.
They decide to offer Texas hold'em also online.
Can you help them by writing an algorithm that can rank poker hands?

Task
Create a poker hand that has a method to compare itself to another poker hand:

compare_with(self, other_hand)
A poker hand has a constructor that accepts a string containing 5 cards:

PokerHand("KS 2H 5C JD TD")
The characteristics of the string of cards are:

Each card consists of two characters, where
The first character is the value of the card: 2, 3, 4, 5, 6, 7, 8, 9, T(en), J(ack), Q(queen), K(ing), A(ce)
The second character represents the suit: S(spades), H(hearts), D(diamonds), C(clubs)
A space is used as card separator between cards
The result of your poker hand compare can be one of these 3 options:

[ "Win", "Tie", "Loss" ]
Notes
Apply the Texas Hold'em rules for ranking the cards.
Low aces are NOT valid in this kata.
There is no ranking for the suits.
If you finished this kata, you might want to continue with Sortable Poker Hands
                                                                                """


class PokerHand:
    # Pair: 2point, 2Pair: 4points, 3ofKind: 4.5points, Straight: 5points
    # Flush: 6points, FullHouse: 6.5points, 4ofKind: 7, StraightFlush: (5+6)points
    def __init__(self, hand):
        self.result = ["Loss", "Tie", "Win"]
        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                       '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        self.hand = hand

        self.value = self.handValue(self.hand)

    def compare_with(self, other):
        return self.result[(self.value > other.value) - (self.value < other.value) + 1]

    def handValue(self, hand):
        temp = hand.split(' ')
        highest = 0
        hand = [[], []]
        for i, card in enumerate(temp):
            temp[i] = [self.values[card[0]], card[1]]
            hand[0].append(temp[i][0])
            hand[1].append(temp[i][1])
            if temp[i][0] > highest:
                highest = temp[i][0]
        hand[0].sort()
        NofKindDict = self.nOfKind(hand)
        ls = list(NofKindDict.values())
        nOfKindValue = ls.count(4) * 7 + ls.count(3) * 4.5 + ls.count(2) * 2
        if nOfKindValue or len(ls) == 5:
            sortedNofKindDict = sorted(NofKindDict, key=NofKindDict.get)[::-1]
            highest = sum([v / 10 ** (2 * i) for i, v in enumerate(sortedNofKindDict)])
        value = (nOfKindValue + self.straight(hand) + self.flush(hand)) * 100 + highest
        return value

    @staticmethod
    def nOfKind(hand):
        tempDict = dict.fromkeys(hand[0])
        for key in tempDict.keys():
            tempDict[key] = hand[0].count(key)
        return tempDict

    @staticmethod
    def straight(hand):
        # Five cards in increasing order
        for i in range(len(hand[0]) - 1):
            if hand[0][i + 1] != hand[0][i] + 1:
                return 0
        return 5

    @staticmethod
    def flush(hand: list):
        # Five cards of the same suit
        for i in range(len(hand[1]) - 1):
            if hand[1][i] != hand[1][i + 1]:
                return 0
        return 6


pokerH = PokerHand("8S JH QH KS AC")
# print(pokerH.compare_with(PokerHand("KS AS QS JS TS")))  # Straight + flush + highest
# print(pokerH.compare_with(PokerHand("7H 3H 4H 5H 6H")))
# print(pokerH.compare_with(PokerHand("2H 3H 4H 5H 6H")))
# print(pokerH.compare_with(PokerHand("AS AH KH AD AC"))) # 4 of a Kind
# print(pokerH.compare_with(PokerHand("AS AH QH AD AC")))
# print(pokerH.compare_with(PokerHand("AS AH JH AD AC")))
# print(pokerH.compare_with(PokerHand("KS AH KH AS AC")))  # Full House
# print(pokerH.compare_with(PokerHand("QH AS AH AD QC")))
# print(pokerH.compare_with(PokerHand("JH AS AH AD JC")))
# print(pokerH.compare_with(PokerHand("AH AC 2H 3H AS")))  # 3 of a Kind
# print(pokerH.compare_with(PokerHand("KH KC QH JH KS")))
# print(pokerH.compare_with(PokerHand("KH KC QH TH KS")))
# print(pokerH.compare_with(PokerHand("AS AH KH QS KC")))  # 2 Pairs
# print(pokerH.compare_with(PokerHand("AS AH KH KS JC")))
# print(pokerH.compare_with(PokerHand("AS AH KH KS TC")))
# print(pokerH.compare_with(PokerHand("AH AC KH JH QS")))  # Pair
# print(pokerH.compare_with(PokerHand("AH AC KH TH QS")))
# print(pokerH.compare_with(PokerHand("AH AC KH 9H QS")))
print(pokerH.compare_with(PokerHand("9S JH QH KS AC")))  # Highest Card
print(pokerH.compare_with(PokerHand("8S JH QH KS AC")))
print(pokerH.compare_with(PokerHand("7S JH QH KS AC")))
