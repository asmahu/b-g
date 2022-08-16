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

    def __init__(self, size, num_ships, name, type):
        self.size = size
        self.board = [["." for x in range(size)] for y in range(size)]
        self.num_ships = num_ships
        self.name = name
        self.type = type
        self.guesses = []
        self.ships = []

    def print(self):
        # prints board
        for row in self.board:
            print("  ".join(row))

    def guess(self, x, y):
        # appends "X" at the chosen coordinates
        self.board[x][y] = "X"

        # appends "*" if chosen coordinates hits a target
        if (x, y) in self.ships:
            self.board[x][y] = "*"
            return "Hit"
        else:
            return "Miss"

    def add_ship(self, x, y, type="CPU"):
        if len(self.ships) >= self.num_ships:
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
            print("You cannot guess the same coordinates twice!\n")
            return False
    return True


def populate_board(board):

    """
    Function to add ships to the board's ships list
    """

    x = random_point(board.size)
    y = random_point(board.size)
    board.add_ship(x, y)


def make_guess(board):

    """
    Function to get validated user guess and append it to the guesses list
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
    print("-" * 35)


def print_board(CPU_board, player_board):

    """
    Prints the player's board and the CPU's board
    """

    print(f"{player_board.name}'s Board:")
    player_board.print()
    print()
    print("CPU's Board:")
    CPU_board.print()
    print("-" * 35)


def check_winner(scores, CPU_board, player_board):

    """
    Function that checks the winner and displays the winning message
    """

    if scores["player"] == player_board.num_ships:
        print("GAME OVER!!")
        print(f"Well done {player_board.name}!! You are the Victor")
    elif scores['CPU'] == player_board.num_ships:
        print("GAME OVER!!")
        print(f"Sorry, {player_board.name}!! You lost to the CPU")


def play_game(CPU_board, player_board):

    """
    Main game function. Takes in the board instances as arguement
    and controls the game logic"""

    while True:
        # Get the player's guess and populate CPU's board
        x, y = make_guess(player_board)
        x, y = int(x), int(y)
        player_board.guesses.append((x, y))
        print(f"Player guessed: {x, y}")
        if CPU_board.guess(x, y) == "Hit":
            print("Player got a hit!")
            scores['player'] += 1
        elif CPU_board.guess(x, y) == "Miss":
            print("Player missed this time")

        # Get CPU's guess and populate player's board
        x, y = make_guess(CPU_board)
        CPU_board.guesses.append((x, y))
        print(f"CPU guessed: {x, y}")
        if player_board.guess(int(x), int(y)) == "Hit":
            print("CPU got a hit!")
            scores["CPU"] += 1
        elif player_board.guess(x, y) == "Miss":
            print("CPU missed this time")

        scores_dashboard(player_board)
        print_board(CPU_board, player_board)
        check_winner(scores, CPU_board, player_board)

        # Get user's feedback to continue or to quit
        player_choice = input("Enter 'e' to quit, 'n' for new game and \
any key to continue: ")

        if player_choice.lower() == "n":
            new_game()
        elif player_choice.lower() == "e":
            sys.exit("You have quit the game")


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
            num_ships = int(input("Choose the number of ships: "))
            if num_ships >= 3 and num_ships <= 10:
                break
        except ValueError:
            print("The number of ships must be integer number\n")
        else:
            print("Out of bound: choose an integer between 3 and 10\n")

    scores["CPU"] = 0
    scores["player"] = 0
    print("-" * 37)
    print("Welcome to the ULTIMATE BATTLESHIPS!!")
    print(f"Board Size: {size}. Number of Ships: {num_ships}")
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
    CPU_board = Board(size, num_ships, "CPU", type="CPU")
    player_board = Board(size, num_ships, player_name, type="player")

    # Append ships to the board instances
    for _ in range(num_ships):
        populate_board(player_board)
        populate_board(CPU_board)
    print("-" * 35)
    print_board(CPU_board, player_board)
    play_game(CPU_board, player_board)


new_game()