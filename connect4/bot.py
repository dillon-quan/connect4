from typing import Optional

import numpy as np

from connect4.board import Board, HUMAN, BOT, EMPTY, ROWS, COLS

# Score constants used by the heuristic
_WIN_SCORE = 100_000
_THREE_SCORE = 10
_TWO_SCORE = 2
_CENTER_BONUS = 3


class Bot:
    """Heuristic-based Connect 4 bot using minimax with alpha-beta pruning.

    Design notes
    ------------
    - ``depth`` controls the minimax search depth.  Depth 4 gives
      a strong casual opponent without noticeable latency.
    - ``_score_window`` assigns local scores to every window of 4 cells,
      which ``_score_position`` aggregates across all rows, columns, and
      diagonals to produce a single board evaluation.
    - The bot favours the centre column because centre control gives the
      most winning threats in Connect 4.
    """

    def __init__(self, depth: int = 4) -> None:
        self.depth = depth

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_move(self, board: Board) -> int:
        """Return the column index of the best move for the bot.

        Uses minimax with alpha-beta pruning up to based on the set depth.

        Args:
            board (Board): the current board

        Returns:
            int: the column from minimax
        """
        col = self._minimax(
            board=board, depth=self.depth, alpha=-np.inf, beta=np.inf, maximizing=True
        )[0]

        # depth=0 skips move selection entirely and returns None for the column.
        # Fall back to picking the valid column with the highest heuristic score.
        if col is None:
            col = max(
                board.get_valid_columns(),
                key=lambda c: self._score_after(board, c),
            )
        return col

    def _score_after(self, board: Board, col: int) -> float:
        """Return the heuristic score of board after dropping a BOT piece in col.
        This is for when depth=0.

        Args:
            board (Board): board instance with the current state
            col (int): chosen column for placement

        Returns:
            float: the score after insertion
        """
        copy = board.copy()
        copy.insert_piece(col, BOT)
        return self._score_position(copy)

    # ------------------------------------------------------------------
    # Minimax
    # ------------------------------------------------------------------

    def _minimax(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> tuple[Optional[int], float]:
        """Minimax search with alpha-beta pruning.
        A branch is pruned with alpha >= beta.

        Args:
            board (Board): current board state.
            depth (int): remaining search depth.
            alpha (float): value to keep track to determine to prune branches, initialize to -inf
            beta (float): value to keep track to determine to prune branches, initialize to inf
            maximizing (bool): True when it is the bot's turn to move and False when its the human turn.

        Returns:
            tuple[Optional[int], float]: (best_column, best_score)
        """

        # --- Terminal nodes ---
        if board.is_draw():
            return None, 0

        if board.check_win(BOT):
            return None, _WIN_SCORE

        if board.check_win(HUMAN):
            return None, -_WIN_SCORE

        if depth == 0:
            return None, self._score_position(board)

        # --- Recursive case ---
        valid_columns = board.get_valid_columns()

        # bot's turn
        if maximizing:
            best_score = -np.inf
            best_col = None

            for col in valid_columns:
                board_copy = board.copy()
                board_copy.insert_piece(col, BOT)
                _, score = self._minimax(
                    board=board_copy,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    maximizing=False,
                )

                if score > best_score:
                    best_score = score
                    best_col = col

                alpha = max(alpha, best_score)

                if alpha >= beta:
                    break
            return best_col, best_score
        # human's turn
        else:
            best_score = np.inf
            best_col = None

            for col in valid_columns:
                board_copy = board.copy()
                board_copy.insert_piece(col, HUMAN)
                _, score = self._minimax(
                    board=board_copy,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    maximizing=True,
                )

                if score < best_score:
                    best_score = score
                    best_col = col

                beta = min(beta, best_score)

                if alpha >= beta:
                    break
            return best_col, best_score

    # ------------------------------------------------------------------
    # Heuristic evaluation
    # ------------------------------------------------------------------

    def _score_position(self, board: Board) -> float:
        """Return a heuristic score of *board* from the bot's perspective.

        Positive values favour the bot; negative values favour the human.
        Evaluation considers:
          - Centre column occupancy (positional advantage)
          - All horizontal, vertical, and diagonal windows of length 4

        Args:
            board (Board): the board instance

        Returns:
            float: the total score of the board state
        """
        score = 0.0
        grid = board.grid

        # Centre column bonus: pieces in the centre column participate in more
        # potential winning lines than any other column, so reward occupancy.
        center_col = grid[:, COLS // 2].tolist()
        score += center_col.count(BOT) * _CENTER_BONUS

        # Horizontal windows
        for row in range(ROWS):
            for col in range(COLS - 3):
                window = grid[row, col : col + 4].tolist()
                score += self._score_window(window)

        # Vertical windows
        for col in range(COLS):
            for row in range(ROWS - 3):
                window = grid[row : row + 4, col].tolist()
                score += self._score_window(window)

        # Diagonal windows — mirrors _check_diagonal: extract each 4×4 subgrid
        # and score both its main diagonal (↘) and its flipped diagonal (↗).
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                subgrid = grid[row : row + 4, col : col + 4]
                score += self._score_window(np.diagonal(subgrid).tolist())
                score += self._score_window(np.diagonal(np.fliplr(subgrid)).tolist())

        return score

    def _score_window(self, window: list[int]) -> float:
        """Score a single window of 4 cells.

        Scoring rules (bot-centric):
          - 4 bot pieces            → +WIN_SCORE
          - 3 bot pieces + 1 empty  → +THREE_SCORE
          - 2 bot pieces + 2 empty  → +TWO_SCORE
          - 3 human pieces + 1 empty → -THREE_SCORE  (blocking threat)

        Mixed windows (both players present) score 0 — neither side can
        complete a four-in-a-row through that window.

        Args:
            window (list[int]): a list of length 4 with player piece values
            (i.e [1, 0, 1, 1])

        Returns:
            float: a score based on the placement of the pieces in the window
        """
        bot_count = window.count(BOT)
        human_count = window.count(HUMAN)
        empty_count = window.count(EMPTY)

        if bot_count == 4:
            return _WIN_SCORE
        if bot_count == 3 and empty_count == 1:
            return _THREE_SCORE
        if bot_count == 2 and empty_count == 2:
            return _TWO_SCORE
        if human_count == 3 and empty_count == 1:
            return -_THREE_SCORE
        if human_count == 2 and empty_count == 2:
            return -_TWO_SCORE

        return 0.0
