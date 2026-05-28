import copy
from collections import deque
from constants import GRID_SIZE


# Represents the current state of the game
class GameState:
    def __init__(self):
        # Initial player positions
        # Player 1 starts at bottom middle
        # Player 2 starts at top middle
        self.p1_pos, self.p2_pos = (4, 8), (4, 0)

        # Each player starts with 10 walls
        self.p1_walls, self.p2_walls, self.turn = 10, 10, 1

        # Horizontal wall grid
        # Stores whether a horizontal wall exists between cells
        self.h_walls = [[False for _ in range(GRID_SIZE-1)] for _ in range(GRID_SIZE)]

        # Vertical wall grid
        # Stores whether a vertical wall exists between cells
        self.v_walls = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE-1)]

        # Stores winner number when game ends
        self.winner = None


# Handles game logic and gameplay operations
class GameEngine:
    def __init__(self):
        # Create a new game state
        self.state = GameState()

        # Stack for undo functionality
        self.history = []

        # Stack for redo functionality
        self.redo_stack = []

        # Save initial game state
        self.save_state()

    # Save a deep copy of current state into history
    def save_state(self):
        self.history.append(copy.deepcopy(self.state))
        
    # Undo the previous move
    def undo(self):
        # Ensure there is at least one previous state
        if len(self.history) > 1:

            # Move current state into redo stack
            self.redo_stack.append(self.history.pop())

            # Restore previous state
            self.state = copy.deepcopy(self.history[-1])

            return True

        return False
            
    # Redo an undone move
    def redo(self):
        # Check if redo stack contains states
        if self.redo_stack:

            # Get latest undone state
            s = self.redo_stack.pop()

            # Add it back to history
            self.history.append(s)

            # Restore the state
            self.state = copy.deepcopy(s)

            return True

        return False

    # Reset the game completely
    def reset(self):
        self.__init__()

    # Check if any player reached winning row
    def check_win(self):

        # Player 1 wins if reaches top row
        if self.state.p1_pos[1] == 0:
            self.state.winner = 1

        # Player 2 wins if reaches bottom row
        elif self.state.p2_pos[1] == GRID_SIZE - 1:
            self.state.winner = 2

        return self.state.winner

    # Returns all adjacent reachable cells
    # considering existing walls
    def get_adjacent(self, col, row, state=None):

        # Use current state if no custom state provided
        if state is None:
            state = self.state

        adj = []

        # Check upward movement
        if row > 0 and not state.h_walls[col][row-1]:
            adj.append((col, row-1))

        # Check downward movement
        if row < GRID_SIZE-1 and not state.h_walls[col][row]:
            adj.append((col, row+1))

        # Check left movement
        if col > 0 and not state.v_walls[col-1][row]:
            adj.append((col-1, row))

        # Check right movement
        if col < GRID_SIZE-1 and not state.v_walls[col][row]:
            adj.append((col+1, row))

        return adj

    # Returns all valid pawn moves for a player
    def get_valid_pawn_moves(self, player, state=None):

        # Use current state if none provided
        if state is None:
            state = self.state

        # Get current player position
        pos = state.p1_pos if player == 1 else state.p2_pos

        # Get opponent position
        opp_pos = state.p2_pos if player == 1 else state.p1_pos

        valid = []

        # Loop through adjacent cells
        for cell in self.get_adjacent(pos[0], pos[1], state):

            # Normal move if opponent is not occupying cell
            if cell != opp_pos: 
                valid.append(cell)

            else:
                # Get opponent possible adjacent cells
                opp_adj = self.get_adjacent(opp_pos[0], opp_pos[1], state)

                # Calculate jump position behind opponent
                jump_behind = (
                    opp_pos[0] + (opp_pos[0]-pos[0]),
                    opp_pos[1] + (opp_pos[1]-pos[1])
                )

                # If jump is possible, add jump move
                if jump_behind in opp_adj and jump_behind != pos: 
                    valid.append(jump_behind)

                else:
                    # Otherwise allow diagonal side moves
                    valid.extend([
                        c for c in opp_adj
                        if c not in (pos, jump_behind)
                    ])

        return valid

    # Validate whether a wall placement is legal
    def is_valid_wall(self, col, row, orient, state=None):

        # Use current state if none provided
        if state is None:
            state = self.state

        # Ensure wall is inside board boundaries
        if col < 0 or col >= GRID_SIZE-1 or row < 0 or row >= GRID_SIZE-1:
            return False
        
        # Horizontal wall validation
        if orient == 'H':

            # Cannot overlap another horizontal wall
            if state.h_walls[col][row] or state.h_walls[col+1][row]:
                return False

            # Cannot cross a vertical wall
            if state.v_walls[col][row]:
                return False

        else:
            # Vertical wall validation

            # Cannot overlap another vertical wall
            if state.v_walls[col][row] or state.v_walls[col][row+1]:
                return False

            # Cannot cross a horizontal wall
            if state.h_walls[col][row]:
                return False

        # Create temporary state for testing wall placement
        test_state = copy.deepcopy(state)

        # Place temporary wall
        if orient == 'H':
            test_state.h_walls[col][row] = True
            test_state.h_walls[col+1][row] = True
        else:
            test_state.v_walls[col][row] = True
            test_state.v_walls[col][row+1] = True
            
        # Ensure both players still have a path to goal
        p1_path = self.bfs_shortest_path(
            test_state.p1_pos,
            0,
            test_state
        )

        p2_path = self.bfs_shortest_path(
            test_state.p2_pos,
            GRID_SIZE-1,
            test_state
        )

        # Wall is valid only if both paths exist
        return p1_path is not None and p2_path is not None

    # Breadth First Search algorithm
    # Finds shortest path to target row
    def bfs_shortest_path(self, start, target_row, state):

        # Queue stores current position and path taken
        queue = deque([(start, [])])

        # Track visited cells to avoid loops
        visited = {start}

        while queue:

            # Get next cell from queue
            (c, r), path = queue.popleft()

            # Goal reached
            if r == target_row:
                return path

            # Explore adjacent cells
            for adj in self.get_adjacent(c, r, state):

                # Visit only unvisited cells
                if adj not in visited:
                    visited.add(adj)

                    # Add new path into queue
                    queue.append((adj, path + [adj]))

        # No path found
        return None