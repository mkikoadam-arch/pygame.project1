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
# LEVEL SYSTEM
# ============================

current_level = 1
highest_level = 1

level_goals = {
    1: 8,
    2: 10,
    3: 12,
    4: 15,
    5: 18,
    6: 20,
    7: 22,
    8: 25,
    9: 28,
    10: 30
}


# Golden Apple
golden_food = [
    random.randint(0, ROWS - 1),
    random.randint(0, ROWS - 1)
]

golden_visible = True

# ============================
# POISON FRUIT
# ============================

poison_food = [
    random.randint(0, ROWS - 1),
    random.randint(0, ROWS - 1)
]

poison_visible = True

normal_fps = 10
slow_fps = 5

poison_timer = 0

star_food = [
    random.randint(0, ROWS - 1),
    random.randint(0, ROWS - 1)
]

star_visible = True

# ============================
# STAR POWER
# ============================

star_food = [
    random.randint(0, ROWS - 1),
    random.randint(0, ROWS - 1)
]

star_visible = True

power_mode = False
power_timer = 0


# ============================
# ENEMY SNAKE
# ============================

enemy_snake = [
    [20, 20],
    [21, 20],
    [22, 20]
]

enemy_direction = "LEFT"

# Pause button
pause_button = pygame.Rect(550, 10, 40, 40)


# ============================
# PART 7 - DRAW GAME
# ============================

