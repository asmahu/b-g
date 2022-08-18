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
        self.board = [["." for a in range(size)] for b in range(size)]
        self.number_ships = number_ships
        self.name = name
        self.type = type
        self.guesses = []
        self.ships = []

    def print(self):
        # prints board
        for row in self.board:
            print("  ".join(row))

    def guess(self, a, b):
        # adds "a" at the selected coordinates
        self.board[a][b] = "a"

        # adds "*" if selected coordinates hits a target
        if (a, b) in self.ships:
            self.board[a][b] = "*"
            return "Hit"
        else:
            return "Miss"

    def add_ship(self, a, b, type="CPU"):
        if len(self.ships) >= self.number_ships:
            print("Error: you cannot add any more ships!")
        else:
            self.ships.append((a, b))
            if self.type == "player":
                self.board[a][b] = "@"


def random_point(size):

    """
    Helper function to return a random integer between o and size
    """
    return randint(0, size - 1)


def validate_coordinates(a, b, board):

    """
    Function to validate coordinate inputs from users
    """

    try:
        a, b = int(a), int(b)
        board.board[a][b] in board.board

    except IndexError:
        print(f"Invalid input: row and column\
must be an integer between 0 - {board.size - 1}\n")
        return False

    except ValueError:
        print(f"Invalid input: sorry, only integer numbers are allowed.\n")
        return False

    finally:
        if (a, b) in board.guesses:
            print("Boat does not fit. please input different coordinates!!!\n")
            return False
    return True


def populate_board(board):

    """
    Function to add ships to the board's ships list
    """

    a = random_point(board.size)
    b = random_point(board.size)
    board.add_ship(a, b)


def make_guess(board):

    """
    Function to get validated player guess and add it to the guesses list
    """

    while True:
        if board.type == "CPU":
            a, b = random_point(board.size), random_point(board.size)
            if validate_coordinates(a, b, board):
                board.guesses.append((a, b))
                return a, b
                break

        elif board.type == "player":
            a = input("Guess a row: ")
            b = input("Guess a column: ")
            if validate_coordinates(a, b, board):
                board.guesses.append((a, b))
                return a, b
                break


def scores_Area(board):

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
        # Get the player's guess and populate CPU's board
        a, b = make_guess(player_board)
        a, b = int(a), int(b)
        player_board.guesses.append((a, b))
        print(f"Player guessed: {a, b}")
        if CPU_board.guess(a, b) == "Hit":
            print("Player got a hit!")
            scores['player'] += 1
        elif CPU_board.guess(a, b) == "Miss":
            print("Player missed this time")

        # Get CPU's guess and setup player's board
        a, b = make_guess(CPU_board)
        CPU_board.guesses.append((a, b))
        print(f"CPU guessed: {a, b}")
        if player_board.guess(int(a), int(b)) == "Hit":
            print("CPU got a hit!")
            scores["CPU"] += 1
        elif player_board.guess(a, b) == "Miss":
            print("CPU missed this time")

        scores_Area(player_board)
        print_board(CPU_board, player_board)
        winner(scores, CPU_board, player_board)

        # Get user's feedback to continue or to quit
        player_selection = input("Enter 'e' to quit, 'n' for new game and \
any key to continue: ")

        if player_selection.lower() == "n":
            new_game()
        elif player_selection.lower() == "e":
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
            size = int(input("Select the board size: "))
            if size >= 3 and size <= 10:
                break
        except ValueError:
            print("The board size must be an integer number\n")
        else:
            print("Out of range: Select an integer between 3 and 10\n")

    print()
    print("The number of ships must be integers between 3 and 10\n")

    # Get the number of ships from the user and validate it
    while True:
        try:
            number_ships = int(input("Seleect the number of ships: "))
            if number_ships >= 3 and number_ships <= 10:
                break
        except ValueError:
            print("The number of ships must be integer number\n")
        else:
            print("Out of range: Select an integer between 3 and 10\n")

    scores["CPU"] = 0
    scores["player"] = 0
    print("-" * 37)
    print("Welcome to the ULTIMATE BATTLESHIPS!!")
    print("You will be playing against CPU")
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
    player_board = Board(size, number_ships, player_name, type="player")

    # Add ships to the board instances
    for _ in range(number_ships):
        populate_board(player_board)
        populate_board(CPU_board)
    print("-" * 35)
    print_board(CPU_board, player_board)
    play_game(CPU_board, player_board)


new_game()