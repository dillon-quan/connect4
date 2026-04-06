import time
import numpy as np

from connect4.board import Board, HUMAN, BOT, EMPTY, ROWS, COLS
from connect4.bot import Bot, _WIN_SCORE, _THREE_SCORE, _TWO_SCORE


class TestGetMove:
    def test_returns_valid_column(self):
        bot = Bot()
        board = Board()
        col = bot.get_move(board)
        assert 0 <= col < COLS
        assert board.is_valid_column(col)

    def test_wins_immediately_if_possible(self):
        # BOT has three in a row at the bottom; col 3 completes the horizontal win.
        # depth=1 is enough: the heuristic scores [BOT,BOT,BOT,BOT] as _WIN_SCORE.
        bot = Bot(depth=1)
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0:3] = BOT
        col_heights = {col: ROWS - 1 for col in range(COLS)}
        col_heights[0] = col_heights[1] = col_heights[2] = ROWS - 2
        board = Board(grid=grid, col_heights=col_heights)

        assert bot.get_move(board) == 3

    def test_blocks_human_winning_threat(self):
        # HUMAN has three in a row; bot must play col 3 to block.
        # depth=3 is required: the bot needs to see human playing col 3 and
        # winning before it recognises the threat via the terminal win check.
        bot = Bot(depth=3)
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0:3] = HUMAN
        grid[4, 0:2] = BOT
        col_heights = {col: ROWS - 1 for col in range(COLS)}
        col_heights[0] = col_heights[1] = col_heights[2] = ROWS - 2
        col_heights[0] = col_heights[1] = ROWS - 3
        board = Board(grid=grid, col_heights=col_heights)

        assert bot.get_move(board) == 3

    def test_takes_win_over_blocking(self):
        # BOT can win vertically in col 0 (rows 3–5 already filled).
        # HUMAN threatens horizontally at row 5 cols 3–5 and would win at col 6.
        # Bot must choose its own win (col 0) rather than block (col 6).
        # depth=1 is enough: the heuristic scores the vertical [BOT]*4 as _WIN_SCORE.
        bot = Bot(depth=1)
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0] = BOT
        grid[4, 0] = BOT
        grid[3, 0] = BOT
        grid[5, 3] = HUMAN
        grid[5, 4] = HUMAN
        grid[5, 5] = HUMAN
        col_heights = {col: ROWS - 1 for col in range(COLS)}
        col_heights[0] = ROWS - 4        # rows 3,4,5 taken — next piece lands at row 2
        col_heights[3] = col_heights[4] = col_heights[5] = ROWS - 2
        board = Board(grid=grid, col_heights=col_heights)

        assert bot.get_move(board) == 0

    def test_prefers_centre_column_as_first_move(self):
        # On an empty board at depth=1 every column produces windows with only
        # one piece, which score 0. The sole differentiator is the centre-column
        # bonus (+_CENTER_BONUS) applied to col 3, making it uniquely optimal.
        bot = Bot(depth=1)
        board = Board()

        assert bot.get_move(board) == 3

    def test_does_not_play_in_full_column(self):
        bot = Bot()
        board = Board()
        for _ in range(ROWS):
            board.insert_piece(3, HUMAN)
        col = bot.get_move(board)
        assert col != 3

    def test_get_move_is_fast_enough(self):
        bot = Bot(depth=4)
        board = Board()
        start = time.time()
        bot.get_move(board)
        assert time.time() - start < 1.0

class TestScoreWindow:
    def setup_method(self):
        self.bot = Bot()

    def test_four_bot_pieces_is_win_score(self):
        assert self.bot._score_window([BOT, BOT, BOT, BOT]) == _WIN_SCORE

    def test_three_bot_one_empty(self):
        assert self.bot._score_window([BOT, BOT, BOT, EMPTY]) == _THREE_SCORE

    def test_two_bot_two_empty(self):
        assert self.bot._score_window([BOT, BOT, EMPTY, EMPTY]) == _TWO_SCORE

    def test_three_human_one_empty_is_negative(self):
        assert self.bot._score_window([HUMAN, HUMAN, HUMAN, EMPTY]) == -_THREE_SCORE

    def test_two_human_two_empty_is_negative(self):
        assert self.bot._score_window([HUMAN, HUMAN, EMPTY, EMPTY]) == -_TWO_SCORE

    def test_mixed_window_scores_zero(self):
        # Both players present — neither can complete a four-in-a-row here.
        assert self.bot._score_window([BOT, HUMAN, EMPTY, EMPTY]) == 0.0
        assert self.bot._score_window([BOT, HUMAN, BOT, HUMAN]) == 0.0

    def test_all_empty_scores_zero(self):
        assert self.bot._score_window([EMPTY, EMPTY, EMPTY, EMPTY]) == 0.0

    def test_order_does_not_affect_result(self):
        # _score_window uses .count(), so position within the window is irrelevant.
        assert self.bot._score_window([EMPTY, BOT, BOT, BOT]) == _THREE_SCORE
        assert self.bot._score_window([EMPTY, HUMAN, HUMAN, HUMAN]) == -_THREE_SCORE


