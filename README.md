# 🐍 Snake Rush: Arcade Edition

A modern, neon-themed take on the classic Snake game, built with **Python** and **Pygame**. Eat the food, grow longer, and avoid the walls and your own tail. The game speeds up as your score climbs.

<p align="center">
  <img src="screenshots/start-screen.png" width="32%" alt="Start screen">
  <img src="screenshots/gameplay.png" width="32%" alt="Gameplay">
  <img src="screenshots/game-over.png" width="32%" alt="Game over screen">
</p>

## Features

- Dark neon interface with live **Score** and **Best** cards
- Snake with eyes that face the direction of travel and a body that shades toward the tail
- Pulsing, glowing food
- Five game states: ready, playing, paused, game over and win
- Speed starts at 4 moves per second and rises with your score, capped at 15
- Pause, restart and play-again controls

## Controls

| Key | Action |
| --- | --- |
| `W` `A` `S` `D` or arrow keys | Move the snake |
| `Enter` | Start, or play again after the game ends |
| `Space` | Pause / resume |
| `R` | Restart (your best score is kept) |
| `Esc` | Quit |

## Getting started

### Option 1: Run the Windows executable

Download `dist/SnakeRush.exe` from this repository and double-click it. No Python needed. (Windows only. If Windows SmartScreen warns you, choose *More info* then *Run anyway*.)

### Option 2: Run from source

You need Python 3.8 or newer.

```bash
git clone https://github.com/Anshika-choudhary29/snake-rush.git
cd snake-rush
pip install pygame
python SnakeRush.py
```

## How it works

- **Board:** a 40 × 28 grid of 20 px cells (800 × 560 px) with a 90 px score panel above it.
- **Game loop:** read input, update the snake, draw everything, repeat at 60 FPS.
- **Snake:** stored as a list of `(x, y)` cells. Each move inserts a new head and removes the tail. When food is eaten the tail is kept, so the snake grows.
- **Food:** placed only on empty cells. If none are left, you win.

### Problems solved

| Problem | Solution |
| --- | --- |
| 180° reversal bug: quick key presses could turn the snake into itself | New direction is compared with the already-committed direction |
| Snake jumping several moves after un-pausing | The time accumulator is reset on resume |
| Food appearing on the snake | Food is chosen only from empty cells |
| Wrong collision on the turn the snake grows | The tail cell is ignored on a normal move, but the whole body is checked when eating |
| Game becoming unplayable at high scores | Speed increase is capped at 15 moves per second |

## Tech stack

- Python 3
- Pygame
- Standard library: `random`, `sys`

## Project structure

```
snake-rush/
├── SnakeRush.py      # complete game source
├── dist/
│   └── SnakeRush.exe # prebuilt Windows executable
├── screenshots/      # images used in this README
└── README.md
```

## Future ideas

- Sound effects
- High score saved to a file
- Multiple difficulty levels
- Obstacles and power-ups
- Start menu
- An AI-controlled snake

## Author

**Anshika Choudhary**, LNCT College. Built as a college mini project.
