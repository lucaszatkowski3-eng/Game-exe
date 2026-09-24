import pygame
import random
import sys

pygame.init()

# =========================
# EINSTELLUNGEN
# =========================

WIDTH = 1000
HEIGHT = 650
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Runner")

clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (10, 10, 18)
CYAN = (0, 220, 255)
YELLOW = (255, 220, 0)
RED = (255, 70, 70)
PURPLE = (170, 70, 255)
GRAY = (80, 80, 95)
GREEN = (50, 220, 120)

font_big = pygame.font.SysFont("arial", 60, bold=True)
font = pygame.font.SysFont("arial", 30, bold=True)
font_small = pygame.font.SysFont("arial", 22)

# =========================
# SPIELER
# =========================

LANES = [300, 500, 700]

player_width = 55
player_height = 80

player_lane = 1
player_x = LANES[player_lane]
player_y = HEIGHT - 150

player_velocity_y = 0
gravity = 1.2
jump_strength = -20

on_ground = True

# =========================
# SPIELDATEN
# =========================

score = 0
coins = 0
speed = 8

game_over = False

obstacles = []
coin_objects = []

spawn_timer = 0
coin_timer = 0

# =========================
# HILFSFUNKTIONEN
# =========================

def draw_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
    else:
        rect = surface.get_rect(topleft=(x, y))

    screen.blit(surface, rect)


def reset_game():
    global player_lane
    global player_x
    global player_y
    global player_velocity_y
    global on_ground
    global score
    global coins
    global speed
    global obstacles
    global coin_objects
    global spawn_timer
    global coin_timer
    global game_over

    player_lane = 1
    player_x = LANES[player_lane]
    player_y = HEIGHT - 150

    player_velocity_y = 0
    on_ground = True

    score = 0
    coins = 0
    speed = 8

    obstacles = []
    coin_objects = []

    spawn_timer = 0
    coin_timer = 0

    game_over = False


def create_obstacle():
    lane = random.randint(0, 2)

    obstacle = {
        "x": LANES[lane] - 35,
        "y": -100,
        "width": 70,
        "height": 70,
        "lane": lane
    }

    obstacles.append(obstacle)


def create_coin():
    lane = random.randint(0, 2)

    coin = {
        "x": LANES[lane],
        "y": -30,
        "radius": 14,
        "lane": lane
    }

    coin_objects.append(coin)


def draw_background():
    screen.fill(BLACK)

    # Himmel
    pygame.draw.rect(
        screen,
        (15, 15, 35),
        (0, 0, WIDTH, HEIGHT)
    )

    # Gebäude
    for x in range(0, WIDTH, 100):
        height = random.Random(x).randint(100, 250)

        pygame.draw.rect(
            screen,
            (25, 25, 50),
            (x, 250 - height, 80, height)
        )

    # Straße
    pygame.draw.polygon(
        screen,
        (35, 35, 45),
        [
            (180, HEIGHT),
            (820, HEIGHT),
            (620, 250),
            (380, 250)
        ]
    )

    # Fahrbahnlinien
    for lane_x in [400, 600]:
        pygame.draw.line(
            screen,
            (100, 100, 120),
            (lane_x, 250),
            (lane_x, HEIGHT),
            4
        )


def draw_player():
    # Körper
    pygame.draw.rect(
        screen,
        CYAN,
        (
            player_x - player_width // 2,
            player_y,
            player_width,
            player_height
        ),
        border_radius=12
    )

    # Kopf
    pygame.draw.circle(
        screen,
        WHITE,
        (player_x, player_y - 15),
        25
    )

    # Augen
    pygame.draw.circle(
        screen,
        BLACK,
        (player_x - 8, player_y - 18),
        4
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (player_x + 8, player_y - 18),
        4
    )


def draw_obstacles():
    for obstacle in obstacles:

        pygame.draw.rect(
            screen,
            RED,
            (
                obstacle["x"],
                obstacle["y"],
                obstacle["width"],
                obstacle["height"]
            ),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (
                obstacle["x"] + 10,
                obstacle["y"] + 10,
                obstacle["width"] - 20,
                8
            )
        )