def start_menu():

    global current_level

    selected = 1

    pygame.mixer.music.play(-1)

    while True:

        for y in range(HEIGHT):
            color = (
                20,
                30 + y // 8,
                80 + y // 6
            )
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

            pygame.draw.rect(
                screen,
                (30,40,80),
                (50,25,500,90),
                border_radius=25
            )

            pygame.draw.rect(
                screen,
                YELLOW,
                (50,25,500,90),
                5,
                border_radius=25
            )
        shadow = big_font.render("SNAKE ADVENTURE", True, BLACK)
        shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 3, 68))
        screen.blit(shadow, shadow_rect)
        title = big_font.render("SNAKE ADVENTURE", True, GREEN)
        title_rect = title.get_rect(center=(WIDTH // 2, 65))
        screen.blit(title, title_rect)

        info = font.render("Choose a Level", True, WHITE)

        info_rect = info.get_rect(center=(WIDTH // 2, 150))

        screen.blit(info, info_rect)

        for level in range(1,11):

            if level == selected:
                color = YELLOW
                arrow = ">"
            else:
                color = WHITE
                arrow = " "

            if level <= highest_level:
                status = "UNLOCKED"
            else:
                status = "LOCKED"

            button_y = 170 + (level - 1) * 42
            button = pygame.Rect(110, button_y, 380, 35)

            if level == selected:
                pygame.draw.rect(screen, YELLOW, button, border_radius=12)
                pygame.draw.rect(screen, WHITE, button, 3, border_radius=12)
                text_color = BLACK
            else:
                pygame.draw.rect(screen, (40, 50, 90), button, border_radius=12)
                pygame.draw.rect(screen, (90, 120, 255), button, 2, border_radius=12)
                text_color = WHITE

            text = font.render(
                f"Level {level}   {status}",
                True,
                text_color
            )

            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)
       

        pygame.display.update()     

        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:

                        if selected > 1:
                            selected -= 1

                    elif event.key == pygame.K_DOWN:

                        if selected < 10:
                            selected += 1

                    elif event.key == pygame.K_RETURN:

                        if selected <= highest_level:

                            current_level = selected
                            return

                    elif event.key == pygame.K_ESCAPE:

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
    if golden_visible:

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                golden_food[0] * CELL_SIZE + CELL_SIZE // 2,
                golden_food[1] * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 2 - 2
        )

    if poison_visible:
        pygame.draw.circle(
            screen,
            (180, 0, 180),   # purple
            (
                poison_food[0] * CELL_SIZE + CELL_SIZE // 2,
                poison_food[1] * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 2 - 2
        )
    if star_visible:
        cx = star_food[0] * CELL_SIZE + CELL_SIZE // 2
        cy = star_food[1] * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.polygon(
            screen,
            YELLOW,
            [
                (cx, cy-9),
                (cx+3, cy-3),
                (cx+9, cy-3),
                (cx+4, cy+2),
                (cx+6, cy+9),
                (cx, cy+5),
                (cx-6, cy+9),
                (cx-4, cy+2),
                (cx-9, cy-3),
                (cx-3, cy-3)
            ]
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
    for block in enemy_snake:

        pygame.draw.rect(
            screen,
            RED,
            (
                block[0] * CELL_SIZE,
                block[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            ),
            border_radius=4
        )
    # Score
    score_text = font.render(
        f"Score : {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (10,10))

   

    pygame.draw.rect(screen, GRAY, pause_button, border_radius=8)

    # left bar
    pygame.draw.rect(screen, WHITE, (560, 18, 6, 24))
    #Right bar
    pygame.draw.rect(screen, WHITE, (574, 18, 6, 24))
    pygame.display.update()


# ============================
# PART 8 - MOVE SNAKE
# ============================
def move_snake():
    global golden_food
    global golden_visible   
    global score
    global food
    global running
    global poison_food
    global poison_visible
    global poison_timer
    global power_mode
    global power_timer
    global star_visible
    global enemy_snake
    global star_food

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
        if score >= level_goals[current_level]:

            level_complete()

            return

        while True:

            food = [
                random.randint(0, ROWS - 1),
                random.randint(0, ROWS - 1)
            ]

            # Golden Apple
            golden_food = [
                random.randint(0, ROWS - 1),
                random.randint(0, ROWS - 1)
            ]

            golden_visible = True

            # Poison Fruit
            poison_food = [
                random.randint(0, ROWS - 1),
                random.randint(0, ROWS - 1)
            ]

            poison_visible = True
                        # Make the star appear again
            if not star_visible:
                star_food = [
                    random.randint(0, ROWS - 1),
                    random.randint(0, ROWS - 1)
                ]
                star_visible = True

            if food not in snake:
                break

    elif golden_visible and head == golden_food:

        score += 3
        golden_visible = False

    elif poison_visible and head == poison_food:

        poison_visible = False
        poison_timer = pygame.time.get_ticks()

    elif star_visible and head == star_food:

        star_visible = False
        power_mode = True
        power_timer = pygame.time.get_ticks()

        # Create the next star
        star_food = [
            random.randint(0, ROWS - 1),
            random.randint(0, ROWS - 1)
        ]
    else:
        snake.pop()

def move_enemy():

    global enemy_direction

    # Randomly change direction
    if random.randint(1, 10) == 1:
        enemy_direction = random.choice(
            ["UP", "DOWN", "LEFT", "RIGHT"]
        )

    head = enemy_snake[0].copy()

    # Move enemy
    if enemy_direction == "UP":
        head[1] -= 1

    elif enemy_direction == "DOWN":
        head[1] += 1

    elif enemy_direction == "LEFT":
        head[0] -= 1

    elif enemy_direction == "RIGHT":
        head[0] += 1

    # Keep enemy inside the map
    if head[0] < 0:
        head[0] = 0
        enemy_direction = "RIGHT"

    elif head[0] >= ROWS:
        head[0] = ROWS - 1
        enemy_direction = "LEFT"

    if head[1] < 0:
        head[1] = 0
        enemy_direction = "DOWN"

    elif head[1] >= ROWS:
        head[1] = ROWS - 1
        enemy_direction = "UP"

    # Move the enemy snake
    enemy_snake.insert(0, head)
    enemy_snake.pop()

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

def level_complete():

    global current_level
    global highest_level
    global score
    global snake
    global food
    global direction
    global next_direction

    pygame.mixer.music.stop()
    winner_sound.play()

    screen.fill((20, 100, 20))

    title = big_font.render("LEVEL COMPLETE!", True, YELLOW)
    screen.blit(title, (70, 120))

    if current_level < 10:
        highest_level = max(highest_level, current_level + 1)

        text = font.render(
            f"Level {current_level + 1} Unlocked!",
            True,
            WHITE
        )
        screen.blit(text, (120, 220))
    else:
        text = font.render(
            "You finished the game!",
            True,
            WHITE
        )
        screen.blit(text, (120, 220))

    text2 = font.render(
        "Press ENTER",
        True,
        GREEN
    )
    screen.blit(text2, (180, 320))

    pygame.display.update()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    score = 0

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

                    if current_level < 10:
                        highest_level = max(highest_level, current_level + 1)

                    pygame.mixer.music.play(-1)

                    start_menu()

                    return
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

#PAUSE MENU 

def pause_menu():

    while True:

        screen.fill((30, 30, 30))

        title = big_font.render("PAUSED", True, YELLOW)
        screen.blit(title, (180, 180))

        text = font.render("Press P to Resume", True, WHITE)
        screen.blit(text, (170, 280))

        text2 = font.render("Press ESC to Quit", True, RED)
        screen.blit(text2, (175, 330))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    return

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# ============================
# PART 10 - MAIN GAME LOOP
# ============================

start_menu()

while running:

    current_fps = normal_fps

    if poison_timer != 0:
        if pygame.time.get_ticks() - poison_timer < 5000:
            current_fps = slow_fps
        else:
            poison_timer = 0

    clock.tick(current_fps)
    if power_mode:

        if pygame.time.get_ticks() - power_timer > 8000:
            power_mode = False

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
            elif event.key == pygame.K_p:
                pause_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if pause_button.collidepoint(event.pos):
                    pause_menu()

    direction = next_direction

    move_snake()
    move_enemy()    

    head = snake[0]

    if head in enemy_snake:
        if power_mode:

            score += 5          # Bonus points

            enemy_snake = [
                [random.randint(5, ROWS - 5), random.randint(5, ROWS - 5)],
                [random.randint(5, ROWS - 5), random.randint(5, ROWS - 5)],
                [random.randint(5, ROWS - 5), random.randint(5, ROWS - 5)]
            ]

            power_mode = False



        else:

            if game_over_screen():

                snake = [
                    [10,10],
                    [9,10],
                    [8,10]
                ]

                direction = "RIGHT"
                next_direction = "RIGHT"
                score = 0

    

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