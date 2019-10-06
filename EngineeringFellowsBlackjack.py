import random
import time
import Cards
import terminalCards


class BlackjackPlayer(Cards.Player):
    def __init__(self, hand="", name="Player", productOfSplit=False):
        super().__init__(hand, name)

        # Initialize if the new Player is simply the "split" of an old player
        self.productOfSplit = productOfSplit

    def getHandTotal(self):
        total = 0
        aces = 0

        # Associate the cards with their corresponding values
        for card in self.hand:
            if card[0] in "2345678910":
                total += int(card[0])
            elif card[0] in "JQK":
                total += 10
            else:
                aces += 1

        # Calculates hand value with aces as whichever is more optimal: 1 or 11
        for ace in range(aces):
            total += 11 if (total + aces - ace) < 12 else 1
        return total


def main():
    # Startup message
    terminalCards.clearTerminal()
    print("-=" * 15 + " Welcome To Blackjack! " + "=-" * 15)

    # Deck and dealer created
    deck = Cards.DeckOfCards()
    dealer = BlackjackPlayer(name="The Dealer")

    # Gets number of players and names of each player
    players = getPlayers()

    # Turns will repeat until told to stop
    gameRunning = True
    while gameRunning:
        random.shuffle(deck)
        dealStarters(players + [dealer], deck)

        # Turn of blackjack runs and player either continues or stops
        gameRunning = gameTurn(players, dealer, deck)

        # Returns all cards back to the deck
        players = returnCards(players, deck)
        dealer = returnCards([dealer], deck)[0]


def returnCards(players, deck):
    # Returns card from each player
    for player in players:
        while player.hand:
            deck.append(player.hand.pop())

    # Removes any players that were just splits from other players
    return [player for player in players if not player.productOfSplit]


def getPlayers():
    # Determines the number of players
    numPlayers = ""
    while numPlayers not in "1 2 3 4".split():
        numPlayers = input("How many players? (1, 2, 3, or 4): ")

    # Gets name of each player and creates player object
    players = []
    for number in range(int(numPlayers)):
        name = input("Input your name, player " + str(number + 1) + ": ")
        players.append(BlackjackPlayer(name=name))
    return players


def gameTurn(players, dealer, deck):
    # Hide the dealer's card until the player plays
    dealerHiddenCard = dealer.hand[0]
    dealer.hand[0] = ["*", "Hidden"]

    # Each player gets a turn
    for index, player in enumerate(players):
        turnContinuing = True
        while turnContinuing:
            turnContinuing = playerTurn(players, index, dealer, deck)

    # Dealer's hand is revealed
    dealer.hand[0] = dealerHiddenCard

    # Dealer draws cards and winners are printed
    dealer.hand = dealerDraw(players, dealer, deck)
    printWinners(players, dealer)

    # Player is prompted if they want to play again
    playAgain = ""
    while playAgain not in "y n".split():
        playAgain = input("Play again? 'y' or 'n': ").lower()
    if playAgain == "y":
        return 1
    return 0


def dealerDraw(players, dealer, deck):
    # Dealer draws cards until his hand is over 16
    while True:
        terminalCards.displayBoard(players[-1], dealer)
        if dealer.getHandTotal() > 16:
            return dealer.hand
        hit(dealer, deck)
        time.sleep(0.5)


def playerTurn(players, index, dealer, deck):
    # Players, index required to be passed in case of split
    player = players[index]

    terminalCards.displayBoard(player, dealer)

    # Act according to player's choice
    playerChoice = move(player, dealer, deck)
    if playerChoice == "hit":
        hit(player, deck)
    elif playerChoice == "split":

        # Create a temperary new player if the player splits
        splitInfo ={"hand": [player.hand.pop()],
                    "name": player.name + " #2",
                    "productOfSplit": True
                    }
        players.insert(index + 1, BlackjackPlayer(**splitInfo))
    else:
        # Either a stand or a bust, the turn stops now
        return False
    # The turn will repeat if the player hits or splits
    return True


def printWinners(players, dealer):
    print("The dealer's hand value was", dealer.getHandTotal())
    for player in players:
        # Compares players hands to dealer, sees who won
        print(player.name + "'s hand value was", player.getHandTotal(), end=": ")
        print(winner(dealer, player) + "!")

        # Delay just to make it more readable
        time.sleep(0.5)


def winner(player1, player2):
    # If a player busts, they automatically lose no matter what the dealer does
    player1Value = player1.getHandTotal() if player1.getHandTotal() < 22 else 1
    player2Value = player2.getHandTotal() if player2.getHandTotal() < 22 else 0

    # Prints out who won out of the two players
    if player1Value > player2Value:
        return player1.name + " beat " + player2.name
    elif player2Value > player1Value:
        return player2.name + " beat " + player1.name
    else:
        return "It was a tie"


def move(player, dealer, deck):
    # Checks to see if player has busted, if so it stops
    if player.getHandTotal() > 21:
        print("Bust! Your hand is over 21.")
        time.sleep(3)
        return "Bust"

    # If, on their first turn they're dealt a double, they can split as well as hit/stand
    allowedMoves = ["hit", "stand"]
    if (len(player.hand) + len(player.hand[0]) == 4 and
            player.hand[0][0] == player.hand[1][0]):
        allowedMoves.append("split")

    # Prompt user until they enter a valid input
    move = '#'
    while move not in allowedMoves:
        move = input(player.name + ", do you " + " or ".join(allowedMoves) + "?: ").lower()
    return move


def dealStarters(players, deck):
    # adds 2 cards to each players hand
    for player in players:
        hit(player, deck, 2)


def hit(player, deck, numTimes=1):
    # adds a card to a player's hand
    for _ in range(numTimes):
        player.addCard(deck.pop())


if __name__ == "__main__":
    main()
