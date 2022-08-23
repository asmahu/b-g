### THIS IS PART OF CODEINSTITUTE CODING CHALLANGE 
### BATTLESHIP WITH PYTHON3 (PLAYER VS CPU)
from random import randint
import sys

scores = {'CPU': 0, 'player': 0}


# Board class adopted and modified from the CI's battleship tutorial
class Board:

    """
    Main board class. to set board size, the number of ships,
     the player's name and the player board or CPU
     contains methods to add ships, guesses and to print the board
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
        # adds "x" at the selected coordinates
        self.board[x][y] = "x"

        # adds "*" if selected coordinates hits a target
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
                self.board[x][y] = "#"


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
        print(f"Invalid input: row and column\
must be an integer between 0 - {board.size - 1}\n")
        return False

    except ValueError:
        print(f"Invalid input: sorry, only integer numbers are allowed.\n")
        return False

    finally:
        if (x, y) in board.guesses:
            print("Boat does not fit. please input different coordinates!!!\n")
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
    Function to get validated player guess and add it to the guesses list
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


def scores_Area(board):

    """
    Prints the score dashboard status after each round
    """

    print("~" * 35)
    print("After this round, the scores are:")
    print(f"{board.name}: {scores['player']} CPU: {scores['CPU']}")
    print("~" * 35)


def print_board(CPU_board, player_board):

    """
    Prints the player's board and the CPU's board
    """

    print(f"{player_board.name}'s Board:")
    player_board.print()
    print()
    print("CPU's Board:")
    CPU_board.print()
    print("~" * 35)


def winner(scores, CPU_board, player_board):

    """
    function to check who wins and display the result message
    """

    if scores["player"] == player_board.number_ships:
        print("GAME OVER!!")
        print(f"Well done {player_board.name}!! You are the winner")
    elif scores['CPU'] == player_board.number_ships:
        print("GAME OVER!!")
        print(f"Sorry, {player_board.name}!! You lost to the CPU")


def play_game(CPU_board, player_board):

    """
    Function to start playing game 
    """

    while True:
        # Get the player's guess and setup CPU's board
        x, y = make_guess(player_board)
        x, y = int(x), int(y)
        player_board.guesses.append((x, y))
        print(f"Player guessed: {x, y}")
        if CPU_board.guess(x, y) == "Hit":
            print("PLAYER HIT!")
            scores['player'] += 1
        elif CPU_board.guess(x, y) == "Miss":
            print("Player missed this time")

        # Get CPU's guess and setup player's board
        x, y = make_guess(CPU_board)
        CPU_board.guesses.append((x, y))
        print(f"CPU guessed: {x, y}")
        if player_board.guess(int(x), int(y)) == "Hit":
            print("The CPU HIT!")
            scores["CPU"] += 1
        elif player_board.guess(x, y) == "Miss":
            print("CPU missed this time")

        scores_Area(player_board)
        print_board(CPU_board, player_board)
        winner(scores, CPU_board, player_board)

        # Get user's feedback to continue or to quit
        player_selection = input("Enter 'l' to leave, 'n' for starting new game and \
any key to continue: ")

        if player_selection.lower() == "n":
            new_game()
        elif player_selection.lower() == "l":
            sys.exit("You have quit the game")


def new_game():

    """
    Starts a new game. Sets the board size and number of ships, resets the
    scores and initialises the boards.
    """

    print()
    print(
        """
___  ____ ___ ___ _    ____ ____ _  _ _ ___  ____
|__] |__|  |   |  |    |___ [__  |__| | |__] [__
|__] |  |  |   |  |___ |___ ___] |  | | |    ___]\n
"""
    )
    print("WELCOME TO THIS ULTIMATE BATTLESHIP GAME!!!\n")
    print("You are going to play against CPU\n")
    print("Introduction:\n")
    print("I. Input board size. it must be between 4 - 12\n")
    print("II. Input number of ships between 4 - 12\n")
    print("III. Input your name to dispay on screen only characters can be used\n")
    print("IV. Guess a row and column to hit CPU's ships.\n")
    print("GOOD LUCK!!!\n")
    print("The board size must be integers between 4 and 12\n")

    # Get the size of board from the player and validate it
    while True:
        try:
            size = int(input("Select the board size: "))
            if size >= 4 and size <= 12:
                break
        except ValueError:
            print("The board size must be an integer number\n")
        else:
            print("Out of range: Select an integer between 4 and 12\n")

    print()
    print("The number of ships must be integers between 4 and 12\n")

    # Get the number of ships from the user and validate it
    while True:
        try:
            number_ships = int(input("Seleect the number of ships: "))
            if number_ships >= 4 and number_ships <= 12:
                break
        except ValueError:
            print("The number of ships must be integer number\n")
        else:
            print("Out of range: Select an integer between 4 and 12\n")

    scores["CPU"] = 0
    scores["player"] = 0
    print("~" * 37)
    print(f"Board Size: {size}. Number of Ships: {number_ships}")
    print("Top left corner is row: 0, col: 0")
    print("~" * 37)

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
    player_board = Board(size, number_ships, player_name, type="player")

    # Add ships to the board instances
    for _ in range(number_ships):
        setup_board(player_board)
        setup_board(CPU_board)
    print("~" * 35)
    print_board(CPU_board, player_board)
    play_game(CPU_board, player_board)


new_game()