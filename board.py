import pygame
import logic

CELL_SIZE = 30

BG_COLOR = (192, 192, 192)
GRID_COLOR = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

NUM_COLORS = {
    1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0),
    4: (0, 0, 128), 5: (128, 0, 0)
}

def draw_field(screen, font):
    screen.fill(BG_COLOR)

    for r in range(logic.ROWS):
        for c in range(logic.COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

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

def draw_end_menu(screen, font, btn_restart, btn_exit, width, height):

    popup_rect = pygame.Rect(width // 2 - 130, height // 2 - 60, 260, 130)
    pygame.draw.rect(screen, (192, 192, 192), popup_rect)  # gray fon
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 3)  #black ramka

    msg_text = "WIN!" if logic.win else "GAME OVER!"
    text_color = (0, 128, 0) if logic.win else (255, 0, 0)
    msg_surf = font.render(msg_text, True, text_color)
    screen.blit(msg_surf, (width // 2 - msg_surf.get_width() // 2, height // 2 - 40))

    # Кнопка Retry
    pygame.draw.rect(screen, (100, 100, 100), btn_restart)
    screen.blit(font.render("Retry", True, (255, 255, 255)), (btn_restart.x + 28, btn_restart.y + 10))

    # Кнопка Exit
    pygame.draw.rect(screen, (100, 100, 100), btn_exit)
    screen.blit(font.render("Exit", True, (255, 255, 255)), (btn_exit.x + 35, btn_exit.y + 10))