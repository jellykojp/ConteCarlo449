import random
from pygame import Rect
import pygame
import pgzrun


BASE_WIDTH = 1280
BASE_HEIGHT = 720
WIDTH = 1600
HEIGHT = 900
SCALE_X = WIDTH/BASE_WIDTH
SCALE_Y = HEIGHT/BASE_HEIGHT
SCALE = min(SCALE_X,SCALE_Y)

TITLE = "The Countdown of Conte Carlos"

def pos(x, y):
    """Convert base coordinates to actual window coordinates."""
    return (x * SCALE_X, y * SCALE_Y)

def size(w, h):
    """Scale a width/height pair."""
    return (w * SCALE_X, h * SCALE_Y)

def fsize(base_font_size):
    """Scale font size."""
    return int(base_font_size * SCALE_Y)
# -----------------------------
# GAME CONSTANTS
# -----------------------------
MAX_FINGERS = 6
ROUND_TIME = 30  # seconds

# Colors
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
RED     = (220, 60, 60)
GREEN   = (60, 200, 60)
YELLOW  = (230, 200, 25)
GREY    = (60, 60, 60)
BLUE    = (80, 80, 220)

bg_menu = Actor("menu_background.png")
bg_briefing = Actor("main_background.png")
bg_level = Actor("menu_background.png")
bg_lossfing = Actor("lossfingers_background.png")
bg_losstime = Actor("losstime_background.png")
bg_win = Actor("win_background.png")


for bg in (bg_menu, bg_level, bg_lossfing, bg_losstime, bg_win, bg_briefing):
    img = bg._surf  
    original_w = img.get_width()
    original_h = img.get_height()

    scale_w = WIDTH / original_w
    scale_h = HEIGHT / original_h

    scale_factor = min(scale_w, scale_h, 1)   

    new_w = int(original_w * scale_factor)
    new_h = int(original_h * scale_factor)

    img = pygame.transform.smoothscale(img, (new_w, new_h))

    bg._surf = img
    bg._update_pos()
    bg.pos = (WIDTH/1.67, HEIGHT/1.67)

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

in_menu = True
in_briefing = False
current_track = None
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
    target_actor = make_scaled_actor(img_name, (BASE_WIDTH * 0.58, BASE_HEIGHT * 0.92), 600, 250)

def get_current_background():
    if in_menu:
        return bg_menu
    
    if in_briefing:
        return bg_briefing

    # game over states
    if game_state == "WON":
        return bg_win
    if game_state == "LOST_TIME":
        return bg_losstime
    if game_state == "LOST_FINGERS":
        return bg_lossfing

    # default: during puzzle / normal play
    return bg_level

def draw_hourglass_bar(screen, x, y, width, height, t_left, t_total):
    ratio = max(0.0, min(1.0, t_left / t_total))
    bg_rect = Rect(x, y, width, height)
    screen.draw.filled_rect(bg_rect, GREY)
    fg_rect = Rect(x, y, width * ratio, height)
    screen.draw.filled_rect(fg_rect, YELLOW)

def play_music(track, volume=0.5, loop=True):
    global current_track
    if current_track == track:
        return
    
    current_track = track
    music.set_volume(volume)
    if loop:
        music.play(track)
    else:
        music.play_once(track)

def update(dt):
    global time_left, game_state, message
    
    if in_menu or in_briefing:
        return
    
    if game_state != "PLAYING":
        return

    time_left -= dt
    if time_left <= 0:
        time_left = 0
        if game_state == "PLAYING":
            play_music("lose_music.mp3",volume=0.4)
            game_state = "LOST_TIME"
            message = "The hourglass runs out...The Queen dies. Inigo wins."


