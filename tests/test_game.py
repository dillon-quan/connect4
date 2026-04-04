import pytest
from unittest.mock import patch
import numpy as np

from connect4.game import Game
from connect4.board import Board, HUMAN, BOT, EMPTY, ROWS, COLS


@pytest.fixture
def silence_display():
    """Suppress all terminal output produced by game.run()."""
    with (
        patch("connect4.game.print_welcome"),
        patch("connect4.game.print_board"),
        patch("connect4.game.print_turn"),
        patch("connect4.game.print_winner"),
        patch("connect4.game.print_draw"),
    ):
        yield


class TestDetermineFirstPlayer:
    def test_returns_human_or_bot(self):
        game = Game()
        assert game.current_player in (HUMAN, BOT)

    def test_randomness_produces_both_options(self):
        # With p=0.5 each, the probability of seeing only one value in 100
        # trials is (0.5)^99 * 2 — effectively zero.
        results = set()
        for _ in range(100):
            game = Game()
            results.add(game.current_player)
            if results == {HUMAN, BOT}:
                break
        assert results == {HUMAN, BOT}


class TestHandleHumanTurn:
    def test_valid_input_returns_column(self):
        game = Game()
        with patch("builtins.input", return_value="3"):
            col = game._handle_human_turn()
        assert col == 3

    def test_reprompts_on_out_of_bounds_column(self):
        # Column 9 is out of range; the second input (3) should be accepted.
        game = Game()
        with patch("builtins.input", side_effect=["9", "3"]):
            col = game._handle_human_turn()
        assert col == 3

    def test_reprompts_on_full_column(self):
        # Fill column 0 completely, then verify the loop skips it.
        game = Game()
        for _ in range(ROWS):
            game.board.insert_piece(0, HUMAN)
        with patch("builtins.input", side_effect=["0", "1"]):
            col = game._handle_human_turn()
        assert col == 1

    def test_reprompts_on_non_integer_input(self):
        game = Game()
        with patch("builtins.input", side_effect=["abc", "2"]):
            col = game._handle_human_turn()
        assert col == 2


class TestHandleBotTurn:
    def test_returns_column_from_bot(self):
        game = Game()
        with patch.object(game.bot, "get_move", return_value=3) as mock_get_move:
            col = game._handle_bot_turn()
        assert col == 3
        mock_get_move.assert_called_once()

    def test_passes_board_copy_to_bot(self):
        """Bot must receive a copy of the board, not the live instance, so that
        minimax simulations cannot corrupt the actual game state."""
        game = Game()
        captured = {}

        def capture_board(board):
            captured["board"] = board
            return 3

        with patch.object(game.bot, "get_move", side_effect=capture_board):
            game._handle_bot_turn()

        assert captured["board"] is not game.board


class TestRunLoop:
    def test_human_wins_ends_game(self, silence_display):
        game = Game()
        game.current_player = HUMAN

        # Place three HUMAN pieces in the bottom row (cols 0–2).
        # Inserting at col 3 will complete the horizontal four-in-a-row.
        game.board._grid[5, 0:3] = HUMAN
        game.board._col_heights[0] = 4
        game.board._col_heights[1] = 4
        game.board._col_heights[2] = 4

        with patch.object(game, "_handle_human_turn", return_value=3):
            game.run()

        assert game.board.check_win(HUMAN)

    def test_bot_wins_ends_game(self, silence_display):
        game = Game()
        game.current_player = BOT

        # Mirror the human-win setup but for BOT.
        game.board._grid[5, 0:3] = BOT
        game.board._col_heights[0] = 4
        game.board._col_heights[1] = 4
        game.board._col_heights[2] = 4

        with patch.object(game, "_handle_bot_turn", return_value=3):
            game.run()

        assert game.board.check_win(BOT)

    def test_draw_ends_game(self, silence_display):
        # Near-full board using the two-row stripe pattern (verified in
        # test_board.py to contain no four-in-a-row). Column 0 has one
        # slot remaining at row 0. Placing BOT there does not create a win.
        game = Game()
        game.current_player = BOT

        H, B = HUMAN, BOT
        grid = np.array(
            [
                [EMPTY, B, H, B, H, B, H],
                [H,     B, H, B, H, B, H],
                [B,     H, B, H, B, H, B],
                [B,     H, B, H, B, H, B],
                [H,     B, H, B, H, B, H],
                [H,     B, H, B, H, B, H],
            ],
            dtype=int,
        )
        game.board._grid = grid
        game.board._col_heights = {col: -1 for col in range(COLS)}
        game.board._col_heights[0] = 0

        with patch.object(game, "_handle_bot_turn", return_value=0):
            game.run()

        assert game.board.is_draw()
