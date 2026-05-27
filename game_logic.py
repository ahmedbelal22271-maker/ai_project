from constants import GRID_SIZE

class GameState:
    def __init__(self):
        self.p1_pos, self.p2_pos = (4, 8), (4, 0)
        self.p1_walls, self.p2_walls, self.turn = 10, 10, 1
        self.h_walls = [[False for _ in range(GRID_SIZE-1)] for _ in range(GRID_SIZE)]
        self.v_walls = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE-1)]
        self.winner = None

class GameEngine:
    def __init__(self):
        self.state = GameState()

    def get_adjacent(self, col, row, state=None):
        if state is None: state = self.state
        adj = []
        if row > 0 and not state.h_walls[col][row-1]: adj.append((col, row-1))
        if row < GRID_SIZE-1 and not state.h_walls[col][row]: adj.append((col, row+1))
        if col > 0 and not state.v_walls[col-1][row]: adj.append((col-1, row))
        if col < GRID_SIZE-1 and not state.v_walls[col][row]: adj.append((col+1, row))
        return adj

    def get_valid_pawn_moves(self, player, state=None):
        if state is None: state = self.state
        pos = state.p1_pos if player == 1 else state.p2_pos
        opp_pos = state.p2_pos if player == 1 else state.p1_pos
        valid = []
        for cell in self.get_adjacent(pos[0], pos[1], state):
            if cell != opp_pos: 
                valid.append(cell)
            else:
                opp_adj = self.get_adjacent(opp_pos[0], opp_pos[1], state)
                jump_behind = (opp_pos[0] + (opp_pos[0]-pos[0]), opp_pos[1] + (opp_pos[1]-pos[1]))
                if jump_behind in opp_adj and jump_behind != pos: 
                    valid.append(jump_behind)
                else: 
                    valid.extend([c for c in opp_adj if c not in (pos, jump_behind)])
        return valid