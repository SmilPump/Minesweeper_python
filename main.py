import pygame
import sys
import logic
import board
from menu import DifficultyMenu

# Pygame window
pygame.init()
CELL_SIZE = 30
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Minesweeper Raw Split")
font = pygame.font.SysFont('Arial', 16, bold=True)

# Start menu
game_state = "MENU"
menu = DifficultyMenu(400, 400)

#End Button
btn_restart = None
btn_exit = None

clock = pygame.time.Clock()

# game core
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "MENU":
                settings = menu.handle_click(event.pos)
                if settings:
                    logic.init_game(settings["rows"], settings["cols"], settings["mines"])
                    screen = pygame.display.set_mode((logic.COLS * CELL_SIZE, logic.ROWS * CELL_SIZE))

                    W, H = logic.COLS * CELL_SIZE, logic.ROWS * CELL_SIZE
                    btn_restart = pygame.Rect(W // 2 - 110, H // 2 + 10, 100, 40)
                    btn_exit = pygame.Rect(W // 2 + 10, H // 2 + 10, 100, 40)
                    game_state = "GAME"

            elif game_state == "GAME" and logic.game_over:

                if btn_restart.collidepoint(event.pos):
                    logic.init_game(logic.ROWS, logic.COLS, logic.MINES)
                elif btn_exit.collidepoint(event.pos):
                    pygame.quit();
                    sys.exit()

            elif game_state == "GAME":
                # klick logic
                c, r = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if 0 <= r < logic.ROWS and 0 <= c < logic.COLS:
                    if event.button == 1:
                        if logic.first_click: logic.generate_mines(r, c); logic.first_click = False
                        logic.reveal_cell(r, c)
                    elif event.button == 3:
                        if logic.visible[r][c] == 0:
                            logic.visible[r][c] = 2
                        elif logic.visible[r][c] == 2:
                            logic.visible[r][c] = 0

    # draw menu)
    if game_state == "MENU":
        menu.draw(screen, font)
    else:
        board.draw_field(screen, font)
        if logic.game_over:
            #end game menu draw
            W, H = logic.COLS * CELL_SIZE, logic.ROWS * CELL_SIZE
            board.draw_end_menu(screen, font, btn_restart, btn_exit, W, H)

    pygame.display.flip()
    clock.tick(30)