def on_key_down(key):
    global current_dist_index, current_func_index
    global game_state, message, fingers_left, in_menu, in_briefing

    from pygame.locals import (
        K_SPACE,
        K_RETURN,
        # do something here :P
        K_r,
        K_a,
        K_d,
        K_j,
        K_l,
        K_ESCAPE

    )
    sounds.click_sound.play()
    if in_menu:
        if key == K_RETURN:
            in_menu = False
            in_briefing = True
        return
    
    if in_briefing:
        if key == K_RETURN:
            generate_new_puzzle()
            in_briefing = False
        elif key == K_ESCAPE:
            in_briefing = False
            in_menu = True
        return
    
    if game_state in ("WON", "LOST_TIME", "LOST_FINGERS"):
        if key == K_r:
            in_menu = True
            in_briefing = False
            message = ""
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
    elif key == K_SPACE:
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
        play_music("win_music.mp3",volume=0.4)
    else:
        fingers_left -= 1
        if fingers_left <= 0:
            game_state = "LOST_FINGERS"
            message = "Wrong again... Carlos loses his last finger and dies."
            play_music("lose_music.mp3")
        else:
            message = (
                "Wrong choice! Carlos loses a finger. Fingers left: "
                + str(fingers_left)
            )
# scale the image so its not fugly
def make_scaled_actor(image_name, center, max_width, max_height):
    a = Actor(image_name)

    max_w_px, max_h_px = size(max_width, max_height)

    # Compute scale factor so it fits in the box [max_width x max_height]
    scale = min(max_w_px / a.width, max_h_px / a.height, SCALE)
    if scale != 1.0:
        new_w = int(a.width * scale)
        new_h = int(a.height * scale)
        a._surf = pygame.transform.smoothscale(a._surf, (new_w, new_h))
        a._update_pos()
    
    a.pos = pos(*center)
    return a

