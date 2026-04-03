import pytest
from unittest.mock import patch, MagicMock

from connect4.game import Game
from connect4.board import HUMAN, BOT


class TestDetermineFirstPlayer:
    def test_returns_human_or_bot(self):
        """First player must be either HUMAN or BOT."""
        pass

    def test_randomness_produces_both_options(self):
        """Over many trials, both HUMAN and BOT should be chosen at least once."""
        pass


class TestHandleHumanTurn:
    def test_valid_input_returns_column(self):
        pass

    def test_reprompts_on_invalid_column(self):
        """When the player enters a full or out-of-bounds column, the game should
        keep prompting until a valid column is provided."""
        pass

    def test_reprompts_on_non_integer_input(self):
        pass


class TestHandleBotTurn:
    def test_returns_valid_column(self):
        pass


class TestRunLoop:
    def test_human_wins_ends_game(self):
        """run() should return after the human achieves a win."""
        pass

    def test_bot_wins_ends_game(self):
        pass

    def test_draw_ends_game(self):
        pass
