class PdWorld:
    def __init__(self, rows, cols, pickup_locations, dropoff_locations, red_agent, blue_agent, black_agent):
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


    def transition(self, position, action):
        x, y = position
        if action == 'up':
            new_position = (max(x-1, 0), y)
        elif action == 'down':
            new_position =  (min(x+1, self.rows-1), y)
        elif action == 'left':
            new_position =  (x, max(y-1, 0))
        elif action == 'right':
            new_position =  (x, min(y+1, self.rows-1))

        original = self.grid[position[0], position[1]]
        replacement = self.grid[new_position[0], new_position[1]]
        
        self.grid[new_position[0], new_position[1]] = original
        self.grid[position[0], position[1]] = replacement
        
        return -1, new_position
        
    def performAction(self, position, action):
        if (action == 'pickup' or action == 'dropoff'):
            self.transition(position, action)
        else:
            if action == 'pickup':
                #impliment pickup
                return state
            elif action == 'pickup':
                #impliment pickup
                return state
            

#pickup reward = 13
#dropoff reward = 13
#movement penalty = -1