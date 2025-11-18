# The Countdown of Conte Carlos – Analysis & Design

### Finn Maguire & Jericho Morallo
## 1. Game Overview

- **Working title:** The Countdown of Conte Carlos 
- **Engine / Framework:** Pygame Zero coded in VS Code
- **Goal of the game:** Carlos must match a target (white) histogram by:
    - Picking a **distribution shape** for random variable `x` (Bandit 1) which will be in the list of, and also,  
    - Picking a **function** `f(x)` (Bandit 2) to transform that variable,

so that the resulting transformed distribution matches the given target. If he picks the correct combination, he is recognized and wins. Otherwise, he loses fingers or runs out of time, losing the throne to Inigo (Damn you Inigo!!!).

**Core story elements:**
- Carlos vs. Inigo for the throne.
- A magical hourglass as a countdown timer.
- Carlos has 6 fingers; each incorrect submission costs 1 finger.
- If fingers reach 0 → Carlos dies.
- If time reaches 0 → the queen dies and Carlos is executed.

---

## 2. Requirements Analysis

### 2.1 Functional Requirements

1. **Target Histogram Display**
   - Show a fixed target histogram (white) on screen at game start.
   - The target corresponds to some combination of:
     - Base distribution of `x` (e.g., bell-shaped, skewed right, etc.)
     - Transformation `f(x)` (e.g., `f(x) = x`, `f(x) = x²`, etc.).

2. **Bandit 1 – Distribution Selector**
   - Bandit 1’s screen has a single “lever” control.
   - Cycling the lever iterates over available distributions for `x`, e.g.:
     - Bell-shaped (normal),
     - Skewed right,
     - Skewed left,
     - Uniform,
     - Symmetric bimodal,
     - Non-symmetric bimodal.
   - The currently selected distribution should be **visually indicated** (e.g., highlighted name or sample histogram preview).

3. **Bandit 2 – Function Selector**
   - Bandit 2’s screen also has a single lever.
   - Cycling the lever iterates over available transform functions `f(x)`, e.g.:
     - `f(x) = x`
     - `f(x) = x²`
     - `f(x) = √x`
     - 'f(x) = 1/x'
   - The currently selected function is clearly displayed (as a formula or label).

4. **Submission / Confirmation**
   - A specific key (e.g. `ENTER`) or on-screen button confirms Carlos’s choice.
   - When submitted:
     - Compute (or look up) the resulting transformed distribution.
     - Compare it to the target histogram.
     - Decide **correct** vs **incorrect**.

5. **Feedback and Win/Loss Conditions**
   - **Correct combination:**
     - Show win message (You Win, The Throne has been regained!!!).
     - Stop countdown / freeze interactions.
   - **Incorrect combination:**
     - Decrease finger count by 1.
     - Update on-screen display of remaining fingers.
     - If fingers > 0: allow another attempt (no reset of timer).
     - If fingers = 0: show death/game-over screen.

6. **Timer / Hourglass**
   - Countdown timer displayed either as:
     - Numeric countdown (e.g. seconds remaining), and/or
     - Visual hourglass graphic with sand level changing.
   - When timer hits 0:
     - Trigger game-over (queen dies, Carlos executed).
     - Show game-over message and disable further input.

7. **Game States**
   - Main menu (optional).
   - Active puzzle state (main gameplay).
   - Win state.
   - Lose state (fingers = 0 or time = 0).

8. **Controls**
- We want the player to be able to switch each lever individually so they can mix and match simultaneously.
   - Keys for cycling distributions and functions:
     - e.g. `A/D` for left/right cycling distribution lever.
     - e.g. `J/L` for left/right cycling function lever.
   - Key to submit selection (e.g. `ENTER`).
   - Optional: `ESC` to quit.

---

### 2.2 Non-Functional Requirements

- **Visual clarity:** Distributions, functions, and the given histogram must be clearly distinguishable (labels, or numbered).

---

## 3. Game Flow / User Interaction

1. **Start of Game**
   - Game Title with Start Button
   - Display instructions briefly (goal, controls, penalties).
   - Generate or load the target histogram and show it at the bottom half of the game screen.

2. **Player Choices**
   - Player cycles through possible `x` distributions via Bandit 1’s lever.
   - Player cycles through possible `f(x)` functions via Bandit 2’s lever.

3. **Submission**
   - Player presses the submission key 'KP_ENTER'.
   - Game looks at the selected distribution and function name and matches it looks to see if the names correspond to the answer key.
     - If correct → win.
     - Else → lose a finger and continue (if any remain).

4. **End Conditions**
   - **Win:** Correct pair chosen before timer expires, with at least 1 finger left.
   - **Lose – fingers:** Fingers reach 0 before correct combination or timer.
   - **Lose – time:** Timer hits 0 before correct combination.

5. **Restart / Quit**
   - After win or loss, show options:
     - Restart (Will return to title screen to reset game).
     - Quit game.

---

## 4. Technical Design

### 4.1 Overall Architecture

- **Main file:** `contecarlo.py` using Pygame Zero
  - Uses standard Pygame Zero functions:
    - `draw()` – for rendering all visuals.
    - `update(dt)` – for updating timer and animations.
    - `on_mouse_down(pos)` – for handling player input.
    - `on_key_down(pos)`

- **Core components:**

  - `GameState` – tracks current state: `MENU`, `PLAYING`, `WIN`, `LOSE`.
  - `Puzzle` – contains:
    - Target distribution ID.
    - List of possible distribution IDs.
    - List of possible function IDs.
    - Mapping of (distribution ID, function ID) → resulting transformed distribution.
  - `UI` – responsible for showing target histogram, images for both bandit 1 and bandit 2, counter of fingers left, and countdown timer.

### 4.2 Data Structures

- **Distributions List:**
  ```python
  distributions = [
      {"name": "Normal", "image": dist_normal.png},        
      {"name": "Skewed Right", "image": dist_skw_right.png},  
      {"name": "Skewed Left", "image": dist_skw_left.png},
      {"name": "Uniform", "image": dist_uniform.png},
      {"name": "Bimodal Symmetrical", "image": dist_bimodal_sym.png},
      {"name": "Bimodal Asymmetrical", "image": dist_bimodal_asym.png}
  ]
  
- **Functions List**
  ```python
  functions = [
      {"name": "f(x) = x", "image": x_function.png},
      {"name": "f(x) = x^2", "image": x_squared.png},
      {"name": "f(x) = sqrt(x)", "image": sqrt_x.png},
      {"name": "f(x) = 1/x", "image": x_invrt.png},
  ]
