import random
from pygame import Rect
import pygame
import pgzrun
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
    {"name": "Skewed Left", "image": 'dist_leftskw.png', "ID": 3},
    {"name": "Uniform", "image": 'dist_uniform.png', "ID": 4},
    {"name": "Bimodal (Symmetric)", "image": 'dist_symbimodal.png', "ID": 5},
    {"name": "Bimodal (Non-symmetric)", "image": 'dist_asymbimodal.png', "ID": 6},
]
# Functions
# -----------------------------
# CHANGED AS OF 2025-11-20
# -----------------------------
functions = [
    {"name": "f(x) = x", "image": 'fn_x.png', "ID": 1 },
    {"name": "f(x) = x^2", "image": 'fn_x^2.png', "ID": 2},
    {"name": "f(x) = sqrt(x)", "image": 'fn_sqrt(x).png', "ID": 3},
    {"name": "f(x) = 1 - x", "image": 'fn_1minusx.png', "ID": 4},
]

# Potential Answers
# -----------------------------
# CHANGED AS OF 2025-11-20
# -----------------------------
answers = [
    {"name": "Answer 1", "image": 'ans_bimodal_sym_fn_sqrtx.png', "Dist ID": 5, "Function ID": 3},
    {"name": "Answer 2", "image": 'ans_bimodal_asym_fn_x2.png', "Dist ID": 6, "Function ID": 2},
    {"name": "Answer 3", "image": 'ans_bimodal_sym_fn_x.png', "Dist ID": 5, "Function ID": 1},
    {"name": "Answer 4", "image": 'ans_left_skew_fn_1minusx.png', "Dist ID": 3, "Function ID": 4},
    {"name": "Answer 5", "image": 'ans_left_skew_fn_sqrtx.png', "Dist ID": 3, "Function ID": 3},
    {"name": "Answer 6", "image": 'ans_normal_fn_x.png', "Dist ID": 1, "Function ID": 1},
    {"name": "Answer 7", "image": 'ans_right_skew_fn_x2.png', "Dist ID": 2, "Function ID": 2},
    {"name": "Answer 8", "image": 'ans_uniform_fn_sqrtx.png', "Dist ID": 4, "Function ID": 3},
    {"name": "Answer 9", "image": 'ans_normal_fn_x2.png', "Dist ID": 1, "Function ID": 2},
    {"name": "Answer 10", "image": 'ans_bimodal_asym_fn_1minusx.png', "Dist ID": 6, "Function ID": 4},
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

target_actor = None
current_answer_index = 0

# -----------------------------
# CHANGED AS OF 2025-11-25
# -----------------------------
def generate_new_puzzle():
    global answer_dist_index, answer_func_index
    global current_dist_index, current_func_index
    global time_left, game_state, message, fingers_left, answer_key
    global target_actor, current_answer_index

    time_left = ROUND_TIME
    game_state = "PLAYING"
    message = ""
    fingers_left = MAX_FINGERS
    current_dist_index = 0
    current_func_index = 0

    current_answer_index = random.randrange(len(answers))
    ans = answers[current_answer_index]

    # set the logical answer key (IDs)
    answer_key = [ans["Dist ID"], ans["Function ID"]]

    # build the visual target histogram at the top-center
    img_name = ans["image"]   # e.g. "ans_bimodal_sym_fn_sqrtx.png"
    target_actor = make_scaled_actor(img_name, (WIDTH * 0.5, HEIGHT), 600, 250)

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

    if key == K_a:
        current_dist_index = (current_dist_index - 1) % len(distributions)
    elif key == K_d:
        current_dist_index = (current_dist_index + 1) % len(distributions)
    elif key == K_j:
        current_func_index = (current_func_index - 1) % len(functions)
    elif key == K_l:
        current_func_index = (current_func_index + 1) % len(functions)
    elif key == K_RETURN:
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
    screen.fill(BLACK)

    margin = 30

    # ----- Target title -----
    screen.draw.text(
        "Target histogram: Match It Or Die",
        center=(WIDTH / 2, 40),
        fontsize=30,
        color=WHITE,
    )

    # ----- Target answer image (we'll move this in section 2) -----
    if target_actor is not None:
        target_actor.draw()

    # =====================
    # LEFT LEVER: DISTRIBUTION
    # =====================
    dist_center = (WIDTH * 0.5, HEIGHT * 0.7)   # image center
    dist_image = distributions[current_dist_index]["image"]
    current_dist = make_scaled_actor(dist_image, dist_center, 400, 250)
    current_dist.draw()

    screen.draw.text(
        "Lever 1: distribution of X (A/D to change)",
        center=(dist_center[0] * 0.62, dist_center[1] - 112),
        fontsize=24,
        color=BLUE,
    )

    # =====================
    # RIGHT LEVER: FUNCTION
    # =====================
    fn_center = (WIDTH * 1.2, HEIGHT * 0.86)     # image center
    fn_img = functions[current_func_index]["image"]
    current_fn = make_scaled_actor(fn_img, fn_center, 400, 250)
    current_fn.draw()
    
    screen.draw.text(
        "Lever 2: function f(x) (J/L to change)",
        center=(fn_center[0] * 0.62, fn_center[1] - 230),
        fontsize=24,
        color=GREEN,
    )

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
            center=(WIDTH / 2, info_y - 40),
            fontsize=26,
            color=WHITE,
        )

    screen.draw.text(
        "Controls: A/D change distribution | J/L change function | ENTER submit | R new puzzle",
        center=(WIDTH / 2, HEIGHT - 30),
        fontsize=20,
        color=WHITE,
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

pgzrun.go()