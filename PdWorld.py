from enum import Enum
import my_enums

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
        else: #action == 'right'
            new_position =  (x, min(y+1, self.rows-1))

        original = self.grid[position[0]][position[1]]
        replacement = self.grid[new_position[0]][new_position[1]]
        
        self.grid[new_position[0]][new_position[1]] = original
        self.grid[position[0]][position[1]] = replacement
        
        return -1, new_position
    
    def get_agent_position_and_block_status(self, state, agent):
        print("steate")
        print(state)
        if agent == my_enums.Agent.RED:
            position = state[0], state[1]
            block_status = state[6]
            
        elif agent == my_enums.Agent.BLUE:
            position = state[2], state[3]
            block_status = state[7]
            
        else:
            position = state[4], state[5]
            block_status = state[8]
            
        return position, block_status
    
    def performAction(self, state, action, agent):
        print(action)
        
        position, block_status = self.get_agent_position_and_block_status(state, agent)

        if (action != 'pickup' and action != 'dropoff'):
            result = self.transition(position, action)
            return result[0], result[1], block_status, False
        else:
            if action == 'pickup':
                #impliment pickup
                block_status = 1
                return 13, position, block_status, False
            elif action == 'pickup':
                #impliment pickup
                block_status = 0
                return 13, position, block_status, False
            

            
            

#pickup reward = 13
#dropoff reward = 13
#movement penalty = -1