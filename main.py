import pygame
import os
from bot import bot

# Assets managers initialization
pygame.mixer.init()
pygame.font.init()

# Window constants
WIDTH, HEIGHT = 900, 500
MENU_WIDTH, MENU_HEIGHT = 300, 500

# Window initialization
WIN = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pygame.display.set_caption("Space Duel Menu")

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (80, 80, 255)

# Pillar in the center of the game
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Importing the sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "grenade.wav"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "gun_silencer.wav"))

# Setting up the fonts
TITLE_FONT = pygame.font.SysFont("freemono", 30)
WINNER_FONT = pygame.font.SysFont("freemono", 80)

# Gameplay constants
FPS = 50
VEL = 5
BULLET_VEL = 9
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (
    48,
    40,
)  # Original image: w 500px h 413px, keeping aspect ratio of 1.21

# Events for when a bullet hits a player
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Spaceships (players) images importation and parsing
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90,
)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270,
)

# Background image
SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
)

# Facilitates the text drawing
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Drawing the game
def draw_game(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = TITLE_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = TITLE_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


# Handling player movement
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 5:  # down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 5:  # down
        red.y += VEL


# Handle bullets movement and collision
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# Displaying the winner announcement
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


# Diaplays the main menu
def main_menu():
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        WIN.blit(SPACE, (0, 0), (0, 0, MENU_WIDTH, MENU_HEIGHT))

        draw_text("main menu", TITLE_FONT, WHITE, WIN, 20, 20)

        mx, my = pygame.mouse.get_pos()

        pvp_btn = pygame.Rect(20, 100, 200, 50)
        pve_btn = pygame.Rect(20, 190, 200, 50)

        pygame.draw.rect(WIN, BLUE, pvp_btn)
        pygame.draw.rect(WIN, BLUE, pve_btn)

        draw_text("PvP", TITLE_FONT, WHITE, WIN, pvp_btn.x + 10, pvp_btn.y + 10)
        draw_text("PvE", TITLE_FONT, WHITE, WIN, pve_btn.x + 10, pve_btn.y + 10)

        if pvp_btn.collidepoint((mx, my)):
            if click:
                game("pvp")

        if pve_btn.collidepoint((mx, my)):
            if click:
                game("pve")

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


# Diaplays the game, the arg can be "pve" or "pvp". PvP is vs another player and PvE is against an AI
def game(gamemode):
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Duel")

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if (
                    event.key == pygame.K_RCTRL
                    and len(red_bullets) < MAX_BULLETS
                    and gamemode == "pvp"
                ):
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)

        if gamemode == "pvp":
            red_handle_movement(keys_pressed, red)
        else:
            red_bullets = bot(red, yellow, yellow_bullets, red_bullets)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_game(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    game(gamemode)


def main():
    main_menu()


if __name__ == "__main__":
    main()
