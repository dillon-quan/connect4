import numpy as np

from connect4.board import Board, HUMAN, BOT, EMPTY, ROWS, COLS


class TestBoardInit:
    def test_initial_board_is_empty(self):
        board = Board()
        assert (board.grid == EMPTY).all()

    def test_board_dimensions(self):
        board = Board()
        assert board.grid.shape == (ROWS, COLS)

    def test_col_heights_initialised(self):
        board = Board()
        for col in range(COLS):
            assert board._col_heights[col] == ROWS - 1


class TestIsValidColumn:
    def test_empty_column_is_valid(self):
        board = Board()
        assert board.is_valid_column(0) is True

    def test_full_column_is_invalid(self):
        board = Board()
        for _ in range(ROWS):
            board.insert_piece(0, HUMAN)
        assert board.is_valid_column(0) is False

    def test_out_of_bounds_column_is_invalid(self):
        board = Board()
        assert board.is_valid_column(-1) is False
        assert board.is_valid_column(COLS) is False


class TestInsertPiece:
    def test_first_piece_lands_at_bottom(self):
        board = Board()
        board.insert_piece(0, HUMAN)
        assert board.grid[ROWS - 1, 0] == HUMAN

    def test_second_piece_stacks_above_first(self):
        board = Board()
        board.insert_piece(0, HUMAN)
        board.insert_piece(0, BOT)
        assert board.grid[ROWS - 2, 0] == BOT

    def test_insert_updates_col_height(self):
        board = Board()
        board.insert_piece(3, HUMAN)
        assert board._col_heights[3] == ROWS - 2

    def test_insert_correct_player_value(self):
        board = Board()
        board.insert_piece(4, BOT)
        assert board.grid[ROWS - 1, 4] == BOT


class TestWinConditions:
    def test_horizontal_win_human(self):
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0:4] = HUMAN
        board = Board(grid=grid)
        assert board.check_win(HUMAN) is True

    def test_horizontal_win_bot(self):
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 3:7] = BOT
        board = Board(grid=grid)
        assert board.check_win(BOT) is True

    def test_vertical_win(self):
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[2:6, 3] = HUMAN
        board = Board(grid=grid)
        assert board.check_win(HUMAN) is True

    def test_diagonal_win_positive_slope(self):
        # ↗: pieces at (5,0), (4,1), (3,2), (2,3)
        grid = np.zeros((ROWS, COLS), dtype=int)
        for i in range(4):
            grid[5 - i, i] = BOT
        board = Board(grid=grid)
        assert board.check_win(BOT) is True

    def test_diagonal_win_negative_slope(self):
        # ↘: pieces at (0,0), (1,1), (2,2), (3,3)
        grid = np.zeros((ROWS, COLS), dtype=int)
        for i in range(4):
            grid[i, i] = HUMAN
        board = Board(grid=grid)
        assert board.check_win(HUMAN) is True

    def test_no_win_with_only_three_in_a_row(self):
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0:3] = HUMAN
        board = Board(grid=grid)
        assert board.check_win(HUMAN) is False

    def test_no_win_on_empty_board(self):
        board = Board()
        assert board.check_win(HUMAN) is False
        assert board.check_win(BOT) is False

    def test_interrupted_row_is_not_a_win(self):
        # H H H B — the opponent piece at index 3 breaks the run
        grid = np.zeros((ROWS, COLS), dtype=int)
        grid[5, 0:3] = HUMAN
        grid[5, 3] = BOT
        board = Board(grid=grid)
        assert board.check_win(HUMAN) is False


class TestIsDraw:
    def test_empty_board_is_not_draw(self):
        board = Board()
        assert board.is_draw() is False

    def test_full_board_without_winner_is_draw(self):
        # Two-row stripe pattern: every horizontal run is length 1,
        # every vertical run is length 2, and no diagonal reaches 4.
        # Verified manually that neither player has four in a row.
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

        assert board.check_win(HUMAN) is False
        assert board.check_win(BOT) is False
        assert board.is_draw() is True


class TestCopy:
    def test_copy_is_independent(self):
        board = Board()
        board.insert_piece(0, HUMAN)
        copy = board.copy()

        # mutate the copy — original must be unaffected
        copy.insert_piece(0, BOT)

        assert board.grid[ROWS - 2, 0] == EMPTY
        assert board._col_heights[0] == ROWS - 2

    def test_copy_has_same_state(self):
        board = Board()
        board.insert_piece(3, HUMAN)
        board.insert_piece(3, BOT)
        copy = board.copy()

        assert (copy.grid == board.grid).all()
        assert copy._col_heights == board._col_heights