class TestScorePosition:
    def setup_method(self):
        self.bot = Bot()

    def test_empty_board_scores_zero(self):
        # No pieces on the board, so no window contributes and the centre
        # column is empty — total score must be exactly 0.
        board = Board()
        assert self.bot._score_position(board) == 0.0

    def test_bot_piece_in_centre_scores_positive(self):
        # A single BOT piece in the centre column earns the centre bonus.
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, COLS // 2] = BOT
        board = Board(grid=grid)
        assert self.bot._score_position(board) > 0.0

    def test_bot_advantage_scores_positive(self):
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0] = BOT
        grid[5, 1] = BOT
        board = Board(grid=grid)
        assert self.bot._score_position(board) > 0.0

    def test_human_advantage_scores_negative(self):
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0] = HUMAN
        grid[5, 1] = HUMAN
        board = Board(grid=grid)
        assert self.bot._score_position(board) < 0.0

    def test_three_bot_in_row_scores_higher_than_two(self):
        # More pieces in a line = higher threat value.
        grid_two = np.zeros((ROWS, COLS), dtype=int)
        grid_two[5, 0:2] = BOT

        grid_three = np.zeros((ROWS, COLS), dtype=int)
        grid_three[5, 0:3] = BOT

        score_two = self.bot._score_position(Board(grid=grid_two))
        score_three = self.bot._score_position(Board(grid=grid_three))
        assert score_three > score_two

    def test_symmetric_positions_cancel_out(self):
        # Equal BOT and HUMAN threats of the same strength should produce a
        # score close to zero (ignoring the centre-column bonus).
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0] = BOT
        grid[5, 6] = HUMAN
        board = Board(grid=grid)
        # Both contribute equally and symmetrically — net score ≈ 0.
        assert self.bot._score_position(board) == 0.0


class TestMinimax:
    def setup_method(self):
        self.bot = Bot()

    def test_depth_zero_returns_no_column(self):
        board = Board()
        col, _ = self.bot._minimax(board, depth=0, alpha=-np.inf, beta=np.inf, maximizing=True)
        assert col is None

    def test_depth_zero_returns_heuristic_score(self):
        board = Board()
        _, score = self.bot._minimax(board, depth=0, alpha=-np.inf, beta=np.inf, maximizing=True)
        assert score == self.bot._score_position(board)

    def test_detects_bot_win_terminal(self):
        # Board already in a BOT-won state — minimax must return immediately.
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0:4] = BOT
        board = Board(grid=grid)
        col, score = self.bot._minimax(board, depth=4, alpha=-np.inf, beta=np.inf, maximizing=True)
        assert col is None
        assert score == _WIN_SCORE

    def test_detects_human_win_terminal(self):
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0:4] = HUMAN
        board = Board(grid=grid)
        col, score = self.bot._minimax(board, depth=4, alpha=-np.inf, beta=np.inf, maximizing=False)
        assert col is None
        assert score == -_WIN_SCORE

    def test_detects_draw_returns_zero(self):
        # Full board with no winner — score must be 0, column must be None.
        H, B = HUMAN, BOT
        grid = np.array(
            [
                [H, B, H, B, H, B, H],
                [H, B, H, B, H, B, H],
                [B, H, B, H, B, H, B],
                [B, H, B, H, B, H, B],
                [H, B, H, B, H, B, H],
                [H, B, H, B, H, B, H],
            ],
            dtype=int,
        )
        col_heights = {col: -1 for col in range(COLS)}
        board = Board(grid=grid, col_heights=col_heights)
        col, score = self.bot._minimax(board, depth=4, alpha=-np.inf, beta=np.inf, maximizing=True)
        assert col is None
        assert score == 0

    def test_maximizing_returns_a_column(self):
        # At depth > 0 on a non-terminal board, minimax must pick a column.
        board = Board()
        col, _ = self.bot._minimax(board, depth=1, alpha=-np.inf, beta=np.inf, maximizing=True)
        assert col is not None
        assert 0 <= col < COLS
