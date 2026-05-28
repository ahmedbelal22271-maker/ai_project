
##  Team Members

| # | Name | ID |
|---|---|---|
| 1 | *Ahmed Belal Taher* |*2300216*|
| 2 | *Saifallah Basem Ahmed * |*2300142*|
| 3 | *Ahmed Mostafa Elsayed* |*2300192*|
| 4 | *Mahmoud Mohamed Mokhtar* |*2300824*|
| 5 | *Ahmed Mamoun Mahmoud Mamoun* |*2300035*|

---

##  Game Description

**Quoridor** is an award-winning abstract strategy board game. Two players race to move their pawn across a 9×9 board to the opposite side, while using walls to block each other's path.

### Rules Summary
- The board is **9×9 squares**
- Each player starts at the center of their baseline and has **10 walls**
- On each turn, a player must either **move their pawn** or **place a wall**
- Pawns move **one square orthogonally** (no diagonal movement)
- Walls are **2 squares long** and block movement between cells
- **Walls cannot completely block** a player's path to their goal (BFS enforced)
- If your pawn is adjacent to the opponent's, you can **jump over** them (or diagonally if blocked)
- **First player to reach the opposite baseline wins!**

---

## Screenshots

### Game in Progress
![alt text](image-1.png)

### Player 1 Wins
![alt text](image.png)

---

##  Demo Video

 **[Watch the Demo Video here](  )**

> The video demonstrates game setup, Human vs Human gameplay, and Human vs Computer gameplay across all three AI difficulty levels.

---

##  Installation & Running Instructions

### Prerequisites
- Python 3.x installed on your system
- pip (Python package manager)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/ahmedbelal22271-maker/ai_project.git
cd ai_project
```

### Step 2 — Install Dependencies
```bash
pip install pygame
```

### Step 3 — Run the Game
```bash
python main.py
```

>  No other dependencies are required. The game will launch immediately.

---

##  Controls

### Mouse Controls
| Action | How To Do It |
|---|---|
| **Move pawn** | Click on a highlighted valid cell |
| **Place a wall** | Hover between cells to preview, then click to place |
| **Select mode / buttons** | Click the buttons at the top of the screen |

### Button Controls
| Button | Action |
|---|---|
| `Reset` | Restart the game from the beginning |
| `Vs Human` | Switch to Human vs Human mode |
| `Undo` | Undo the last move |
| `Redo` | Redo an undone move |
| `Quit` | Exit the game |

### Keyboard Shortcuts
| Key | Action |
|---|---|
| `Ctrl + Z` | Undo last move |
| `Ctrl + Y` | Redo move |

---

##  AI Difficulty Levels

The game features three AI difficulty levels, each using a different strategy:

###  Easy
The Easy AI makes purely **random decisions**. It has a 20% chance to attempt placing a random wall; otherwise it picks a random valid pawn move. Great for beginners learning the game.

###  Medium
The Medium AI uses a **Greedy BFS Path-Blocking Strategy**:
1. It calculates the BFS shortest path for both itself and the human player
2. If the human is winning the race, it places a wall to block the human's path
3. Otherwise, it advances along its own shortest path toward the goal

###  Hard
The Hard AI uses **Heuristic State Evaluation (1-ply search)**:
- Evaluates every valid pawn move and wall placement using the score formula:
  > `Score = len(P1_path) − len(P2_path)`
- Simulates placing walls around the first 4 steps of the human's BFS path
- Applies a small penalty (−0.1) to wall placements to prefer moving unless a wall provides a strict advantage
- Selects the move that **maximizes its positional advantage**

---

##  Bonus Features

### Undo / Redo
Full undo/redo functionality is implemented using Python's `copy.deepcopy()` to snapshot the entire `GameState` at the end of every turn. This allows instant, bug-free state reversion:
- `history` stack stores all past states
- `redo_stack` stores undone states for redo
- Works for both pawn moves and wall placements

---
