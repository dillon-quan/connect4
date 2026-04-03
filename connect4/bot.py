from __future__ import annotations
from typing import Optional

from connect4.board import Board, HUMAN, BOT, EMPTY

# Score constants used by the heuristic
_WIN_SCORE     = 100_000
_THREE_SCORE   = 10
_TWO_SCORE     = 2
_CENTER_BONUS  = 3


class Bot:
    """Heuristic-based Connect 4 bot using minimax with alpha-beta pruning.

    Design notes
    ------------
    - ``difficulty`` controls the minimax search depth.  Depth 4 gives
      a strong casual opponent without noticeable latency.
    - ``_score_window`` assigns local scores to every window of 4 cells,
      which ``_score_position`` aggregates across all rows, columns, and
      diagonals to produce a single board evaluation.
    - The bot favours the centre column because centre control gives the
      most winning threats in Connect 4.
    """

    def __init__(self, difficulty: int = 4) -> None:
        self.difficulty = difficulty

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_move(self, board: Board) -> int:
        """Return the column index of the best move for the bot.

        Uses minimax with alpha-beta pruning up to *self.difficulty* plies.
        """
        pass

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

        Parameters
        ----------
        board:
            Current board state.
        depth:
            Remaining search depth.
        alpha / beta:
            Alpha-beta bounds.
        maximizing:
            True when it is the bot's turn to move.

        Returns
        -------
        (best_col, score)
            ``best_col`` is None at terminal nodes.
        """
        pass

    # ------------------------------------------------------------------
    # Heuristic evaluation
    # ------------------------------------------------------------------

    def _score_position(self, board: Board) -> float:
        """Return a heuristic score of *board* from the bot's perspective.

        Positive values favour the bot; negative values favour the human.
        Evaluation considers:
          - Centre column occupancy (positional advantage)
          - All horizontal, vertical, and diagonal windows of length 4
        """
        pass

    def _score_window(self, window: list[int]) -> float:
        """Score a single window of 4 cells.

        Scoring rules (bot-centric):
          - 4 bot pieces          → +WIN_SCORE
          - 3 bot pieces + 1 empty → +THREE_SCORE
          - 2 bot pieces + 2 empty → +TWO_SCORE
          - 3 human pieces + 1 empty → -THREE_SCORE  (blocking threat)
        """
        pass
