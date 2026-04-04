import numpy as np

ROWS = 6
COLS = 7
EMPTY = 0
HUMAN = 1
BOT = 2


class Board:
    """Represents the Connect 4 game board and enforces game rules."""

    def __init__(self, grid=None, col_heights=None) -> None:
        self._grid: np.ndarray = (
            grid if grid is not None else np.zeros((ROWS, COLS), dtype=int)
        )
        # used to track the remaining spaces left for a given column. < 0 means no remaining space
        self._col_heights: dict[int, int] = (
            col_heights
            if col_heights is not None
            else {col: ROWS - 1 for col in range(COLS)}
        )

    @property
    def grid(self) -> np.ndarray:
        return self._grid

    # ------------------------------------------------------------------
    # Column / placement helpers
    # ------------------------------------------------------------------

    def is_valid_column(self, col: int) -> bool:
        """Checks whether the col is a valid next move.

        Args:
            col (int): a chosen col by the human or bot.

        Returns:
            bool: Return True if the column is in bounds and has at least one empty slot and False otherwise.
        """
        return 0 <= col < COLS and self._col_heights[col] >= 0

    def get_valid_columns(self) -> list[int]:
        """Return a list of all columns that can still accept a piece. This method is needed for minimax when iterating through valid options.

        Returns:
            list[int]: a list of valid columns based on the current board state
        """
        return [col for col in range(COLS) if self.is_valid_column(col)]

    def insert_piece(self, col: int, player: int) -> None:
        """Drop a piece for *player* into *col*, updating internal state."""
        self._grid[self._col_heights[col]][col] = player
        self._col_heights[col] -= 1

    # ------------------------------------------------------------------
    # Win / draw detection
    # ------------------------------------------------------------------

    def check_win(self, player: int) -> bool:
        """Return True if *player* has four checkers in a row.

        Args:
            player (int): player piece

        Returns:
            bool: Return True if any of the winning conditions are met and False otherwise.
        """
        return (
            self._check_horizontal(player)
            or self._check_vertical(player)
            or self._check_diagonal(player)
        )

    def is_draw(self) -> bool:
        """Checks whether the board is full.

        Returns:
            bool: Return True if the board is completely full (no winner) and False otherwise.
        """
        return all(list(map(lambda x: x < 0, self._col_heights.values())))

    # ------------------------------------------------------------------
    # Private win helpers
    # ------------------------------------------------------------------

    def _check_horizontal(self, player: int) -> bool:
        """Scan every row for four consecutive pieces belonging to *player*.

        Args:
            player (int): player piece

        Returns:
            bool: Returns True if there is a connect4 in the horizontal direction and False otherwise.
        """
        for row in range(ROWS):
            for col in range(COLS - 3):
                if (self._grid[row, col : col + 4] == player).all():
                    return True
        return False

    def _check_vertical(self, player: int) -> bool:
        """Scan every column for four consecutive pieces belonging to *player*.

        Args:
            player (int): player piece

        Returns:
            bool: Returns True if there is a connect4 in the vertical direction and False otherwise.
        """
        for col in range(COLS):
            for row in range(ROWS - 3):
                if (self._grid[row : row + 4, col] == player).all():
                    return True
        return False

    def _check_diagonal(self, player: int) -> bool:
        """Scan both diagonal directions for four consecutive pieces belonging to *player*.

        Args:
            player (int): player piece

        Returns:
            bool: Returns True if theres a connect4 from the diagonal of the 4x4 grid and False otherwise.
        """
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                board_window = self._grid[row : row + 4, col : col + 4]
                if (np.diagonal(board_window) == player).all() or (
                    np.diagonal(np.fliplr(board_window)) == player
                ).all():
                    return True
        return False

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def copy(self) -> "Board":
        """Return an independent deep copy of this board (used by the bot during minimax algo).

        Returns:
            Board: a new instance of board with a deep copy of the board state
        """
        return Board(grid=self._grid.copy(), col_heights=self._col_heights.copy())
