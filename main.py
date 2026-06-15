import pygame
import sys
import logic

CELL_SIZE = 30
WIDTH, HEIGHT = logic.COLS * CELL_SIZE, logic.ROWS * CELL_SIZE

# colors
BG_COLOR = (192, 192, 192)
GRID_COLOR = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

NUM_COLORS = {
    1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0),
    4: (0, 0, 128), 5: (128, 0, 0)
}

# Pygame window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper Raw Split")
font = pygame.font.SysFont('Arial', 16, bold=True)

clock = pygame.time.Clock()

# game core
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and not logic.game_over:
            # Convert click position to grid coordinates
            c, r = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
            if not (0 <= r < logic.ROWS and 0 <= c < logic.COLS): continue

            if event.button == 1:  # Left Click
                if logic.first_click:
                    logic.generate_mines(r, c)
                    logic.first_click = False
                logic.reveal_cell(r, c)

            elif event.button == 3:  # Right Click
                if logic.visible[r][c] == 0:
                    logic.visible[r][c] = 2
                elif logic.visible[r][c] == 2:
                    logic.visible[r][c] = 0

    # Draw phase
    screen.fill(BG_COLOR)
    for r in range(logic.ROWS):
        for c in range(logic.COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)  # Draw cell border

            state = logic.visible[r][c]
            if state == 0:
                pygame.draw.rect(screen, WHITE, (rect.x + 1, rect.y + 1, CELL_SIZE - 2, CELL_SIZE - 2), 1)
            elif state == 2:
                txt = font.render("F", True, RED)
                screen.blit(txt, (rect.x + 9, rect.y + 6))
            elif state == 1:
                pygame.draw.rect(screen, GRID_COLOR, rect)
                val = logic.board[r][c]
                if val == -1:
                    pygame.draw.rect(screen, RED, rect)
                    txt = font.render("X", True, BLACK)
                    screen.blit(txt, (rect.x + 9, rect.y + 6))
                elif val > 0:
                    txt = font.render(str(val), True, NUM_COLORS.get(val, BLACK))
                    screen.blit(txt, (rect.x + 9, rect.y + 6))

    pygame.display.flip()
    clock.tick(30)