# ===================
# Fully Adjusted as of Dec 1
# ====================
def draw():
    screen.clear()
    bg = get_current_background()
    bg.draw()

    if in_menu:
        play_music("menu_music.mp3",volume=0.4)
        title_y = BASE_HEIGHT * 0.3
        screen.draw.text(
            "The Countdown of Conte Carlos",
            center=pos(BASE_WIDTH / 2, title_y),
            fontsize=fsize(60),
            color=WHITE,
            fontname="ruritania.ttf"
        )

        screen.draw.text(
            "A Monte Carlo Guessing Game",
            center=pos(BASE_WIDTH / 2, title_y + 75),
            fontsize=fsize(32),
            color=GREY,
            fontname="oldeenglish.ttf"
        )

        screen.draw.text(
            "Press ENTER to begin",
            center=pos(BASE_WIDTH / 2, title_y + 140),
            fontsize=fsize(36),
            color=YELLOW,
            fontname="cardinal.ttf"
        )

        return
    
    if in_briefing:
        base_y = BASE_HEIGHT * 0.22

        screen.draw.text(
            "Story:",
            topleft=pos(BASE_WIDTH * 0.07, base_y + 70),
            fontsize=fsize(28),
            color=YELLOW,
            fontname="cardinal.ttf",
        )
        screen.draw.text(
            "Carlos has one last chance to prove he is the true heir.\n"
            "He was exiled by his evil twin brother Inigo after being blamed for\n"
            "causing their father's death years ago. Carlos has returned\n"
            "to see his mother who is on her deathbed. Her time is limited, \n"
            "an hourglass of sand is going to determine her passing. Carlos must be\n"
            "recognized by her before that happens, otherwise, Inigo will take the throne.\n"
            "Match the target histogram by choosing the correct distribution of X\n"
            "and the correct transformation f(x). Each wrong guess costs a finger.",
            topleft=pos(BASE_WIDTH * 0.07, base_y + 105),
            fontsize=fsize(22),
            color=WHITE,
            fontname="cardinal.ttf",
        )

        screen.draw.text(
            "Rules:",
            topleft=pos(BASE_WIDTH * 0.55, base_y + 70),
            fontsize=fsize(28),
            color=YELLOW,
            fontname="cardinal.ttf",
        )
        screen.draw.text(
            "1. Look at the target histogram shown at the bottom of the screen.\n"
            "2. Use A / D to cycle the distribution of X on the left.\n"
            "3. Use J / L to cycle the function f(x) on the right.\n"
            "4. Press SPACE to lock in your guess.\n"
            "5. You have 6 fingers (6 wrong guesses) and limited time.",
            topleft=pos(BASE_WIDTH * 0.55, base_y + 105),
            fontsize=fsize(22),
            color=WHITE,
            fontname="cardinal.ttf",
        )

        screen.draw.text(
            "Press ENTER to begin the trial   |   Press ESC to return to Menu",
            center=pos(BASE_WIDTH / 2, BASE_HEIGHT * 0.84),
            fontsize=fsize(24),
            color=YELLOW,
            fontname="cardinal.ttf",
        )
        return
    
    # End screen overlay
    if game_state in ("WON", "LOST_TIME", "LOST_FINGERS"):
        if game_state == "WON":
            end_text = "You Win!"
            color = GREEN
        elif game_state == "LOST_TIME":
            end_text = "Out of Time!"
            color = YELLOW
        else:
            end_text = "Carlos Dies!"
            color = RED

        screen.draw.text(
            end_text,
            center=pos(BASE_WIDTH / 2, HEIGHT / 2 - 30),
            fontsize=fsize(60),
            color=color,
            fontname="cardinal.ttf"
        )
        screen.draw.text(
            "Press R to Return to Menu",
            center=pos(WIDTH / 2, HEIGHT / 2 + 40),
            fontsize=fsize(30),
            color=WHITE,
            fontname="cardinal.ttf"
        )
        return

    margin = 30

    screen.draw.text(
        "Target histogram: Match It Or Die",
        center=pos(BASE_WIDTH / 2, 40),
        fontsize=fsize(30),
        color=WHITE,
        fontname="old europe.ttf"
    )
    
    play_music("menu_music.mp3",volume=0.4)
    if target_actor is not None:
        target_actor.draw()

    # =====================
    # LEFT LEVER: DISTRIBUTION
    # =====================
    dist_center = (BASE_WIDTH * 0.40, BASE_HEIGHT * 0.6)   # image center
    dist_image = distributions[current_dist_index]["image"]
    current_dist = make_scaled_actor(dist_image, dist_center, 400, 250)
    current_dist.draw()

    screen.draw.text(
        "Lever 1: distribution of X (A/D to change)",
        center=pos(BASE_WIDTH * 0.25, BASE_HEIGHT * 0.53),
        fontsize=fsize(24),
        color=BLUE,
        fontname="cardinal.ttf"
    )

    # =====================
    # RIGHT LEVER: FUNCTION
    # =====================
    fn_center = (BASE_WIDTH * 1.08, BASE_HEIGHT * 0.723)     # image center
    fn_img = functions[current_func_index]["image"]
    current_fn = make_scaled_actor(fn_img, fn_center, 400, 250)
    current_fn.draw()
    
    screen.draw.text(
        "Lever 2: function f(x) (J/L to change)",
        center=pos(BASE_WIDTH * 0.73, BASE_HEIGHT * 0.53),
        fontsize=fsize(24),
        color=GREEN,
        fontname="cardinal.ttf"
    )

    info_y = BASE_HEIGHT - 80

    screen.draw.text(
        "Fingers left: " + str(fingers_left),
        pos(margin, info_y),
        fontsize=fsize(28),
        color=RED,
        fontname="old europe.ttf"
    )

    draw_hourglass_bar(
        screen,
        *pos(BASE_WIDTH * 0.75, info_y + 5),
        *(size(300, 20)),
        time_left,
        ROUND_TIME,
)
    screen.draw.text(
        f"Time left: {int(time_left)}s",
        pos(BASE_WIDTH / 1.23, info_y + 30),
        fontsize=fsize(24),
        color=YELLOW,
        fontname="old europe.ttf"
    )

    if message:
        screen.draw.text(
            message,
            center=pos(BASE_WIDTH * 0.22, info_y - 40),
            fontsize=fsize(26),
            color=RED,
            fontname="cardinal.ttf"
        )

    screen.draw.text(
        "Controls: A/D change distribution | J/L change function | SPACE submit",
        center=pos(BASE_WIDTH / 2, BASE_HEIGHT - 22),
        fontsize=fsize(20),
        color=WHITE,
        fontname="cardinal.ttf"
    )


pgzrun.go()