def draw_coins():
    for coin in coin_objects:

        pygame.draw.circle(
            screen,
            YELLOW,
            (coin["x"], int(coin["y"])),
            coin["radius"]
        )

        pygame.draw.circle(
            screen,
            (255, 245, 120),
            (coin["x"], int(coin["y"])),
            7
        )


# =========================
# HAUPTSCHLEIFE
# =========================

while True:

    clock.tick(FPS)

    # -------------------------
    # EVENTS
    # -------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if not game_over:

                # Links
                if event.key in [pygame.K_LEFT, pygame.K_a]:

                    if player_lane > 0:
                        player_lane -= 1

                # Rechts
                if event.key in [pygame.K_RIGHT, pygame.K_d]:

                    if player_lane < 2:
                        player_lane += 1

                # Springen
                if event.key in [pygame.K_SPACE, pygame.K_UP]:

                    if on_ground:
                        player_velocity_y = jump_strength
                        on_ground = False

            else:

                # Neustart
                if event.key == pygame.K_r:
                    reset_game()

    # -------------------------
    # SPIEL AKTUALISIEREN
    # -------------------------

    if not game_over:

        # Spieler bewegt sich zur neuen Spur
        target_x = LANES[player_lane]

        player_x += (target_x - player_x) * 0.25

        # Springen
        player_velocity_y += gravity
        player_y += player_velocity_y

        ground_y = HEIGHT - 150

        if player_y >= ground_y:

            player_y = ground_y
            player_velocity_y = 0
            on_ground = True

        # Geschwindigkeit erhöhen
        speed += 0.002

        # Hindernisse erzeugen
        spawn_timer += 1

        if spawn_timer > max(25, 70 - int(speed * 2)):

            create_obstacle()
            spawn_timer = 0

        # Münzen erzeugen
        coin_timer += 1

        if coin_timer > 45:

            create_coin()
            coin_timer = 0

        # Hindernisse bewegen
        for obstacle in obstacles:

            obstacle["y"] += speed

        # Münzen bewegen
        for coin in coin_objects:

            coin["y"] += speed

        # Alte Objekte entfernen
        obstacles = [
            obstacle
            for obstacle in obstacles
            if obstacle["y"] < HEIGHT + 100
        ]

        coin_objects = [
            coin
            for coin in coin_objects
            if coin["y"] < HEIGHT + 50
        ]

        # -------------------------
        # KOLLISION
        # -------------------------

        player_rect = pygame.Rect(
            player_x - 25,
            player_y,
            50,
            80
        )

        for obstacle in obstacles:

            obstacle_rect = pygame.Rect(
                obstacle["x"],
                obstacle["y"],
                obstacle["width"],
                obstacle["height"]
            )

            if player_rect.colliderect(obstacle_rect):

                game_over = True

        # -------------------------
        # MÜNZEN
        # -------------------------

        for coin in coin_objects:

            distance_x = abs(player_x - coin["x"])
            distance_y = abs((player_y + 40) - coin["y"])

            if distance_x < 40 and distance_y < 50:

                coins += 1
                coin_objects.remove(coin)
                break

        # Punkte
        score += 1

    # =========================
    # ZEICHNEN
    # =========================

    draw_background()

    draw_coins()
    draw_obstacles()
    draw_player()

    # HUD

    draw_text(
        f"Score: {score}",
        font,
        WHITE,
        25,
        20
    )

    draw_text(
        f"Münzen: {coins}",
        font,
        YELLOW,
        25,
        60
    )

    draw_text(
        f"Speed: {speed:.1f}",
        font_small,
        CYAN,
        25,
        105
    )

    # Game Over

    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)

        screen.blit(overlay, (0, 0))

        draw_text(
            "GAME OVER",
            font_big,
            RED,
            WIDTH // 2,
            250,
            center=True
        )

        draw_text(
            f"Score: {score}",
            font,
            WHITE,
            WIDTH // 2,
            330,
            center=True
        )

        draw_text(
            f"Münzen: {coins}",
            font,
            YELLOW,
            WIDTH // 2,
            375,
            center=True
        )

        draw_text(
            "Drücke R zum Neustarten",
            font_small,
            WHITE,
            WIDTH // 2,
            440,
            center=True
        )

    pygame.display.flip()
