import copy
from collections import deque
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
        self.history = []
        self.redo_stack = []
        self.save_state()

    def save_state(self):
        self.history.append(copy.deepcopy(self.state))
        
    def undo(self):
        if len(self.history) > 1:
            self.redo_stack.append(self.history.pop())
            self.state = copy.deepcopy(self.history[-1])
            return True
        return False
            
    def redo(self):
        if self.redo_stack:
            s = self.redo_stack.pop()
            self.history.append(s)
            self.state = copy.deepcopy(s)
            return True
        return False

    def reset(self):
        self.__init__()

    def check_win(self):
        if self.state.p1_pos[1] == 0: self.state.winner = 1
        elif self.state.p2_pos[1] == GRID_SIZE - 1: self.state.winner = 2
        return self.state.winner

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

    def is_valid_wall(self, col, row, orient, state=None):
        if state is None: state = self.state
        if col < 0 or col >= GRID_SIZE-1 or row < 0 or row >= GRID_SIZE-1: return False
        
        if orient == 'H':
            if state.h_walls[col][row] or state.h_walls[col+1][row]: return False
            if state.v_walls[col][row]: return False
        else:
            if state.v_walls[col][row] or state.v_walls[col][row+1]: return False
            if state.h_walls[col][row]: return False

        test_state = copy.deepcopy(state)
        if orient == 'H':
            test_state.h_walls[col][row] = test_state.h_walls[col+1][row] = True
        else:
            test_state.v_walls[col][row] = test_state.v_walls[col][row+1] = True
            
        p1_path = self.bfs_shortest_path(test_state.p1_pos, 0, test_state)
        p2_path = self.bfs_shortest_path(test_state.p2_pos, GRID_SIZE-1, test_state)
        return p1_path is not None and p2_path is not None

    def bfs_shortest_path(self, start, target_row, state):
        queue = deque([(start, [])])
        visited = {start}
        while queue:
            (c, r), path = queue.popleft()
            if r == target_row: return path
            for adj in self.get_adjacent(c, r, state):
                if adj not in visited:
                    visited.add(adj)
                    queue.append((adj, path + [adj]))
        return None