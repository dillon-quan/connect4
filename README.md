# Connect 4

A terminal-based Connect 4 game where you play against a bot. The bot uses a minimax algorithm with alpha-beta pruning and heuristic board evaluation to play competitively against a casual player.

## Project Structure

```
connect_4/
├── connect4/
│   ├── __init__.py       # exposes Game
│   ├── board.py          # Board class — state, validation, win detection
│   ├── bot.py            # Bot class — minimax + heuristic evaluation
│   ├── display.py        # terminal rendering
│   └── game.py           # Game class — turn loop, player orchestration
├── tests/
│   ├── test_board.py
│   ├── test_bot.py
│   └── test_game.py
├── main.py               # entry point
└── pyproject.toml
```

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Setup

### Using uv (recommended)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repo and navigate into it
git clone <repo-url>
cd connect_4

# Create a virtual environment and install dependencies
uv sync
```

### Using pip

```bash
git clone <repo-url>
cd connect_4

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install numpy
```

## How to Play

```bash
# With uv
uv run python main.py

# With pip / activated venv
python main.py
```

The game runs in your terminal. You will be prompted to enter a column number (0–6) to drop your piece. The bot will automatically take its turn after yours.

```
 0  1  2  3  4  5  6
```

- **You** are player `1` (yellow)
- **Bot** is player `2` (red)
- First to get four in a row — horizontally, vertically, or diagonally — wins
- Who goes first is decided randomly at the start of each game

## Running Tests

```bash
# With uv
uv run pytest tests/

# With pip / activated venv
pytest tests/
```
