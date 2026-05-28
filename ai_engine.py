import random
from constants import GRID_SIZE

class AIPlayer:
    def __init__(self, difficulty, engine):
        self.difficulty = difficulty
        self.engine = engine

    def get_move(self):
        if self.difficulty == 1:
            return self._ai_easy()
            
        valid_moves = self.engine.get_valid_pawn_moves(2)
        if valid_moves:
            return ('MOVE', random.choice(valid_moves))
        return None

    def _ai_easy(self):
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
        
        if p2_path is not None and len(p2_path) > 0 and random.random() < 0.70:
            if p2_path[0] in valid_moves: 
                return ('MOVE', p2_path[0])
        return ('MOVE', random.choice(valid_moves))