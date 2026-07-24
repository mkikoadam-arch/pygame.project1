import pygame
import random
import sys

# ============================
# PART 1 - INITIALIZATION
# ============================

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("game_music.mp3")
winner_sound = pygame.mixer.Sound("winner.wav")
lose_sound = pygame.mixer.Sound("lose.wav")

# ============================
# PART 2 - SETTINGS
# ============================

WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20
ROWS = WIDTH // CELL_SIZE

FPS = 10

# ============================
# PART 3 - COLORS
# ============================

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
GREEN = (0, 220, 0)
DARK_GREEN = (0, 170, 0)
RED = (230, 60, 60)
YELLOW = (255, 220, 0)
GRAY = (120, 120, 120)

# ============================
# PART 4 - SCREEN
# ============================

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 60)

winner_image = pygame.image.load("winner.jpg")
winner_image = pygame.transform.scale(winner_image, (400,250))

# ============================
# PART 5 - GAME VARIABLES
# ============================

snake = [
    [10, 10],
    [9, 10],
    [8, 10]
]

direction = "RIGHT"
next_direction = "RIGHT"

food = [
    random.randint(0, ROWS - 1),
    random.randint(0, ROWS - 1)
]

score = 0
running = True

# ============================
# PART 6 - START MENU
# ============================

def start_menu():
    
    pygame.mixer.music.play(-1)


    while True:

        screen.fill((20, 30, 60))

        title = big_font.render("SNAKE GAME", True, GREEN)
        screen.blit(title, (120, 90))

        welcome = font.render(
            "Welcome to Snake Game!",
            True,
            YELLOW
        )

        screen.blit(welcome, (140, 180))

        start = font.render(
            "Press ENTER to Start",
            True,
            WHITE
        )

        screen.blit(start, (150, 280))

        quit_text = font.render(
            "Press ESC to Exit",
            True,
            RED
        )

        screen.blit(quit_text, (165, 330))

        creator = font.render(
            "Created by Adam",
            True,
            GRAY
        )

        screen.blit(creator, (185, 500))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()



# ============================
# PART 7 - DRAW GAME
# ============================

def draw_game():

    # Background
    screen.fill(BLACK)

    # Draw Apple
    pygame.draw.circle(
        screen,
        RED,
        (
            food[0] * CELL_SIZE + CELL_SIZE // 2,
            food[1] * CELL_SIZE + CELL_SIZE // 2
        ),
        CELL_SIZE // 2 - 2
    )

    # Apple Leaf
    pygame.draw.rect(
        screen,
        GREEN,
        (
            food[0] * CELL_SIZE + 8,
            food[1] * CELL_SIZE + 1,
            4,
            6
        )
    )

    # Draw Snake
    for i, block in enumerate(snake):

        x = block[0] * CELL_SIZE
        y = block[1] * CELL_SIZE

        # Snake Head
        if i == 0:

            pygame.draw.rect(
                screen,
                DARK_GREEN,
                (x, y, CELL_SIZE, CELL_SIZE),
                border_radius=5
            )

            # Eyes
            pygame.draw.circle(screen, WHITE, (x+6, y+6), 2)
            pygame.draw.circle(screen, WHITE, (x+14, y+6), 2)

            pygame.draw.circle(screen, BLACK, (x+6, y+6), 1)
            pygame.draw.circle(screen, BLACK, (x+14, y+6), 1)

        # Snake Body
        else:

            pygame.draw.rect(
                screen,
                GREEN,
                (x, y, CELL_SIZE, CELL_SIZE),
                border_radius=4
            )

            pygame.draw.rect(
                screen,
                DARK_GREEN,
                (x+3, y+3, CELL_SIZE-6, CELL_SIZE-6),
                border_radius=3
            )

    # Score
    score_text = font.render(
        f"Score : {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (10,10))

    pygame.display.update()


# ============================
# PART 8 - MOVE SNAKE
# ============================
def move_snake():

    global score
    global food
    global running

    head = snake[0].copy()

    if direction == "UP":
        head[1] -= 1

    elif direction == "DOWN":
        head[1] += 1

    elif direction == "LEFT":
        head[0] -= 1

    elif direction == "RIGHT":
        head[0] += 1

    snake.insert(0, head)

    if head == food:

        score += 1

        # Win after 10 apples
        if score >= 10:
            pygame.mixer.music.stop()
            winner_sound.play()
            winner_screen()
            running = False
            return

        while True:

            food = [
                random.randint(0, ROWS - 1),
                random.randint(0, ROWS - 1)
            ]

            if food not in snake:
                break

    else:
        snake.pop()

def winner_screen():

    screen.fill((20,120,20))

    if winner_image:
        screen.blit(winner_image, (100,100))
    else:
        text = big_font.render("YOU WIN!", True, YELLOW)
        screen.blit(text, (150,200))

    score_text = font.render(
        f"Final Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (200,320))

    pygame.display.update()

    pygame.time.wait(5000)


# ============================
# PART 9 - GAME OVER SCREEN
# ============================

def game_over_screen():

    pygame.mixer.music.stop()
    lose_sound.play()

    while True:

        screen.fill(BLACK)

        title = big_font.render("GAME OVER", True, RED)
        screen.blit(title, (120, 150))

        score_text = font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        screen.blit(score_text, (180, 250))

        restart = font.render(
            "Press R to Restart",
            True,
            GREEN
        )

        screen.blit(restart, (150, 320))

        exit_text = font.render(
            "Press ESC to Exit",
            True,
            RED
        )

        screen.blit(exit_text, (165, 370))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# ============================
# PART 10 - MAIN GAME LOOP
# ============================

start_menu()

while running:

    clock.tick(FPS)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and direction != "DOWN":
                next_direction = "UP"

            elif event.key == pygame.K_DOWN and direction != "UP":
                next_direction = "DOWN"

            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                next_direction = "LEFT"

            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                next_direction = "RIGHT"

    direction = next_direction

    move_snake()

    head = snake[0]

    # Wall Collision
    if (
        head[0] < 0
        or head[0] >= ROWS
        or head[1] < 0
        or head[1] >= ROWS
    ):

        if game_over_screen():

            snake = [
                [10,10],
                [9,10],
                [8,10]
            ]

            direction = "RIGHT"
            next_direction = "RIGHT"

            food = [
                random.randint(0, ROWS-1),
                random.randint(0, ROWS-1)
            ]

            score = 0

            continue

    # Snake hits itself
    if head in snake[1:]:

        if game_over_screen():

            snake = [
                [10,10],
                [9,10],
                [8,10]
            ]

            direction = "RIGHT"
            next_direction = "RIGHT"

            food = [
                random.randint(0, ROWS-1),
                random.randint(0, ROWS-1)
            ]

            score = 0

            continue

    draw_game()

pygame.quit()
sys.exit()