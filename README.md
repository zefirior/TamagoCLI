# 🎮 Tamagochi - Console Pet Game

A colorful and interactive console-based Tamagochi game with multiple pet types, ASCII art animations, and real-time gameplay!

## ✨ Features

- 🐱 **5 Different Pet Types**: Cat, Dog, Dragon, Bunny, and Alien - each with unique traits!
- 🎨 **Colorful ASCII Art**: Beautiful sprites with different states and animations
- 📊 **Real-time Stats**: Monitor hunger, happiness, energy, and health
- 🎬 **Smooth Animations**: Watch your pet move and change moods
- 💾 **Auto-save**: Your progress is automatically saved
- ⌨️ **Interactive Navigation**: Arrow key navigation with stable two-column layout!
- 👁️ **Live Preview**: See your pet sprite in real-time as you browse
- ✨ **ZERO Flickering**: Full curses implementation with double buffering - updates only changed elements!
- 🎮 **Dual Control Modes**: Arrow keys + Enter OR direct letter commands

## 🐾 Pet Types

1. **Cat** 🐱 - Independent, efficient eater, less needy
2. **Dog** 🐶 - Loyal, needs lots of attention, always hungry  
3. **Dragon** 🐉 - Powerful, eats a lot, low energy drain
4. **Bunny** 🐰 - Cute, efficient eater, moderate needs
5. **Alien** 👽 - Mysterious, minimal hunger, needs entertainment

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup the game

```bash
# Clone or navigate to the project directory
cd tamagochi

# Create virtual environment and install dependencies
uv sync

# Run the game
uv run tamagochi
```

## 🧪 Development

### Running Tests

```bash
# Install dev dependencies
uv sync --extra dev

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=tamagochi --cov-report=html

# Run specific test file
uv run pytest tests/test_eating_timer.py

# Run with verbose output
uv run pytest -v
```

See [tests/README.md](tests/README.md) for more testing details.

## 🎮 How to Play

### Menu Navigation (NEW!)

The game features a modern two-column interface:
- **Left Panel**: List of all available options
- **Right Panel**: Live preview of selected option
- **Fixed Layout**: No jumping or resizing!

Controls:
- **↑/↓ Arrow Keys** - Navigate through menu options
- **Enter** - Select option
- **Q** - Quit/Cancel

### In-Game Controls

- **F** - Feed your pet 🍖
- **P** - Play with your pet 🎾
- **S** - Put pet to sleep / Wake up 😴
- **H** - Heal your pet 💊
- **Q** - Save and quit 💾

### Game Mechanics

- **Hunger**: Decreases over time. Feed your pet to keep them satisfied!
- **Happiness**: Your pet needs attention! Play with them regularly.
- **Energy**: Depletes during activities. Let your pet sleep to recover.
- **Health**: If hunger, happiness, or energy get too low, health will suffer.

### Tips

- 🍖 Don't let hunger reach 0 or health will drop rapidly!
- 😊 Play with your pet to keep happiness high
- 😴 Let your pet sleep when energy is low
- 💊 Use heal when health drops below 30
- 💾 Game auto-saves every 30 seconds

## 📁 Project Structure

```
tamagochi/
├── pyproject.toml           # Project configuration
├── README.md                # This file
└── tamagochi/              # Main package
    ├── __init__.py
    ├── main.py             # Entry point
    ├── models/             # Game models
    │   ├── __init__.py
    │   └── pet.py          # Pet logic
    ├── display/            # Rendering
    │   ├── __init__.py
    │   ├── sprites.py      # ASCII art
    │   └── renderer.py     # UI renderer
    └── game/               # Game engine
        ├── __init__.py
        ├── engine.py       # Game loop
        └── save_manager.py # Save/load
```

## 🔧 Development

### Run from source

```bash
uv run python -m tamagochi.main
```

### Add dependencies

```bash
uv add <package-name>
```

### Format code

```bash
uv run ruff format .
```

## 🎯 Future Ideas

- [ ] More pet types
- [ ] Evolution system
- [ ] Mini-games
- [ ] Achievements
- [ ] Multiple pets at once
- [ ] Pet interactions
- [ ] Seasonal events

## 📝 License

This project is open source and available for personal use and modification.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests!

---

Made with ❤️ and Python

