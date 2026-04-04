import numpy as np

# ANSI color codes
_YELLOW = "\033[0;37;43m"  # human pieces
_RED = "\033[0;37;41m"  # bot pieces
_BLUE = "\033[0;32;44m"  # empty cells / header
_RESET = "\033[0m"


def print_board(grid: np.ndarray) -> None:
    """Render the board to stdout with ANSI color-coded pieces.

    Adapted from the original main.py implementation:
      - 0  → empty (blue background)
      - 1  → human piece (yellow background)
      - 2  → bot piece (red background)

    Args:
        grid (np.ndarray): the current board state of the game
    """
    print(f"{_BLUE} 0  1  2  3  4  5  6 {_RESET}")
    for row in grid:
        row_str = ""
        for cell in row:
            if cell == 1:
                row_str += f"{_YELLOW} 1 "
            elif cell == 2:
                row_str += f"{_RED} 2 "
            else:
                row_str += f"{_BLUE}   "
        print(row_str + _RESET)


def print_welcome() -> None:
    """Print an introductory message when the game starts."""
    print("Welcome to Connect 4!")


def print_turn(player_name: str) -> None:
    """Announce whose turn it is.

    Args:
        player_name (str): HUMAN or BOT
    """
    print(f"{player_name}'s turn")


def print_winner(player_name: str) -> None:
    """Announce the winner at the end of the game.

    Args:
        player_name (str): HUMAN or BOT
    """
    print(f"{player_name} wins!")


def print_draw() -> None:
    """Announce a draw when the board is full with no winner."""
    print("It's a draw!")
