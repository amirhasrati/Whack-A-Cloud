# Clicky Game: Whack-a-mole by Amir Hasrati
import random
import time
import pygame
from pygame.locals import *

pygame.init()

# SCREEN HEIGHT/WIDTH
WIDTH, HEIGHT = (700, 500)
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("WHACK-A-CLOUD")

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (102, 204, 255)
BABY_BLUE = (153, 194, 255)
GREEN = (0, 255, 0)

# MENU VARIABLES
NUM_BUTTONS = 2
BUTTON_DISTANCE_Y = 75
BUTTON_X = 200
BUTTON_Y = 50

# CLOUD VARIABLES
CLOUD_RADIUS = 25
CLOUD_X, CLOUD_Y = (100, 100)
CLOUD_DISTANCE_X = (WIDTH - (CLOUD_X * 2)) / 3
CLOUD_DISTANCE_Y = (HEIGHT - (CLOUD_Y * 2)) / 2
CLOUD_SPEED = 0.6
# ROWS AND COLUMNS
NUM_ROWS = 3
NUM_COLS = 4

# Randomizing the position of the mole/cloud
random_col = random.randrange(0, NUM_COLS)
random_row = random.randrange(0, NUM_ROWS)

# STATS
score = 0
MAX_SCORE = 50
attempts = 0
MAX_ATTEMPTS = 50
num_clicks = 0

running = True
menu = True
game = False
stats = False
is_clicked = False

# FONT
MY_FONT = pygame.font.SysFont('Arial', 25)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Loop until the user clicks the close button.

start = time.time()
# -------- Main Program Loop -----------
while running:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # --- CAPTURE MOUSE CLICKS ---
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            is_clicked = True
            if game is True:
                num_clicks += 1
            # print(f"x: {mouse_x}, y: {mouse_y}")

    if menu is True:
        # MENU LOGIC

        if is_clicked:
            is_clicked_x = (WIDTH - BUTTON_X) / 2 < mouse_x < (WIDTH - BUTTON_X) / 2 + BUTTON_X
            is_clicked_y = HEIGHT / 2 < mouse_y < HEIGHT / 2 + BUTTON_Y

            if is_clicked_x and is_clicked_y:
                game = True
                menu = False
                is_clicked = False
                time.sleep(0.5)

            elif is_clicked:
                is_clicked_x = (WIDTH - BUTTON_X) / 2 < mouse_x < (WIDTH - BUTTON_X) / 2 + BUTTON_X
                is_clicked_y = HEIGHT / 2 - y_offset < mouse_y < HEIGHT / 2 + BUTTON_Y + y_offset
                if is_clicked_x and is_clicked_y:
                    is_clicked = False
                    running = False

        # DRAWING FOR MENU
        SCREEN.fill(BABY_BLUE)

        for buttons in range(NUM_BUTTONS):
            y_offset = buttons * BUTTON_DISTANCE_Y
            pygame.draw.rect(SCREEN, WHITE, ((WIDTH - 200) / 2, HEIGHT / 2 + y_offset, 200, 50))

        # MENU TEXT
        menu_title = MY_FONT.render("WHACK-A-CLOUD", True, (0, 0, 0))
        SCREEN.blit(menu_title, (250, 25))
        # play button
        button_play = MY_FONT.render("PLAY", True, (0, 0, 0))
        SCREEN.blit(button_play, ((WIDTH - 200) / 2, HEIGHT / 2))
        # quit button
        button_quit = MY_FONT.render("QUIT", True, (0, 0, 0))
        SCREEN.blit(button_quit, ((WIDTH - 200) / 2, HEIGHT / 2 + y_offset))

    elif game is True:
        # --- Game logic should go here
        if attempts == MAX_ATTEMPTS or score == MAX_SCORE:
            game = False
            stats = True

        if is_clicked:
            is_clicked_x = mole_x - CLOUD_RADIUS < mouse_x < mole_x + CLOUD_RADIUS
            is_clicked_y = mole_y - CLOUD_RADIUS < mouse_y < mole_y + CLOUD_RADIUS
            if is_clicked_x and is_clicked_y:
                score += 1
                is_clicked = False

        # --- Drawing code should go here
        SCREEN.fill(SKY_BLUE)

        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                x_offset = col * CLOUD_DISTANCE_X
                y_offset = row * CLOUD_DISTANCE_Y
                pygame.draw.circle(SCREEN, WHITE, (CLOUD_X + x_offset, CLOUD_Y + y_offset), CLOUD_RADIUS * 2)

        end = time.time()
        if end - start >= CLOUD_SPEED:
            random_col = random.randrange(0, NUM_COLS)
            random_row = random.randrange(0, NUM_ROWS)
            start = time.time()
            end = time.time()
            attempts += 1

        mole_x = CLOUD_X + random_col * CLOUD_DISTANCE_X
        mole_y = CLOUD_Y + random_row * CLOUD_DISTANCE_Y
        mole = pygame.draw.circle(SCREEN, BABY_BLUE, (mole_x, mole_y), CLOUD_RADIUS)

        # DISPLAY SCORE
        score_text = MY_FONT.render(f"SCORE: {str(score)}", True, (0, 0, 0))
        SCREEN.blit(score_text, (285, 10))

    elif stats is True:

        # STATS LOGIC
        accuracy = score / num_clicks * 100

        # DRAWING FOR STATS
        SCREEN.fill(BABY_BLUE)

        final_score = MY_FONT.render(f"SCORE: {str(score)}/{attempts}", True, (0, 0, 0))
        SCREEN.blit(final_score, (100, 100))

        accuracy_text = MY_FONT.render(f"ACCURACY: {str(round(accuracy, 4))}", True, (0, 0, 0))
        SCREEN.blit(accuracy_text, (100, 150))
    # --- Go  ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

print(f"score: {score}, attempts: {attempts}")

# Close the window and quit.
pygame.quit()