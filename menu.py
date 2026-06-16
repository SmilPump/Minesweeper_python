import pygame

# Colors
BG_COLOR = (192, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (100, 100, 100)
GREEN = (76, 175, 80)


class DifficultyMenu:
    def __init__(self, screen_width=400, screen_height=400):
        self.width = screen_width
        self.height = screen_height

        # Default choices
        self.selected_mode = "small"

        # Rectangles for buttons
        self.btn_small = pygame.Rect(self.width // 2 - 100, 120, 200, 40)
        self.btn_medium = pygame.Rect(self.width // 2 - 100, 180, 200, 40)
        self.btn_big = pygame.Rect(self.width // 2 - 100, 240, 200, 40)
        self.btn_start = pygame.Rect(self.width // 2 - 80, 310, 160, 45)

    def draw(self, screen, font):
        screen.fill(BG_COLOR)

        # Helper function to draw option buttons
        for mode, rect, text in [("small", self.btn_small, "Small (9x9, 10 min)"),
                                 ("medium", self.btn_medium, "Medium (16x16, 40 min)"),
                                 ("big", self.btn_big, "Big (20x20, 80 min)")]:
            # Highlight button
            color = DARK_GRAY if self.selected_mode == mode else BG_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            txt_color = WHITE if self.selected_mode == mode else BLACK
            txt_surf = font.render(text, True, txt_color)
            screen.blit(txt_surf, (rect.x + (rect.width - txt_surf.get_width()) // 2, rect.y + 10))

        # Start Button
        pygame.draw.rect(screen, GREEN, self.btn_start)
        pygame.draw.rect(screen, BLACK, self.btn_start, 3)
        start_txt = font.render("START GAME", True, WHITE)
        screen.blit(start_txt, (self.btn_start.x + 25, self.btn_start.y + 12))

    def handle_click(self, pos):
        if self.btn_small.collidepoint(pos):
            self.selected_mode = "small"
        elif self.btn_medium.collidepoint(pos):
            self.selected_mode = "medium"
        elif self.btn_big.collidepoint(pos):
            self.selected_mode = "big"
        elif self.btn_start.collidepoint(pos):
            # ВОТ ТУТ мы отдаем результат только по клику на START
            if self.selected_mode == "small":
                return {"rows": 9, "cols": 9, "mines": 10}
            elif self.selected_mode == "medium":
                return {"rows": 16, "cols": 16, "mines": 40}
            elif self.selected_mode == "big":
                return {"rows": 20, "cols": 20, "mines": 80}
        return None