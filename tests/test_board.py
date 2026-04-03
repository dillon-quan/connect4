import pytest
import numpy as np

from connect4.board import Board, HUMAN, BOT, EMPTY, ROWS, COLS


class TestBoardInit:
    def test_initial_board_is_empty(self):
        """All cells should be EMPTY (0) on a fresh board."""
        pass

    def test_board_dimensions(self):
        """Grid must be 6 rows × 7 columns."""
        pass

    def test_col_heights_initialised(self):
        """Each column tracker should start at ROWS - 1 (bottom row)."""
        pass


class TestIsValidColumn:
    def test_empty_column_is_valid(self):
        pass

    def test_full_column_is_invalid(self):
        pass

    def test_out_of_bounds_column_is_invalid(self):
        pass


class TestInsertPiece:
    def test_first_piece_lands_at_bottom(self):
        """Piece inserted into an empty column should sit in the last row."""
        pass

    def test_second_piece_stacks_above_first(self):
        pass

    def test_insert_updates_col_height(self):
        pass

    def test_insert_correct_player_value(self):
        pass


class TestWinConditions:
    def test_horizontal_win_human(self):
        """Four human pieces in a row horizontally should trigger a win."""
        pass

    def test_horizontal_win_bot(self):
        pass

    def test_vertical_win(self):
        """Four pieces stacked in the same column should trigger a win."""
        pass

    def test_diagonal_win_positive_slope(self):
        """Win along a bottom-left → top-right diagonal."""
        pass

    def test_diagonal_win_negative_slope(self):
        """Win along a top-left → bottom-right diagonal."""
        pass

    def test_no_win_with_only_three_in_a_row(self):
        pass

    def test_no_win_on_empty_board(self):
        pass

    def test_interrupted_row_is_not_a_win(self):
        """Three same-player pieces broken by an opponent piece is not a win."""
        pass


class TestIsDraw:
    def test_empty_board_is_not_draw(self):
        pass

    def test_full_board_without_winner_is_draw(self):
        """Filling every cell should be detected as a draw."""
        pass


class TestCopy:
    def test_copy_is_independent(self):
        """Mutating the copy must not affect the original board."""
        pass

    def test_copy_has_same_state(self):
        pass
