import pytest

from connect4.board import Board, HUMAN, BOT, ROWS, COLS
from connect4.bot import Bot


class TestGetMove:
    def test_returns_valid_column(self):
        """Bot move must be a column index that currently accepts a piece."""
        pass

    def test_wins_immediately_if_possible(self):
        """Bot should take a winning move when one is available."""
        pass

    def test_blocks_human_winning_threat(self):
        """Bot should block a human who is one move away from winning."""
        pass

    def test_does_not_play_in_full_column(self):
        pass


class TestScoreWindow:
    def test_four_bot_pieces_is_win_score(self):
        pass

    def test_three_bot_one_empty_is_high_score(self):
        pass

    def test_three_human_one_empty_is_negative_score(self):
        """A near-win for the human should produce a negative score."""
        pass

    def test_mixed_window_scores_zero_or_low(self):
        """A window with both players' pieces has no winning potential."""
        pass


class TestScorePosition:
    def test_empty_board_scores_near_zero(self):
        """Centre column bonus aside, an empty board should score close to 0."""
        pass

    def test_bot_advantage_scores_positive(self):
        """A position with more bot threats should outscore an empty board."""
        pass

    def test_human_advantage_scores_negative(self):
        pass


class TestMinimax:
    def test_depth_zero_returns_no_column(self):
        """At depth 0, minimax should return a terminal evaluation with col=None."""
        pass

    def test_detects_terminal_win_state(self):
        pass
