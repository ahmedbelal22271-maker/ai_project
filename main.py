import pygame, sys
from constants import *
from game_logic import GameEngine
from ui_renderer import Renderer

class QuoridorApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Quoridor - MVC Architecture")
        
        font_prefs = "segoeui, helveticaneue, arial"
        self.font = pygame.font.SysFont(font_prefs, 18, bold=True)
        self.title_font = pygame.font.SysFont(font_prefs, 24, bold=True)
        
        self.engine = GameEngine()
        self.renderer = Renderer(self.screen, self.font, self.title_font)
        
        self.ai_mode = 0 
        self.hover_wall = None
        self.msg = "Game Started. Player 1's turn."
        
        btn_y = 25
        self.ui_rects = {
            'reset': pygame.Rect(30, btn_y, 80, 40),
            'ai': pygame.Rect(120, btn_y, 110, 40),
            'undo': pygame.Rect(240, btn_y, 70, 40),
            'redo': pygame.Rect(320, btn_y, 70, 40),
            'quit': pygame.Rect(550, btn_y, 80, 40)
        }

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL): 
                        if self.engine.undo(): self.msg = "Undo successful."
                    elif event.key == pygame.K_y and (pygame.key.get_mods() & pygame.KMOD_CTRL): 
                        if self.engine.redo(): self.msg = "Redo successful."
            
            self.renderer.render_game(self.engine, self.ai_mode, self.msg, self.hover_wall, self.ui_rects)
            clock.tick(60)

if __name__ == "__main__":
    QuoridorApp().run()