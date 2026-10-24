import pygame
import random
import sys

# ---------------------------- Configuration ----------------------------
pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 28
PANEL_HEIGHT = 90
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + PANEL_HEIGHT
FPS = 9

# Modern neon palette
BG = (10, 14, 28)
BOARD_BG = (15, 22, 41)
GRID = (25, 35, 57)
WHITE = (238, 244, 255)
MUTED = (143, 158, 185)
GREEN = (71, 231, 160)
GREEN_DARK = (27, 155, 112)
RED = (255, 91, 112)
GOLD = (255, 205, 92)
PANEL = (18, 25, 45)
PANEL_BORDER = (42, 57, 87)
BLUE = (104, 164, 255)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("NEON SNAKE")
clock = pygame.time.Clock()

FONT_SMALL = pygame.font.SysFont("segoeui", 17)
FONT_MED = pygame.font.SysFont("segoeui", 23, bold=True)
FONT_BIG = pygame.font.SysFont("segoeui", 42, bold=True)
FONT_TITLE = pygame.font.SysFont("segoeui", 28, bold=True)

def draw_text(text, font, color, surface, center):
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))

def random_food_position(snake):
    empty = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in snake
    ]
    return random.choice(empty) if empty else None

def reset_game():
    center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
    return {
        "snake": snake,
        "direction": (1, 0),
        "next_direction": (1, 0),
        "food": random_food_position(snake),
        "score": 0,
        "state": "ready",
        "best": 0,
    }

def draw_rounded_rect(surface, color, rect, radius=10, border_color=None, border_width=1):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border_color:
        pygame.draw.rect(surface, border_color, rect, width=border_width, border_radius=radius)

def draw_board():
    board_rect = pygame.Rect(0, PANEL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - PANEL_HEIGHT)
    pygame.draw.rect(screen, BOARD_BG, board_rect)
    for x in range(0, WINDOW_WIDTH + 1, CELL_SIZE):
        pygame.draw.line(screen, GRID, (x, PANEL_HEIGHT), (x, WINDOW_HEIGHT), 1)
    for y in range(PANEL_HEIGHT, WINDOW_HEIGHT + 1, CELL_SIZE):
        pygame.draw.line(screen, GRID, (0, y), (WINDOW_WIDTH, y), 1)
    pygame.draw.line(screen, PANEL_BORDER, (0, PANEL_HEIGHT), (WINDOW_WIDTH, PANEL_HEIGHT), 2)

def draw_snake(snake, direction):
    for index, (gx, gy) in enumerate(snake):
        x = gx * CELL_SIZE
        y = PANEL_HEIGHT + gy * CELL_SIZE
        rect = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        if index == 0:
            color = GREEN
            pygame.draw.rect(screen, color, rect, border_radius=7)
            # Eyes face the direction of travel.
            dx, dy = direction
            eye_positions = {
                (1, 0): [(x + 13, y + 6), (x + 13, y + 14)],
                (-1, 0): [(x + 7, y + 6), (x + 7, y + 14)],
                (0, -1): [(x + 6, y + 7), (x + 14, y + 7)],
                (0, 1): [(x + 6, y + 13), (x + 14, y + 13)],
            }
            for eye in eye_positions[(dx, dy)]:
                pygame.draw.circle(screen, BG, eye, 2)
        else:
            # Subtle shading toward the tail.
            shade = max(0, index - 1)
            factor = max(0.45, 1 - shade * 0.025)
            segment_color = tuple(int(c * factor) for c in GREEN_DARK)
            pygame.draw.rect(screen, segment_color, rect, border_radius=6)

def draw_food(food, elapsed):
    if food is None:
        return
    gx, gy = food
    cx = gx * CELL_SIZE + CELL_SIZE // 2
    cy = PANEL_HEIGHT + gy * CELL_SIZE + CELL_SIZE // 2
    pulse = int(2 * (1 + (elapsed % 700) / 700))
    pygame.draw.circle(screen, (85, 35, 57), (cx, cy), 9 + pulse)
    pygame.draw.circle(screen, RED, (cx, cy), 7)
    pygame.draw.circle(screen, (255, 205, 210), (cx - 2, cy - 2), 2)

