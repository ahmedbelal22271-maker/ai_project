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
        valid_moves = self.engine.get_valid_pawn_moves(2)
        return ('MOVE', random.choice(valid_moves))