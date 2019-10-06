import os

# Ascii art for each suit
suitASCII = {
    "Hearts" : [" /\\/\\ ",
                " \\  / ",
                "  \\/  ",
                "      "],
    "Spades" : ["  /\\  ",
                " /  \\ ",
                " \\__/ ",
                "  /\\  "],
    "Diamonds":["  /\\  ",
                " /  \\ ",
                " \\  / ",
                "  \\/  "],
    "Clubs"  : ["  __  ",
                " (  ) ",
                "(____)",
                "  /\\  "],
    "Hidden" : [" **** ",
                " **** ",
                " **** ",
                " **** "]
}

# General ascii for each card
cardASCII = ["+--------+",
             "|{:<2}    {:>2}|",
             "|        |",
             "|        |",
             "|        |",
             "|        |",
             "|{:<2}    {:>2}|",
             "+--------+"
]


def clearTerminal():
    # if operating system is unix-based, the "cls" command is run
    # otherwise, "clear" if run (this handles windows terminal)
    os.system('cls' if os.name == 'nt' else 'clear')


def displayBoard(player, dealer):
    clearTerminal()
    print(dealer.name + "'s Hand:\n")
    displayCards(dealer.hand)

    # determines the biggest hand being displayed
    longestLen = max(len(player.hand), len(dealer.hand))

    # prints a line of "*" as long as the biggest hand
    print("\n" + "*" * (len(cardASCII[0]) + 1)  * longestLen + "\n")
    
    displayCards(player.hand)
    print(player.name + "'s Hand:\n")


def displayCards(hand):
    outputLines = [""] * 8

    # Generate a list of all ascii to be printed
    for card in hand:
        for index, line in enumerate(asciiCardRepr(card)):
            outputLines[index] += line + " "
    
    # Prints out our generated ascii for the hand
    for line in outputLines:
        print(line)


def asciiCardRepr(card):
    # Unpack the card to a value and suit
    value, suit = card

    # Generate the ascii for one card
    outputList = [""] * 8
    for line in range(8):
        if line in [0, 1, 6, 7]:
            outputList[line] += cardASCII[line].format(value, value)
        else:
            outputList[line] += cardASCII[line][:2] + suitASCII[suit][line-2] + cardASCII[line][-2:]
    return outputList