def draw_hud(score, best, paused=False):
    pygame.draw.rect(screen, PANEL, (0, 0, WINDOW_WIDTH, PANEL_HEIGHT))
    pygame.draw.line(screen, PANEL_BORDER, (0, PANEL_HEIGHT - 1), (WINDOW_WIDTH, PANEL_HEIGHT - 1), 2)
    draw_text("SNAKE RUSH", FONT_TITLE, WHITE, screen, (105, 27))
    draw_text("ARCADE EDITION", FONT_SMALL, MUTED, screen, (105, 55))

    # Score cards
    card_w, card_h = 120, 54
    score_rect = pygame.Rect(WINDOW_WIDTH - 270, 18, card_w, card_h)
    best_rect = pygame.Rect(WINDOW_WIDTH - 135, 18, card_w, card_h)
    draw_rounded_rect(screen, (26, 37, 62), score_rect, 10, PANEL_BORDER)
    draw_rounded_rect(screen, (26, 37, 62), best_rect, 10, PANEL_BORDER)
    draw_text("SCORE", FONT_SMALL, MUTED, screen, (score_rect.centerx, score_rect.y + 14))
    draw_text(str(score), FONT_MED, GREEN, screen, (score_rect.centerx, score_rect.y + 37))
    draw_text("BEST", FONT_SMALL, MUTED, screen, (best_rect.centerx, best_rect.y + 14))
    draw_text(str(best), FONT_MED, GOLD, screen, (best_rect.centerx, best_rect.y + 37))

    status = "PAUSED" if paused else "WASD / ARROWS  •  SPACE PAUSE  •  R RESTART"
    draw_text(status, FONT_SMALL, BLUE if paused else MUTED, screen, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 14))

def draw_overlay(title, subtitle, hint):
    shade = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - PANEL_HEIGHT), pygame.SRCALPHA)
    shade.fill((5, 9, 20, 185))
    screen.blit(shade, (0, PANEL_HEIGHT))
    card = pygame.Rect(90, PANEL_HEIGHT + 130, WINDOW_WIDTH - 180, 210)
    draw_rounded_rect(screen, (18, 27, 49), card, 18, (56, 77, 112), 2)
    draw_text(title, FONT_BIG, WHITE, screen, (WINDOW_WIDTH // 2, card.y + 55))
    draw_text(subtitle, FONT_MED, GREEN, screen, (WINDOW_WIDTH // 2, card.y + 105))
    draw_text(hint, FONT_SMALL, MUTED, screen, (WINDOW_WIDTH // 2, card.y + 155))

def main():
    game = reset_game()
    best_score = 0
    running = True
    elapsed = 0
    accumulator = 0
    # Start slowly; movement gets faster as the snake grows.
    base_speed = 4  # moves per second at the start
    max_speed = 15   # speed cap so it stays playable
    move_interval = 1000 / base_speed

    while running:
        dt = clock.tick(60)
        elapsed += dt
        accumulator += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    running = False
                elif event.key == pygame.K_r:
                    game = reset_game()
                    game["best"] = best_score
                    accumulator = 0
                elif event.key == pygame.K_SPACE:
                    if game["state"] == "playing":
                        game["state"] = "paused"
                    elif game["state"] == "paused":
                        game["state"] = "playing"
                        # Discard time accumulated while paused so the snake
                        # doesn't try to catch up with several moves at once.
                        accumulator = 0
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if game["state"] in ("ready", "over", "won"):
                        game = reset_game()
                        game["best"] = best_score
                        game["state"] = "playing"
                        accumulator = 0

                if game["state"] in ("ready", "playing"):
                    dx, dy = game["direction"]
                    key_dirs = {
                        pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
                        pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
                        pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
                        pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
                    }
                    requested = key_dirs.get(event.key)
                    if requested:
                        # Compare against the already committed direction so rapid key presses
                        # cannot sneak in a 180-degree reversal.
                        if requested != (-dx, -dy):
                            game["next_direction"] = requested
                        if game["state"] == "ready":
                            game["state"] = "playing"

        if game["state"] == "playing":
            while accumulator >= move_interval:
                accumulator -= move_interval
                game["direction"] = game["next_direction"]
                dx, dy = game["direction"]
                head_x, head_y = game["snake"][0]
                new_head = (head_x + dx, head_y + dy)

                # Wall collision
                if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                    game["state"] = "over"
                    break

                # Eating food
                ate = new_head == game["food"]
                body_to_check = game["snake"] if ate else game["snake"][:-1]
                if new_head in body_to_check:
                    game["state"] = "over"
                    break

                game["snake"].insert(0, new_head)
                if ate:
                    game["score"] += 1
                    best_score = max(best_score, game["score"])
                    game["food"] = random_food_position(game["snake"])
                    if game["food"] is None:
                        game["state"] = "won"
                        break
                    # Gradually ramp difficulty, with a gentle cap.
                    move_interval = max(65, 1000 / min(FPS + game["score"] // 4, 15))
                else:
                    game["snake"].pop()

        draw_board()
        draw_food(game["food"], elapsed)
        draw_snake(game["snake"], game["direction"])
        draw_hud(game["score"], best_score, paused=game["state"] == "paused")

        if game["state"] == "ready":
            draw_overlay("SNAKE RUSH", "Ready to slither?", "Press ENTER or any direction to start")
        elif game["state"] == "paused":
            draw_overlay("PAUSED", "Take a breather", "Press SPACE to continue  •  R to restart")
        elif game["state"] == "over":
            draw_overlay("GAME OVER", f"Final score: {game['score']}", "Press ENTER to play again  •  R to restart")
        elif game["state"] == "won":
            draw_overlay("YOU WIN!", f"Final score: {game['score']}", "Press ENTER to play again")

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
