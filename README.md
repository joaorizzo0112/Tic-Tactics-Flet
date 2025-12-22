# ❌ vs ⭕ | Flet Tic-Tactics

> A tactical, modern, and cross-platform Tic-Tac-Toe game built with Python and Flet.

![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Flet](https://img.shields.io/badge/flet-latest-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

## 🎮 About the Project

**Flet Tic-Tactics** takes the classic paper-and-pencil game to the next level by introducing RPG-like progression, strategic game modes, and a responsive UI. Whether you want to challenge a friend or defeat an unbeatable AI, this game offers a fresh experience on the traditional 3x3 grid.

### ✨ Key Features

* **🤖 Smart AI (PvE):**
    * **Easy Mode:** Perfect for casual play and beginners.
    * **Hard Mode:** Powered by the **Minimax Algorithm**, making the bot mathematically unbeatable.
* **👥 Local Multiplayer (PvP):** Challenge your friends on the same device.
* **🎲 Unique Game Styles:**
    * **Classic:** The traditional rules you know and love.
    * **Inverted:** A "Misere" variant where the player who gets 3 in a row **loses**.
    * **Mined:** Random mines block specific cells on the grid, forcing you to adapt your strategy.
* **🏆 Progression System:**
    * **Achievements:** Unlock badges for specific milestones (e.g., "First Win", "Invincible").
    * **Statistics:** Track your wins, losses, and draws across all game modes.
* **🎨 Customization & Accessibility:**
    * **Themes:** Switch between Light and Dark modes.
    * **Localization:** Fully translated into English, Portuguese (BR), and Spanish.

## 🚀 Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

* [Python 3.7+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR-USERNAME/flet-tic-tactics.git](https://github.com/YOUR-USERNAME/flet-tic-tactics.git)
    cd flet-tic-tactics
    ```

2.  **Create a virtual environment (Optional but recommended):**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install flet
    ```

4.  **Run the game:**
    ```bash
    python main.py
    ```

## 📂 Project Structure

```text
flet-tic-tactics/
│
├── assets/          # Game assets (Pixel Art icons and fonts)
├── data/            # JSON files for local storage (Stats, Achievements, Translations)
├── main.py          # Main application entry point
└── README.md        # Project documentation
