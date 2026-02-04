# Ping-Pong Game

A two-player Ping-Pong game. Play in the **browser** or with **Python/Pygame**.

## Features

- **Game environment:** Playing field, two paddles, ball
- **Player input:** Move paddles up and down (Player 1: W/S, Player 2: ↑/↓)
- **Ball movement and collisions:** Ball moves, bounces off walls and paddles, direction changes
- **Score keeping:** Scores displayed and updated when the ball passes a paddle’s goal line

---

## Play in the browser

1. Open **`index.html`** in any modern browser (double-click or drag into a browser tab).
2. Choose **1 Player (vs Computer)** or **2 Players**.
3. No server or install needed.

---

## Play with Python (desktop)

```bash
pip install -r requirements.txt
python ping_pong.py
```

At the start screen: press **1** for Single Player (vs Computer), **2** for Two Players.

---

## Controls

| Player  | Move up | Move down |
|---------|---------|-----------|
| Player 1 / You (left)  | W | S |
| Player 2 / Computer (right) | ↑ | ↓ (human only) |

In **1 Player** mode, the computer controls the right paddle; you control the left with W/S.

**Pause:** Press **P** or **Space** (or click the Pause button in the browser) to pause and resume.

Close the window (or tab) to quit.
