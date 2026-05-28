import pygame, sys
from constants import *
from game_logic import GameEngine
from ai_engine import AIPlayer
from ui_renderer import Renderer

class QuoridorApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Quoridor - MVC Architecture")
        
        # fallback fonts in case segoeui isn't installed on the machine
        font_prefs = "segoeui, helveticaneue, arial"
        self.font = pygame.font.SysFont(font_prefs, 18, bold=True)
        self.title_font = pygame.font.SysFont(font_prefs, 24, bold=True)
        
        # pull in the other modules
        self.engine = GameEngine()
        self.renderer = Renderer(self.screen, self.font, self.title_font)
        
        # 0=PvP, 1=Easy, 2=Med, 3=Hard
        self.ai_mode = 0 
        self.hover_wall = None
        self.msg = "Game Started. Player 1's turn."
        
        # UI hitboxes for the top menu
        btn_y = 25
        self.ui_rects = {
            'reset': pygame.Rect(30, btn_y, 80, 40),
            'ai': pygame.Rect(120, btn_y, 110, 40),
            'undo': pygame.Rect(240, btn_y, 70, 40),
            'redo': pygame.Rect(320, btn_y, 70, 40),
            'quit': pygame.Rect(550, btn_y, 80, 40)
        }

    def process_click(self, pos):
        mx, my = pos
        
        # check menu buttons first
        if self.ui_rects['quit'].collidepoint(mx, my): 
            pygame.quit(); sys.exit()
        if self.ui_rects['reset'].collidepoint(mx, my): 
            self.engine.reset(); self.msg = "Game reset. Player 1's turn."; return
        if self.ui_rects['ai'].collidepoint(mx, my): 
            self.ai_mode = (self.ai_mode + 1) % 4
            self.engine.reset(); self.msg = "Mode Changed. Player 1's turn."; return
        if self.ui_rects['undo'].collidepoint(mx, my): 
            if self.engine.undo(): self.msg = "Undo successful."
            return
        if self.ui_rects['redo'].collidepoint(mx, my): 
            if self.engine.redo(): self.msg = "Redo successful."
            return

        # block clicks if game is over or AI is currently playing
        if self.engine.state.winner or (self.ai_mode > 0 and self.engine.state.turn == 2): 
            return

        self.hover_wall = None
        in_x, in_y = mx - MARGIN, my - TOP_MARGIN
        
        # make sure click is actually inside the board area
        if 0 <= in_x <= GRID_SIZE * CELL_SIZE and 0 <= in_y <= GRID_SIZE * CELL_SIZE:
            c, r = in_x // CELL_SIZE, in_y // CELL_SIZE
            rem_x, rem_y = in_x % CELL_SIZE, in_y % CELL_SIZE

            walls_avail = self.engine.state.p1_walls if self.engine.state.turn == 1 else self.engine.state.p2_walls
            
            # handle wall placements
            if walls_avail > 0:
                threshold = WALL_THICKNESS * 2
                
                # check horizontal wall slots (bottom edge of cell)
                if rem_y > CELL_SIZE - threshold and r < GRID_SIZE - 1 and c < GRID_SIZE - 1:
                    valid = self.engine.is_valid_wall(c, r, 'H')
                    self.hover_wall = (c, r, 'H', valid)
                    if valid:
                        self.engine.state.h_walls[c][r] = self.engine.state.h_walls[c+1][r] = True
                        self.end_turn(placed_wall=True)
                        return
                        
                # check vertical wall slots (right edge of cell)
                elif rem_x > CELL_SIZE - threshold and c < GRID_SIZE - 1 and r < GRID_SIZE - 1:
                    valid = self.engine.is_valid_wall(c, r, 'V')
                    self.hover_wall = (c, r, 'V', valid)
                    if valid:
                        self.engine.state.v_walls[c][r] = self.engine.state.v_walls[c][r+1] = True
                        self.end_turn(placed_wall=True)
                        return

            # handle pawn movement (if we didn't click a wall slot)
            if not self.hover_wall:
                if (c, r) in self.engine.get_valid_pawn_moves(self.engine.state.turn):
                    if self.engine.state.turn == 1: 
                        self.engine.state.p1_pos = (c, r)
                    else: 
                        self.engine.state.p2_pos = (c, r)
                    self.end_turn(placed_wall=False)
                else:
                    self.msg = "Invalid Move!"

    def process_hover(self, pos):
        # ignore hover if it's not the player's turn or game ended
        if self.engine.state.winner or (self.ai_mode > 0 and self.engine.state.turn == 2): 
            return
            
        mx, my = pos
        self.hover_wall = None
        in_x, in_y = mx - MARGIN, my - TOP_MARGIN
        
        # only preview walls if mouse is inside the grid bounds
        if 0 <= in_x <= GRID_SIZE * CELL_SIZE and 0 <= in_y <= GRID_SIZE * CELL_SIZE:
            c, r = in_x // CELL_SIZE, in_y // CELL_SIZE
            rem_x, rem_y = in_x % CELL_SIZE, in_y % CELL_SIZE
            
            walls = self.engine.state.p1_walls if self.engine.state.turn == 1 else self.engine.state.p2_walls
            if walls > 0:
                thresh = WALL_THICKNESS * 2
                if rem_y > CELL_SIZE - thresh and r < GRID_SIZE - 1 and c < GRID_SIZE - 1:
                    self.hover_wall = (c, r, 'H', self.engine.is_valid_wall(c, r, 'H'))
                elif rem_x > CELL_SIZE - thresh and c < GRID_SIZE - 1 and r < GRID_SIZE - 1:
                    self.hover_wall = (c, r, 'V', self.engine.is_valid_wall(c, r, 'V'))

    def end_turn(self, placed_wall):
        # deduct wall count if they just placed one
        if self.engine.state.turn == 1: 
            self.engine.state.p1_walls -= (1 if placed_wall else 0)
        else: 
            self.engine.state.p2_walls -= (1 if placed_wall else 0)
        
        if self.engine.check_win(): 
            self.msg = f"PLAYER {self.engine.state.winner} WINS!"
        else:
            # swap turns
            self.engine.state.turn = 2 if self.engine.state.turn == 1 else 1
            self.msg = f"Player {self.engine.state.turn}'s turn."
            
        # clear redo stack whenever a new move is made so we don't break history
        self.engine.redo_stack.clear()
        self.engine.save_state()

        # trigger the AI if it's player 2's turn in a PvE mode
        if self.ai_mode > 0 and self.engine.state.turn == 2 and not self.engine.state.winner:
            self.trigger_ai()

    def trigger_ai(self):
        # force a frame draw so the UI updates to "AI is thinking..." before it hangs
        self.msg = "AI is thinking..."
        self.renderer.render_game(self.engine, self.ai_mode, self.msg, self.hover_wall, self.ui_rects)
        
        ai = AIPlayer(self.ai_mode, self.engine)
        move_type, data = ai.get_move()
        
        if move_type == 'MOVE':
            self.engine.state.p2_pos = data
            self.msg = "AI moved pawn."
            self.end_turn(placed_wall=False)
        elif move_type == 'WALL':
            c, r, orient = data
            if orient == 'H': 
                self.engine.state.h_walls[c][r] = self.engine.state.h_walls[c+1][r] = True
            else: 
                self.engine.state.v_walls[c][r] = self.engine.state.v_walls[c][r+1] = True
            self.msg = "AI placed a wall."
            self.end_turn(placed_wall=True)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEMOTION: 
                    self.process_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    self.process_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    # ctrl+z and ctrl+y shortcuts
                    if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL): 
                        if self.engine.undo(): self.msg = "Undo successful."
                    elif event.key == pygame.K_y and (pygame.key.get_mods() & pygame.KMOD_CTRL): 
                        if self.engine.redo(): self.msg = "Redo successful."
            
            self.renderer.render_game(self.engine, self.ai_mode, self.msg, self.hover_wall, self.ui_rects)
            clock.tick(60) # cap framerate

if __name__ == "__main__":
    QuoridorApp().run()