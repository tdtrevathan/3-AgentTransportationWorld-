class PdWorld:
    def __init__(self, rows, cols, pickup_locations, dropoff_locations, black_agent, blue_agent, red_agent):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.pickup_locations = pickup_locations  # List of tuples (row, col)
        self.dropoff_locations = dropoff_locations  # List of tuples (row, col)
        self.black_agent = black_agent
        self.blue_agent = blue_agent
        self.red_agent = red_agent
        self._init_locations()

    def _init_locations(self):
        for row, col in self.pickup_locations:
            self.grid[row][col] = 'P'
        for row, col in self.dropoff_locations:
            self.grid[row][col] = 'D'
        for row, col in self.black_agent:
            self.grid[row][col] = 'b'
        for row, col in self.blue_agent:
            self.grid[row][col] = 'B'
        for row, col in self.red_agent:
            self.grid[row][col] = 'R'

    def display(self):
        for row in self.grid:
            print('|' + '|'.join(row) + '|')

def transition(state, action):
    x, y = state
    if action == 'up':
        return (max(x-1, 0), y)
    elif action == 'down':
        return (min(x+1, grid_size-1), y)
    elif action == 'left':
        return (x, max(y-1, 0))
    elif action == 'right':
        return (x, min(y+1, grid_size-1))
    elif action == 'pickup':
        #impliment pickup
        return state
    elif action == 'pickup':
        #impliment pickup
        return state
    else:
        return state  # No change for undefined actions
