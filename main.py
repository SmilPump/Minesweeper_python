import pygame
import sys
import logic
import board

CELL_SIZE = 30
WIDTH, HEIGHT = logic.COLS * CELL_SIZE, logic.ROWS * CELL_SIZE

# Pygame window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper Raw Split")
font = pygame.font.SysFont('Arial', 16, bold=True)

#End Button
btn_restart = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 10, 100, 40)
btn_exit = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 10, 100, 40)

clock = pygame.time.Clock()

# game core
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #if game end
            if logic.game_over:
                if btn_restart.collidepoint(event.pos):
                    # clean all for new game
                    logic.board = [[0 for _ in range(logic.COLS)] for _ in range(logic.ROWS)]
                    logic.visible = [[0 for _ in range(logic.COLS)] for _ in range(logic.ROWS)]
                    logic.mine_positions = set()
                    logic.first_click = True
                    logic.game_over = False
                    logic.win = False
                elif btn_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                continue

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

    board.draw_field(screen, font)

    # game end menu
    if logic.game_over:
        board.draw_end_menu(screen, font, btn_restart, btn_exit, WIDTH, HEIGHT)

    pygame.display.flip()
    clock.tick(30)

