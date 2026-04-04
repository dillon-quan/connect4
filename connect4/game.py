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

        Returns:
            int: a human chosen column
        """
        while True:
            try:
                col = int(input("Enter a column (0-6): "))
                if self.board.is_valid_column(col):
                    return col
                else:
                    print(
                        "Column is either full or you have chosen an invalid column. Please enter a different column."
                    )
            except Exception as e:
                print(f"An error occurred: {e}")

    def _handle_bot_turn(self) -> int:
        """Point of entry to run minimax for the bot.

        Returns:
            int: The most optimal column from minimax
        """
        board_copy = self.board.copy()
        return self.bot.get_move(board_copy)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _determine_first_player(self) -> int:
        """Randomly select HUMAN or BOT as the first player.

        Returns:
            int: 1 for HUMAN 2 for BOT
        """
        return int(np.random.choice([HUMAN, BOT]))

    def _swap_player(self) -> None:
        """Swap the player for the next move."""
        self.current_player = HUMAN if self.current_player == BOT else BOT

    def _player_name(self, player: int) -> str:
        """Return HUMAN or BOT string depending on the given player piece

        Args:
            player (int): player checker piece value

        Returns:
            str: HUMAN if 1 otherwise BOT
        """
        return "HUMAN" if player == HUMAN else "BOT"
