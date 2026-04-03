import numpy as np

ROWS = 6
COLS = 7
EMPTY = 0
HUMAN = 1
BOT = 2


class Board:
    """Represents the Connect 4 game board and enforces game rules."""

    def __init__(self) -> None:
        self._grid: np.ndarray = np.zeros((ROWS, COLS), dtype=int)
        # Tracks the next available row index (from bottom) for each column.
        # When a column is full, the value drops below 0.
        self._col_heights: dict[int, int] = {col: ROWS - 1 for col in range(COLS)}

    @property
    def grid(self) -> np.ndarray:
        return self._grid

    # ------------------------------------------------------------------
    # Column / placement helpers
    # ------------------------------------------------------------------

    def is_valid_column(self, col: int) -> bool:
        """Return True if the column is in bounds and has at least one empty slot."""
        return 0 <= col < COLS and self._col_heights[col] >= 0

    def get_valid_columns(self) -> list[int]:
        """Return a list of all columns that can still accept a piece. Need it for Minimax."""
        return [col for col in range(COLS) if self.is_valid_column(col)]

    def get_next_open_row(self, col: int) -> int:
        """Return the row index where the next piece will land in *col*. Need it for Minimax."""
        return self._col_heights[col]

    def insert_piece(self, col: int, player: int) -> None:
        """Drop a piece for *player* into *col*, updating internal state."""
        self._grid[self._col_heights[col]][col] = player
        self._col_heights[col] -= 1

    # ------------------------------------------------------------------
    # Win / draw detection
    # ------------------------------------------------------------------

    def check_win(self, player: int) -> bool:
        """Return True if *player* has four checkers in a row."""
        return self._check_horizontal(player) or self._check_vertical(player) or self._check_diagonal(player)

    def is_draw(self) -> bool:
        """Return True if the board is completely full (no winner)."""
        return all(list(map(lambda x: x < 0, self._col_heights.values())))
        
    # ------------------------------------------------------------------
    # Private win helpers
    # ------------------------------------------------------------------

    def _check_horizontal(self, player: int) -> bool:
        """Scan every row for four consecutive pieces belonging to *player*."""
        for row in range(ROWS):
            for col in range(COLS-3):
                if (self._grid[row, col:col+4] == player).all():
                    return True
        return False

    def _check_vertical(self, player: int) -> bool:
        """Scan every column for four consecutive pieces belonging to *player*."""
        for col in range(COLS):
            for row in range(ROWS-3):
                if (self._grid[row:row+4, col] == player).all():
                    return True
        return False

    def _check_diagonal(self, player: int) -> bool:
        """Scan both diagonal directions for four consecutive pieces belonging to *player*."""
        for row in range(ROWS-3):
            for col in range(COLS-3):
                board_window = self._grid[row:row+4, col:col+4]
                if (np.diagonal(board_window) == player).all() or (np.diagonal(np.fliplr(board_window)) == player).all():
                    return True
        return False
    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def copy(self) -> "Board":
        """Return an independent deep copy of this board (used by the bot for lookahead)."""
        pass
