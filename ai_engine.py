import random
import copy
from constants import GRID_SIZE

class AIPlayer:
    """Manages AI decision-making for a Quoridor-style game across 3 difficulties."""
    def __init__(self, difficulty, engine):
        self.difficulty = difficulty
        self.engine = engine

    def get_move(self):
        if self.difficulty == 1:
            return self._ai_easy()
        elif self.difficulty == 2:
            return self._ai_medium()
        elif self.difficulty == 3:
            return self._ai_hard()
        return None

    def _ai_easy(self):
        # 20% chance to attempt a random wall placement
        if self.engine.state.p2_walls > 0 and random.random() < 0.20:
            attempts = 0
            while attempts < 20:
                c, r = random.randint(0, GRID_SIZE-2), random.randint(0, GRID_SIZE-2)
                orient = random.choice(['H', 'V'])
                if self.engine.is_valid_wall(c, r, orient): 
                    return ('WALL', (c, r, orient))
                attempts += 1
                
        valid_moves = self.engine.get_valid_pawn_moves(2)
        p2_path = self.engine.bfs_shortest_path(self.engine.state.p2_pos, GRID_SIZE-1, self.engine.state)
        # 70% chance to follow the optimal BFS shortest path
        if p2_path is not None and len(p2_path) > 0 and random.random() < 0.70:
            if p2_path[0] in valid_moves: 
                return ('MOVE', p2_path[0])
        return ('MOVE', random.choice(valid_moves))
    
    def _ai_medium(self):
        """Reactive: Intercepts opponent's next 3 steps if they are winning; otherwise advances."""
        p1_path = self.engine.bfs_shortest_path(self.engine.state.p1_pos, 0, self.engine.state)
        p2_path = self.engine.bfs_shortest_path(self.engine.state.p2_pos, GRID_SIZE-1, self.engine.state)
        # If opponent is winning or tied, try to block their immediate next 3 steps
        if self.engine.state.p2_walls > 0 and p1_path is not None and p2_path is not None:
            if len(p1_path) <= len(p2_path):
                for c, r in p1_path[:3]:
                    for tw_c, tw_r, orient in [(c, r, 'H'), (c-1, r, 'H'), (c, r, 'V'), (c, r-1, 'V')]:
                        if self.engine.is_valid_wall(tw_c, tw_r, orient):
                            return ('WALL', (tw_c, tw_r, orient))
        # Otherwise, advance along own shortest path
        valid_moves = self.engine.get_valid_pawn_moves(2)
        if p2_path is not None and len(p2_path) > 0 and p2_path[0] in valid_moves: return ('MOVE', p2_path[0])
        return ('MOVE', valid_moves[0])
    
    def _ai_hard(self):
        """Minimax-lite: Simulates 1-step moves/walls, maximizing (P1_path - P2_path)."""
        best_move = None
        max_eval = -999
        valid_moves = self.engine.get_valid_pawn_moves(2)
        # 1. Evaluate all valid pawn moves (maximize P1 path length - P2 path length)
        for move in valid_moves:
            test_state = copy.deepcopy(self.engine.state)
            test_state.p2_pos = move
            p1_path = self.engine.bfs_shortest_path(test_state.p1_pos, 0, test_state)
            p2_path = self.engine.bfs_shortest_path(test_state.p2_pos, GRID_SIZE-1, test_state)
            
            if p1_path is not None and p2_path is not None:
                eval_score = len(p1_path) - len(p2_path)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = ('MOVE', move)
        # 2. Evaluate placing walls around the opponent's next 4 steps
        if self.engine.state.p2_walls > 0:
            current_p1_path = self.engine.bfs_shortest_path(self.engine.state.p1_pos, 0, self.engine.state)
            if current_p1_path is not None:
                for c, r in current_p1_path[:4]:
                    for orient in ['H', 'V']:
                        for dx, dy in [(0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)]:
                            if self.engine.is_valid_wall(c + dx, r + dy, orient):
                                test_state = copy.deepcopy(self.engine.state)
                                if orient == 'H': test_state.h_walls[c+dx][r+dy] = test_state.h_walls[c+dx+1][r+dy] = True
                                else: test_state.v_walls[c+dx][r+dy] = test_state.v_walls[c+dx][r+dy+1] = True
                                p1_new_path = self.engine.bfs_shortest_path(test_state.p1_pos, 0, test_state)
                                p2_new_path = self.engine.bfs_shortest_path(test_state.p2_pos, GRID_SIZE-1, test_state)
                                if p1_new_path is not None and p2_new_path is not None:
                                    # -0.1 penalty breaks ties by prioritizing moving over walling
                                    eval_score = (len(p1_new_path) - len(p2_new_path)) - 0.1
                                    if eval_score > max_eval:
                                        max_eval = eval_score
                                        best_move = ('WALL', (c+dx, r+dy, orient))           

        return best_move if best_move else ('MOVE', random.choice(valid_moves))
    