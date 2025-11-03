# ♟️ Chess Game using Alpha-Beta Pruning (AI-based)

An AI-powered Chess Game built using **Python** and **Pygame**, implementing the **Minimax Algorithm with Alpha-Beta Pruning** for optimal decision-making.  
The project allows a **Player vs AI** match with a smooth graphical interface and intelligent move selection.

---

## 🧠 Project Overview

This project demonstrates how **Artificial Intelligence** can be used to make strategic decisions in a complex game like chess.  
The AI uses **Alpha-Beta Pruning**, an optimization technique for the **Minimax Algorithm**, which significantly reduces the number of nodes evaluated in the game tree.

### 🎯 Features
- 🧩 Player vs AI mode  
- ⚙️ AI logic using **Minimax + Alpha-Beta Pruning**  
- 📊 Adjustable search depth (default: 4–5 ply)  
- 🖥️ Intuitive GUI built with Pygame  
- 💡 Support for standard chess rules (castling, en passant, pawn promotion, etc.)  
- 🚀 Easy to extend — add opening book, heuristic evaluation, or neural enhancements  

---

## 🏗️ Project Structure

```

Chess/
├── ChessAI.py         # Core AI logic (Minimax + Alpha-Beta)
├── ChessEngine.py     # Game state, move generation, validation
├── ChessMain.py       # Main file to run the game
├── images/            # Chess piece assets (PNG images)
└── README.md          # Project documentation

````

---

## ⚙️ Installation & Setup

### Step 1: Clone the repository
```bash
git clone https://github.com/<your-username>/chess-ai-alpha-beta.git
cd chess-ai-alpha-beta/Chess
````

### Step 2: Install dependencies

Make sure you have Python (>=3.10) and pip installed.

```bash
pip install pygame
```

### Step 3: Run the game

```bash
python -m Chess.ChessMain
```

---

## 🕹️ How to Play

* The game starts with **Player (White)** vs **AI (Black)**.
* Use your mouse to select and move pieces.
* The AI responds after a short computation time.
* You can modify **search depth** inside `ChessAI.py` to adjust AI difficulty.

---

## 🤖 AI Algorithm Explanation

### 🔹 Minimax Algorithm

* Simulates all possible moves up to a certain depth.
* Maximizes the player's advantage while minimizing the opponent’s potential gains.

### 🔹 Alpha-Beta Pruning

* Optimizes Minimax by eliminating branches that won’t affect the final decision.
* Reduces computational cost and speeds up AI decisions.

```
Depth 0 (Root) → Player
  ├── Move A → (AI evaluates best reply)
  ├── Move B → (AI prunes less promising branches)
  └── Move C → (AI picks optimal move)
```

### ⚡ Typical Depth: 4–5 plies

This depth balances **speed** and **intelligence** — enough for the AI to play reasonably well.

---

## 🧩 Enhancements (Optional Extensions)

| Enhancement                         | Description                                                                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| ♜ **Opening Book**                  | Store common chess openings (e.g., Ruy Lopez, Sicilian Defense) in a JSON or SQLite database and play them instead of recalculating from scratch. |
| 🔍 **Piece Evaluation Heuristics**  | Include positional advantages (e.g., central control, mobility, king safety) in your scoring function.                                            |
| 🧬 **Machine Learning Integration** | Train a small neural net or regression model to tune evaluation weights.                                                                          |
| 🧱 **Move Ordering**                | Sort moves (captures first, checks, promotions) to improve pruning efficiency.                                                                    |
| 💾 **Save/Load Feature**            | Allow users to save and continue their matches.                                                                                                   |

## 📚 Technologies Used

* **Python 3.13**
* **Pygame (for GUI and event handling)**
* **Alpha-Beta Pruning (AI decision-making)**
* **Minimax Algorithm (game tree search)**
```
