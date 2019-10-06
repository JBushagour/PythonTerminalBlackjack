import collections.abc

class DeckOfCards(collections.abc.MutableSequence):
    # Create the values and suits for a French deck of cards
    values = [str(num) for num in range(2, 11)] + list("JQKA")
    suits = "Hearts, Diamonds, Clubs, Spades".split(", ")

    def __init__(self):
        self.cards = [(value, suit) for value in self.values for suit in self.suits]

    def __repr__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __setitem__(self, index, newItem):
        self.cards[index] = newItem

    def __delitem__(self, index):
        del self.cards[index]

    def insert(self, index, newItem):
        self.cards.insert(index, newItem)

class Player():
    def __init__(self, hand="", name="Player"):
        self.hand = hand if hand else []
        self.name = name

    def __repr__(self):
        return self.name + "'s hand is: " + str(self.hand)

    def addCard(self, card):
        self.hand.append(card)