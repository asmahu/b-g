from random import randint
import sys

scores = {'CPU': 0, 'player': 0}


# Board class adopted and modified from the CI's battleship tutorial
class Board:

    """
    Main board class. Sets board size, the number of ships,
     the player's name and the board type (player board or CPU).
     Has methods for adding ships and guesses and printing the board
    """

    def __init__(self, size, number_ships, name, type):
        self.size = size
        self.board = [["." for x in range(size)] for y in range(size)]
        self.number_ships = number_ships
        self.name = name
        self.type = type
        self.guesses = []
        self.ships = []

    def print(self):
        # prints board
        for row in self.board:
            print("  ".join(row))

    def guess(self, x, y):
        # adds "X" at the chosen coordinates
        self.board[x][y] = "X"

        # adds "*" if chosen coordinates hits a target
        if (x, y) in self.ships:
            self.board[x][y] = "*"
            return "Hit"
        else:
            return "Miss"

    def add_ship(self, x, y, type="CPU"):
        if len(self.ships) >= self.number_ships:
            print("Error: you cannot add any more ships!")
        else:
            self.ships.append((x, y))
            if self.type == "player":
                self.board[x][y] = "@"


def random_point(size):

    """
    Helper function to return a random integer between o and size
    """
    return randint(0, size - 1)


def validate_coordinates(x, y, board):

    """
    Function to validate coordinate inputs from users
    """

    try:
        x, y = int(x), int(y)
        board.board[x][y] in board.board

    except IndexError:
        print(f"Invalid data: row and column\
must be an integer between 0 - {board.size - 1}\n")
        return False

    except ValueError:
        print(f"Invalid data: sorry, you can only enter integer numbers.\n")
        return False

    finally:
        if (x, y) in board.guesses:
            print("!!! Boat does not fit. please input different coordiante\n")
            return False
    return True


def setup_board(board):

    """
    Function to add ships to the board's ships list
    """

    x = random_point(board.size)
    y = random_point(board.size)
    board.add_ship(x, y)


def make_guess(board):

    """
    Function to get validated user guess and add it to the guesses list
    """

    while True:
        if board.type == "CPU":
            x, y = random_point(board.size), random_point(board.size)
            if validate_coordinates(x, y, board):
                board.guesses.append((x, y))
                return x, y
                break

        elif board.type == "player":
            x = input("Guess a row: ")
            y = input("Guess a column: ")
            if validate_coordinates(x, y, board):
                board.guesses.append((x, y))
                return x, y
                break


def scores_dashboard(board):

    """
    Prints the score dashboard status after each round
    """

    print("-" * 35)
    print("After this round, the scores are:")
    print(f"{board.name}: {scores['player']} CPU: {scores['CPU']}")
    ################################################### MOMKIN QLALAT
    print("-" * 35)


def print_board(CPU_board, plyr_board):

    """
    Prints the player's board and the CPU's board
    """

    print(f"{plyr_board.name}'s Board:")
    plyr_board.print()
    print()
    print("CPU's Board:")
    CPU_board.print()
    print("-" * 35)


def check_winner(scores, CPU_board, plyr_board):

    """
    Function that checks the winner and displays the winning message
    """

    if scores["player"] == plyr_board.number_ships:
        print("GAME OVER!!")
        print(f"Well done {plyr_board.name}!! You are the Victor")
    elif scores['CPU'] == plyr_board.number_ships:
        print("GAME OVER!!")
        print(f"Sorry, {plyr_board.name}!! You lost to the CPU")


def play_game(CPU_board, plyr_board):

    """
    Main game function. Takes in the board instances as arguement
    and controls the game logic"""

    while True:
        # Get the player's guess and setup CPU's board
        x, y = make_guess(plyr_board)
        x, y = int(x), int(y)
        plyr_board.guesses.append((x, y))
        print(f"Player guessed: {x, y}")
        if CPU_board.guess(x, y) == "Hit":
            print("Player got a hit!")
            scores['player'] += 1
        elif CPU_board.guess(x, y) == "Miss":
            print("This time player missed")

        # Get CPU's guess and setup player's board
        x, y = make_guess(CPU_board)
        CPU_board.guesses.append((x, y))
        print(f"CPU guessed: {x, y}")
        if plyr_board.guess(int(x), int(y)) == "Hit":
            print("CPU got a hit!")
            scores["CPU"] += 1
        elif plyr_board.guess(x, y) == "Miss":
            print("This time CPU missed")

        scores_dashboard(plyr_board)
        print_board(CPU_board, plyr_board)
        check_winner(scores, CPU_board, plyr_board)

        # Get user's feedback to continue or to quit
        player_selection = input("Enter 'l' to left, 'n' for new game and \
any key to continue: ")

        if player_selection.lower() == "n":
            new_game()
        elif player_selection.lower() == "l":
            sys.exit("You have left the game")


def new_game():

    """
    Starts a new game. Sets the board size and number of ships, resets the
    scores and initialises the boards.
    """

    print()
    print("The board size must be integers between 3 and 10\n")

    # Get the size of board from the player and validate it
    while True:
        try:
            size = int(input("Choose the board size: "))
            if size >= 3 and size <= 10:
                break
        except ValueError:
            print("The board size must be an integer number\n")
        else:
            print("Out of bound: choose an integer between 3 and 10\n")

    print()
    print("The number of ships must be integers between 3 and 10\n")

    # Get the number of ships from the user and validate it
    while True:
        try:
            number_ships = int(input("Choose the number of ships: "))
            if number_ships >= 3 and number_ships <= 10:
                break
        except ValueError:
            print("The number of ships must be integer number\n")
        else:
            print("Out of bound: choose an integer between 3 and 10\n")

    scores["CPU"] = 0
    scores["player"] = 0
    print("-" * 37)
    print("Welcome to the ULTIMATE BATTLESHIPS!!")
    print("You will be playing against CPU")
    print("In this battleship game player's take turns guessing by calling 
    out the coordiantes. The opponent responds with "hit" or "miss"/n")
    print(f"Board Size: {size}. Number of Ships: {number_ships}")
    print("Top left corner is row: 0, col: 0")
    print("-" * 37)

    # Get the player's name
    while True:
        player_name = input('Please input your name: ').capitalize()
        if player_name.isalpha():
            print()
            break
        else:
            print("Invalid entry: players name must be an alphabet")

    # Get board instances
    CPU_board = Board(size, number_ships, "CPU", type="CPU")
    plyr_board = Board(size, number_ships, player_name, type="player")

    # Add ships to the board instances
    for _ in range(number_ships):
        setup_board(plyr_board)
        setup_board(CPU_board)
    print("-" * 35)
    print_board(CPU_board, plyr_board)
    play_game(CPU_board, plyr_board)

    
new_game()