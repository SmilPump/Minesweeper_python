import pygame
import sys
import random

# size
ROWS, COLS, MINES = 16, 16, 40
CELL_SIZE = 30
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Basic colors for rendering
BG_COLOR = (192, 192, 192)
GRID_COLOR = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

NUM_COLORS = {
    1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0),
    4: (0, 0, 128), 5: (128, 0, 0)
}

# Init Pygame engine
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper Raw")
font = pygame.font.SysFont('Arial', 16, bold=True)

# Arrays to hold game data
# board: 0 = empty, -1 = mine, 1+ = numbers
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
# visible: 0 = hidden, 1 = opened, 2 = flag
visible = [[0 for _ in range(COLS)] for _ in range(ROWS)]

mine_positions = set()
first_click = True
game_over = False


def generate_mines(first_r, first_c):
    # Blacklist the first clicked cell and its neighbors
    forbidden = {(first_r + dr, first_c + dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1]}

    while len(mine_positions) < MINES:
        r, c = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if (r, c) not in forbidden:
            mine_positions.add((r, c))
            board[r][c] = -1

    # Calculate neighbor numbers
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == -1: continue
            count = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS and board[r + dr][c + dc] == -1)
            board[r][c] = count


def reveal_cell(r, c):
    if visible[r][c] == 1 or visible[r][c] == 2: return
    visible[r][c] = 1

    # If hit a mine
    if board[r][c] == -1:
        global game_over
        game_over = True
        for mr, mc in mine_positions: visible[mr][mc] = 1  # Show all bombs
        return

    # Auto-open empty neighbors using basic recursion
    if board[r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    reveal_cell(nr, nc)


# Core game
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            c, r = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
            if not (0 <= r < ROWS and 0 <= c < COLS): continue

            if event.button == 1:  # Left Click
                if first_click:
                    generate_mines(r, c)
                    first_click = False
                reveal_cell(r, c)
            elif event.button == 3:  # Right Click
                if visible[r][c] == 0:
                    visible[r][c] = 2
                elif visible[r][c] == 2:
                    visible[r][c] = 0

    # Draw everything from scratch
    screen.fill(BG_COLOR)
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)  # Draw grid line

            state = visible[r][c]
            if state == 0:  # Hidden tile
                pygame.draw.rect(screen, WHITE, (rect.x + 1, rect.y + 1, CELL_SIZE - 2, CELL_SIZE - 2), 1)
            elif state == 2:  # Flag
                txt = font.render("F", True, RED)
                screen.blit(txt, (rect.x + 9, rect.y + 6))
            elif state == 1:  # Revealed tile
                pygame.draw.rect(screen, GRID_COLOR, rect)
                val = board[r][c]
                if val == -1:  # Mine exploded
                    pygame.draw.rect(screen, RED, rect)
                    txt = font.render("X", True, BLACK)
                    screen.blit(txt, (rect.x + 9, rect.y + 6))
                elif val > 0:  # Number inside tile
                    txt = font.render(str(val), True, NUM_COLORS.get(val, BLACK))
                    screen.blit(txt, (rect.x + 9, rect.y + 6))

    pygame.display.flip()
    clock.tick(30)