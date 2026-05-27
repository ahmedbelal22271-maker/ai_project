import pygame
from constants import *

class Renderer:
    def __init__(self, screen, font, title_font):
        self.screen, self.font, self.title_font = screen, font, title_font

    def draw_text_centered(self, text, rect, color=TEXT_COLOR, font=None):
        surf = (font or self.font).render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    def render_game(self, engine, ai_mode, msg):
        self.screen.fill(BG_COLOR)
        pad = 12
        pygame.draw.rect(self.screen, BOARD_BG_COLOR, pygame.Rect(MARGIN-pad, TOP_MARGIN-pad, (GRID_SIZE*CELL_SIZE)+(pad*2), (GRID_SIZE*CELL_SIZE)+(pad*2)), border_radius=10)
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x, y = MARGIN + c*CELL_SIZE, TOP_MARGIN + r*CELL_SIZE
                pygame.draw.rect(self.screen, CELL_COLOR, pygame.Rect(x+2, y+2, CELL_SIZE-4, CELL_SIZE-4), border_radius=5)
                
        pygame.display.flip()