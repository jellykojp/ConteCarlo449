import random
from pygame import Rect
import pygame
# -----------------------------
# BASIC PYGAME ZERO SETTINGS
# -----------------------------
WIDTH = 1280
HEIGHT = 720
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
    {"name": "Normal Distribution","image": 'dist_normal.png',"ID": 1},
    {"name": "Skewed Right", "image": 'dist_rightskw.png', "ID": 2},
    #{"name": "Skewed Left", "image": 'dist_skw_left.png', "ID": 3},
    #{"name": "Uniform", "image": 'dist_uniform.png', "ID": 4},
    #{"name": "Bimodal (Symmetric)", "image": 'dist_bimodal_sym.png', "ID": 5},
    #{"name": "Bimodal (Non-symmetric)", "image": 'dist_bimodal_sym.png', "ID": 6},
]
# Functions
# -----------------------------
# CHANGED AS OF 2025-11-20
# -----------------------------
functions = [
    {"name": "f(x) = x", "image": 'fn_x.png', "ID": 1 },
    {"name": "f(x) = x^2", "image": 'fn_x^2.png', "ID": 2},
    {"name": "f(x) = sqrt(x)", "image": 'fn_sqrt(x).png', "ID": 3},
    {"name": "f(x) = 1 - x", "image": 'fn_1minusx.png', "ID": 4}
]

# Potential Answers
# -----------------------------
# CHANGED AS OF 2025-11-20
# -----------------------------
answers = [
    {"name": "Answer 1", "image": '', "Dist ID": 1, "Function ID": 1},
    {"name": "Answer 2", "image": '', "Dist ID": 5, "Function ID": 3},
]

# -----------------------------
# GAME STATE
# -----------------------------
current_dist_index = 0
current_func_index = 0
answer_dist_index = 0
answer_func_index = 0

answer_key = []

fingers_left = MAX_FINGERS
time_left = ROUND_TIME

game_state = "PLAYING"  # PLAYING, WON, LOST_TIME, LOST_FINGERS
message = ""

# -----------------------------
# CHANGED AS OF 2025-11-25
# -----------------------------
def generate_new_puzzle():
    global answer_dist_index, answer_func_index
    global current_dist_index, current_func_index
    global time_left, game_state, message, fingers_left, answer_key

    time_left = ROUND_TIME
    game_state = "PLAYING"
    message = ""
    fingers_left = MAX_FINGERS
    current_dist_index = 0
    current_func_index = 0

    answer_index = random.randrange(len(answers))

    answer_key = [answers[answer_index]["Dist ID"], answers[answer_index]["Function ID"]]

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
        # do something here :P
        K_r,
        K_a,
        K_d,
        K_j,
        K_l,

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
# Check Answer Function
# -----------------------------
def check_answer():
    global fingers_left, game_state, message

    guess = [distributions[current_dist_index]["ID"], functions[current_func_index]["ID"]]

    if guess == answer_key:
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
# scale the image so its not fugly
def make_scaled_actor(image_name, center, max_width, max_height):
    a = Actor(image_name)
    # Compute scale factor so it fits in the box [max_width x max_height]
    scale = min(max_width / a.width, max_height / a.height, 1.0)
    if scale < 1.0:
        new_w = int(a.width * scale)
        new_h = int(a.height * scale)
        a._surf = pygame.transform.smoothscale(a._surf, (new_w, new_h))
        a._update_pos()  # internal, but works fine
    a.pos = center
    return a

# ===================
# Need to adjust still
# ====================
def draw():
    screen.clear()
    screen.fill(BLACK) # currently a black background

    margin = 30
    hist_width = (WIDTH - margin * 3) / 2
    hist_height = 200

    # Target histogram
    screen.draw.text(
        "Target histogram: Match It Or Die",
        (WIDTH / 2, margin),
        fontsize=30,
        color=WHITE,
        center=(WIDTH / 2, margin + 10),
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

    # Distribution Image
    dist_image = distributions[current_dist_index]["image"]
    current_dist = make_scaled_actor(dist_image, (WIDTH * 0.25, HEIGHT * 0.65, 400, 250))
    current_dist.draw()

    # Right lever: function
    right_x = margin * 2 + hist_width
    right_y = left_y
    screen.draw.text(
        "Lever 2: function f(x) (up/down to change)",
        (right_x, right_y - 40),
        fontsize=24,
        color=GREEN,
    )
    
    # Function Image
    fn_img = functions[current_func_index]["image"]
    current_fn = make_scaled_actor(fn_img, (WIDTH * 0.75, HEIGHT * 0.65), 400, 250)
    current_fn.draw()

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