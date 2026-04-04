import numpy as np

from connect4.board import Board, HUMAN, BOT
from connect4.bot import Bot
from connect4.display import (
    print_board,
    print_welcome,
    print_turn,
    print_winner,
    print_draw,
)


class Game:
    """Orchestrates a single Connect 4 session between a human and the bot.

    Responsibilities
    ----------------
    - Initialise the board and bot.
    - Randomly decide who moves first.
    - Drive the turn loop to perform the following actions:
      - determine current player
      - prompt human/bot for column choice
      - insert piece into board
      - win/draw check
      - swap player
    - Delegate rendering entirely to display.py.
    """

    def __init__(self) -> None:
        self.board = Board()
        self.bot = Bot()
        self.current_player: int = self._determine_first_player()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start and run the game loop until a win or draw occurs."""
        print_welcome()
        print_board(self.board.grid)

        while True:
            player_name = self._player_name(self.current_player)
            print_turn(player_name)

            if self.current_player == HUMAN:
                col = self._handle_human_turn()
            else:
                col = self._handle_bot_turn()

            self.board.insert_piece(col, self.current_player)
            print_board(self.board.grid)

            if self.board.check_win(self.current_player):
                print_winner(player_name)
                break

            if self.board.is_draw():
                print_draw()
                break

            self._swap_player()

    # ------------------------------------------------------------------
    # Turn handlers
    # ------------------------------------------------------------------

    def _handle_human_turn(self) -> int:
        """Prompt the human for a column, validate the choice, and return it.

        Keeps prompting until a valid column is entered.
        """
        while True:
            try:
                col = int(input("Enter a column (0-6): "))
                if self.board.is_valid_column(col):
                    return col
                else:
                    print("Column is full. Please enter a different column.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 6.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def _handle_bot_turn(self) -> int:
        """Ask the bot for its chosen column and return it."""
        board_copy = self.board.copy()
        return self.bot.get_move(board_copy)

        # while True:
        #     try:
        #         col = int(input("Enter a column (0-6): "))
        #         if self.board.is_valid_column(col):
        #             return col
        #         else:
        #             print("Column is full. Please enter a different column.")
        #     except ValueError:
        #         print("Invalid input. Please enter a number between 0 and 6.")
        #     except Exception as e:
        #         print(f"An error occurred: {e}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _determine_first_player(self) -> int:
        """Randomly select HUMAN or BOT as the first player."""
        return int(np.random.choice([HUMAN, BOT]))

    def _swap_player(self) -> None:
        self.current_player = HUMAN if self.current_player == BOT else BOT

    def _player_name(self, player: int) -> str:
        return "HUMAN" if player == HUMAN else "BOT"
