import random
from pygame import Rect

# -----------------------------
# BASIC PYGAME ZERO SETTINGS
# -----------------------------
WIDTH = 900
HEIGHT = 600
TITLE = "The Countdown of Conte Carlos"

# -----------------------------
# GAME CONSTANTS
# -----------------------------
MAX_FINGERS = 6
ROUND_TIME = 60.0  # seconds

# Colors
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
RED     = (220, 60, 60)
GREEN   = (60, 200, 60)
YELLOW  = (230, 200, 25)
GREY    = (60, 60, 60)
BLUE    = (80, 80, 220)

# Histogram Distributions 
# -----------------------------
# CHANGED AS OF 2025-11-20
# -----------------------------
distributions = [
    {"name": "Normal Distribution","image": "dis_normal.png","ID": 1},
    {"name": "Skewed Right", "image": "dist_skw_right.png", "ID": 2},
    {"name": "Skewed Left", "image": "dist_skw_left.png", "ID": 3},
    {"name": "Uniform", "image": "dist_uniform.png", "ID": 4},
    {"name": "Bimodal (Symmetric)", "image": "dist_bimodal_sym.png", "ID": 5},
    {"name": "Bimodal (Non-symmetric)", "image": "dist_bimodal_sym.png", "ID": 6},
]
# Functions
# -----------------------------
# CHANGED AS OF 2025-11-20
# -----------------------------
functions = [
    {"name": "f(x) = x", "image": "fn_x.png", "ID": 1 },
    {"name": "f(x) = x^2", "image": "fn_x^2.png", "ID": 2},
    {"name": "f(x) = sqrt(x)", "image": "fn_sqrt(x).png", "ID": 3},
    {"name": "f(x) = 1 - x", "image": "fn_1minusx.png", "ID": 4}
]

# Potential Answers
# -----------------------------
# CHANGED AS OF 2025-11-20
# -----------------------------
answers = [
    {"name": "Answer 1", "image": "", "Dist ID": 2, "Function ID": 1},
    {"name": "Answer 2", "image": "", "Dist ID": 5, "Function ID": 3},
]

# -----------------------------
# GAME STATE
# -----------------------------
current_dist_index = 0
current_func_index = 0
answer_dist_index = 0
answer_func_index = 0

fingers_left = MAX_FINGERS
time_left = ROUND_TIME

game_state = "PLAYING"  # PLAYING, WON, LOST_TIME, LOST_FINGERS
message = ""

# -----------------------------
# CHANGED AS OF 2025-11-20
# -----------------------------
def generate_new_puzzle():
    global answer_dist_index, answer_func_index
    global current_dist_index, current_func_index
    global time_left, game_state, message, fingers_left

    time_left = ROUND_TIME
    game_state = "PLAYING"
    message = ""
    fingers_left = MAX_FINGERS
    current_dist_index = 0
    current_func_index = 0

    answer_dist_index = random.randrange(len(distributions))
    answer_func_index = random.randrange(len(functions))

    base = distributions[answer_dist_index]["ID"]
    fn = functions[answer_func_index]["ID"]
    answer_key = [base, fn]

    return answer_key

def draw_hourglass_bar(screen, x, y, width, height, t_left, t_total):
    ratio = max(0.0, min(1.0, t_left / t_total))
    bg_rect = Rect(x, y, width, height)
    screen.draw.filled_rect(bg_rect, GREY)
    fg_rect = Rect(x, y, width * ratio, height)
    screen.draw.filled_rect(fg_rect, YELLOW)

def update(dt):
    global time_left, game_state, message
    if game_state != "PLAYING":
        return

    time_left -= dt
    if time_left <= 0:
        time_left = 0
        if game_state == "PLAYING":
            game_state = "LOST_TIME"
            message = "The hourglass runs out...The Queen dies. Inigo wins."


def on_key_down(key):
    global current_dist_index, current_func_index
    global game_state, message, fingers_left

    from pygame.locals import (
        K_LEFT,
        K_RIGHT,
        K_UP,
        K_DOWN,
        K_SPACE,
        K_RETURN,
        K_r,
    )

    if key == K_r:
        generate_new_puzzle()
        return

    if game_state != "PLAYING":
        return

    if key == K_LEFT:
        current_dist_index = (current_dist_index - 1) % len(distributions)
    elif key == K_RIGHT:
        current_dist_index = (current_dist_index + 1) % len(distributions)
    elif key == K_UP:
        current_func_index = (current_func_index - 1) % len(functions)
    elif key == K_DOWN:
        current_func_index = (current_func_index + 1) % len(functions)
    elif key in (K_SPACE, K_RETURN):
        check_answer()

