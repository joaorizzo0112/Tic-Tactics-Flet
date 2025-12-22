# ❌ vs ⭕ | Flet Tic-Tactics

> **A tactical, modern, and cross-platform Tic-Tac-Toe game built with Python and Flet.**

## 🎮 About the Project

**Flet Tic-Tactics** takes the classic paper-and-pencil game to the next level by introducing RPG-like progression, strategic game modes, and a responsive UI. Whether you want to challenge a friend locally or defeat an unbeatable AI, this game offers a fresh experience on the traditional 3x3 grid.

## ✨ Key Features

### 🤖 Smart AI (PvE)
* **Easy Mode:** Perfect for casual play and beginners.
* **Hard Mode:** Powered by the **Minimax Algorithm**, making the bot mathematically unbeatable. Good luck!

### 👥 Local Multiplayer (PvP)
* Challenge your friends on the same device.

### 🎲 Unique Game Styles
* **Classic:** The traditional rules you know and love.
* **Inverted:** A "Misere" variant where the player who gets 3 in a row **LOSES** the match.
* **Mined:** Random mines block specific cells on the grid, forcing you to adapt your strategy.

### 🏆 Progression System
* **Achievements:** Unlock badges for specific milestones (e.g., "First Win", "Invincible", "Strategist").
* **Statistics:** Track your wins, losses, and draws across all game modes.

### 🎨 Customization & Accessibility
* **Themes:** Switch between Light and Dark modes.
* **Localization:** Fully translated into **English**, **Portuguese (BR)**, and **Spanish**.
* **Visuals:** Retro Pixel Art style with "Press Start 2P" font.

---

## 🚀 Download & Play (Windows)

Don't want to install Python? No problem!
1.  Go to the [**Releases Page**](https://github.com/joaorizzo0112/Tic-Tactics-Flet/releases).
2.  Download the latest `TicTactics.exe`.
3.  Double-click to play!

---

## 🛠️ Running from Source

Follow these steps to get a local copy up and running for development.

### Prerequisites
* Python 3.7+
* Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/joaorizzo0112/Tic-Tactics-Flet.git](https://github.com/joaorizzo0112/Tic-Tactics-Flet.git)
    cd Tic-Tactics-Flet
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install flet Pillow
    ```

4.  **Run the game:**
    ```bash
    python src/tic_tactics.py
    ```

## 📂 Project Structure

```text
Tic-Tactics-Flet/
│
├── assets/          # Game assets (Pixel Art icons, .ico, and fonts)
├── data/            # JSON files (Stats, Achievements, Strings/Translations)
├── src/
│   └── tic_tactics.py  # Main application logic
└── README.md        # Project documentation
