import pygame
from constants import *

class Renderer:
    def __init__(self, screen, font, title_font):
        self.screen, self.font, self.title_font = screen, font, title_font

    # draws text in the middle of any rect we pass in
    def draw_text_centered(self, text, rect, color=TEXT_COLOR, font=None):
        surf = (font or self.font).render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    # changes color when mouse is over the button
    def draw_button(self, text, rect, color_bg=UI_BG, color_hover=UI_HOVER):
        mx, my = pygame.mouse.get_pos()
        color = color_hover if rect.collidepoint(mx, my) else color_bg
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        self.draw_text_centered(text, rect)

    def draw_pawn(self, pos, color):
        # convert grid cell to actual pixel position
        px, py = MARGIN + pos[0]*CELL_SIZE + CELL_SIZE//2, TOP_MARGIN + pos[1]*CELL_SIZE + CELL_SIZE//2
        r = CELL_SIZE // 2.8
        pygame.draw.circle(self.screen, color, (px, py), r)
        pygame.draw.circle(self.screen, (255, 255, 255), (px, py), r, 2)
        pygame.draw.circle(self.screen, (max(0, color[0]-40), max(0, color[1]-40), max(0, color[2]-40)), (px, py), r - 4)  # darker inner circle for depth

    def render_game(self, engine, ai_mode, msg, hover_wall, ui_rects):
        self.screen.fill(BG_COLOR)
        
        # top buttons
        self.draw_button("Reset", ui_rects['reset'])
        self.draw_button(["Vs Human", "AI: Easy", "AI: Med", "AI: Hard"][ai_mode], ui_rects['ai'])
        self.draw_button("Undo", ui_rects['undo'])
        self.draw_button("Redo", ui_rects['redo'])
        self.draw_button("Quit", ui_rects['quit'], QUIT_BG, QUIT_HOVER)

        # gold when someone wins, otherwise shows whose turn it is
        msg_color = (255, 215, 0) if engine.state.winner else (P1_COLOR if engine.state.turn == 1 else P2_COLOR)
        self.draw_text_centered(msg, pygame.Rect(MARGIN, 90, WIDTH - 2*MARGIN, 30), color=msg_color, font=self.title_font)
        stats = f"P1 Walls: {engine.state.p1_walls}      |      P2 Walls: {engine.state.p2_walls}"
        self.draw_text_centered(stats, pygame.Rect(MARGIN, 130, WIDTH - 2*MARGIN, 25), color=MUTED_TEXT)

        pad = 12
        pygame.draw.rect(self.screen, BOARD_BG_COLOR, pygame.Rect(MARGIN-pad, TOP_MARGIN-pad, (GRID_SIZE*CELL_SIZE)+(pad*2), (GRID_SIZE*CELL_SIZE)+(pad*2)), border_radius=10)

        # only show valid moves when it's a human's turn
        valid_moves = []
        if not engine.state.winner and (ai_mode == 0 or engine.state.turn == 1): 
            valid_moves = engine.get_valid_pawn_moves(engine.state.turn)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x, y = MARGIN + c*CELL_SIZE, TOP_MARGIN + r*CELL_SIZE
                pygame.draw.rect(self.screen, CELL_COLOR, pygame.Rect(x+2, y+2, CELL_SIZE-4, CELL_SIZE-4), border_radius=5)
                
                # highlight where the pawn can move
                if (c, r) in valid_moves:
                    vs = pygame.Surface((CELL_SIZE-4, CELL_SIZE-4), pygame.SRCALPHA)
                    pygame.draw.rect(vs, VALID_MOVE_COLOR, vs.get_rect(), border_radius=5)
                    self.screen.blit(vs, (x+2, y+2))
                
                if c < GRID_SIZE - 1 and r < GRID_SIZE and engine.state.v_walls[c][r]: 
                    pygame.draw.rect(self.screen, WALL_COLOR, pygame.Rect(MARGIN+(c+1)*CELL_SIZE - WALL_THICKNESS//2, y, WALL_THICKNESS, CELL_SIZE), border_radius=4)
                if r < GRID_SIZE - 1 and c < GRID_SIZE and engine.state.h_walls[c][r]: 
                    pygame.draw.rect(self.screen, WALL_COLOR, pygame.Rect(x, TOP_MARGIN+(r+1)*CELL_SIZE - WALL_THICKNESS//2, CELL_SIZE, WALL_THICKNESS), border_radius=4)

        # show wall preview while hovering, red if it's a bad spot
        if hover_wall and not engine.state.winner:
            hc, hr, horient, hvalid = hover_wall
            w, h = (CELL_SIZE*2, WALL_THICKNESS) if horient == 'H' else (WALL_THICKNESS, CELL_SIZE*2)
            hs = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(hs, HOVER_WALL_COLOR if hvalid else INVALID_WALL_COLOR, hs.get_rect(), border_radius=4)
            self.screen.blit(hs, (MARGIN + hc*CELL_SIZE, TOP_MARGIN + (hr+1)*CELL_SIZE - WALL_THICKNESS//2) if horient == 'H' else (MARGIN + (hc+1)*CELL_SIZE - WALL_THICKNESS//2, TOP_MARGIN + hr*CELL_SIZE))

        # pawns go on top of everything else
        self.draw_pawn(engine.state.p1_pos, P1_COLOR)
        self.draw_pawn(engine.state.p2_pos, P2_COLOR)
        pygame.display.flip()