# -----------------------------
# 
# -----------------------------
def check_answer():
    global fingers_left, game_state, message

    if (
        current_dist_index == answer_dist_index
        and current_func_index == answer_func_index
    ):
        game_state = "WON"
        message = "Correct! Carlos is recognized as the true heir."
    else:
        fingers_left -= 1
        if fingers_left <= 0:
            game_state = "LOST_FINGERS"
            message = "Wrong again... Carlos loses his last finger and dies."
        else:
            message = (
                "Wrong choice! Carlos loses a finger. Fingers left: "
                + str(fingers_left)
            )


def draw():
    screen.clear()
    screen.fill(BLACK)

    margin = 30
    hist_width = (WIDTH - margin * 3) / 2
    hist_height = 200

    # Target histogram
    screen.draw.text(
        "Target histogram (white) - match this:",
        (WIDTH / 2, margin),
        fontsize=30,
        color=WHITE,
        center=(WIDTH / 2, margin + 10),
    )
    draw_histogram(
        screen,
        target_hist,
        margin,
        margin + 40,
        WIDTH - margin * 2,
        hist_height,
        WHITE,
    )

    # Left lever: distribution
    left_x = margin
    left_y = margin + 40 + hist_height + 60
    screen.draw.text(
        "Lever 1: distribution of X (left/right to change)",
        (left_x, left_y - 40),
        fontsize=24,
        color=BLUE,
    )

    current_dist = distributions[current_dist_index]
    draw_histogram(
        screen,
        current_dist["heights"],
        left_x,
        left_y,
        hist_width,
        hist_height,
        BLUE,
    )

    screen.draw.text(
        "Current: " + current_dist["name"],
        (left_x, left_y + hist_height + 10),
        fontsize=22,
        color=WHITE,
    )

    # Right lever: function
    right_x = margin * 2 + hist_width
    right_y = left_y
    screen.draw.text(
        "Lever 2: function f(x) (up/down to change)",
        (right_x, right_y - 40),
        fontsize=24,
        color=GREEN,
    )

    current_fn = functions[current_func_index]["fn"]
    preview_hist = apply_function_to_hist(current_dist["heights"], current_fn)

    draw_histogram(
        screen,
        preview_hist,
        right_x,
        right_y,
        hist_width,
        hist_height,
        GREEN,
    )

    screen.draw.text(
        "Current: " + functions[current_func_index]["name"],
        (right_x, right_y + hist_height + 10),
        fontsize=22,
        color=WHITE,
    )

    # Bottom info: fingers, time, message
    info_y = HEIGHT - 80

    screen.draw.text(
        "Fingers left: " + str(fingers_left),
        (margin, info_y),
        fontsize=28,
        color=RED,
    )

    draw_hourglass_bar(
        screen,
        WIDTH / 2 - 150,
        info_y + 5,
        300,
        20,
        time_left,
        ROUND_TIME,
    )
    screen.draw.text(
        "Time left: " + str(int(time_left)) + "s",
        (WIDTH / 2 - 60, info_y + 30),
        fontsize=24,
        color=YELLOW,
    )

    if message:
        screen.draw.text(
            message,
            (WIDTH / 2, info_y - 40),
            fontsize=26,
            color=WHITE,
            center=(WIDTH / 2, info_y - 40),
        )

    screen.draw.text(
        "Controls: <-/-> change distribution | up/down change function | "
        "SPACE/ENTER submit | R new puzzle",
        (WIDTH / 2, HEIGHT - 30),
        fontsize=20,
        color=WHITE,
        center=(WIDTH / 2, HEIGHT - 30),
    )

    # End screen overlay
    if game_state in ("WON", "LOST_TIME", "LOST_FINGERS"):
        overlay = Rect(0, 0, WIDTH, HEIGHT)
        screen.draw.filled_rect(overlay, (0, 0, 0, 180))
        if game_state == "WON":
            end_text = "YOU WIN!"
            color = GREEN
        elif game_state == "LOST_TIME":
            end_text = "OUT OF TIME!"
            color = YELLOW
        else:
            end_text = "CARLOS DIES!"
            color = RED

        screen.draw.text(
            end_text,
            center=(WIDTH / 2, HEIGHT / 2 - 30),
            fontsize=60,
            color=color,
        )
        screen.draw.text(
            "Press R to start a new puzzle.",
            center=(WIDTH / 2, HEIGHT / 2 + 40),
            fontsize=30,
            color=WHITE,
        )


# -----------------------------
# START FIRST PUZZLE
# -----------------------------
generate_new_puzzle()
