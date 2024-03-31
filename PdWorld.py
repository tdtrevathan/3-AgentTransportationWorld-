import my_enums

class PdWorld:
    def __init__(self, 
                 rows, 
                 cols, 
                 block_capacity, 
                 pickup_locations, 
                 dropoff_locations, 
                 red_agent, 
                 blue_agent, 
                 black_agent, 
                 movement_penalty, 
                 block_reward):
        
        self.rows = rows
        self.cols = cols
        self.block_capacity = block_capacity
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.pickup_locations = pickup_locations  # List of tuples (row, col)
        self.dropoff_locations = dropoff_locations  # List of tuples (row, col)
        self.black_agent = black_agent
        self.blue_agent = blue_agent
        self.red_agent = red_agent
        self.movement_penalty = movement_penalty
        self.block_reward = block_reward
        self._init_locations()
        self._init_block_capacities()
        self._init_carry()

    def _init_locations(self):
        for row, col in self.pickup_locations:
            print('pickup')
            print(row)
            print(col)
            self.grid[row][col] = 'P'
        for row, col in self.dropoff_locations:
            print('dropoff')
            print(row)
            print(col)
            self.grid[row][col] = 'D'
        for row, col in self.black_agent:
            print('blue')
            print(row)
            print(col)
            self.grid[row][col] = 'b'
        for row, col in self.blue_agent:
            print('black')
            print(row)
            print(col)
            self.grid[row][col] = 'B'
        for row, col in self.red_agent:
            print('red')
            print(row)
            print(col)
            self.grid[row][col] = 'R'
    
    def _init_block_capacities(self):
        self.pickup_dictionary = { 
            self.pickup_locations[0]: self.block_capacity, 
            self.pickup_locations[1]: self.block_capacity, 
            self.pickup_locations[2]: self.block_capacity 
        }

        self.dropoff_dictionary = { 
            self.dropoff_locations[0]: 0, 
            self.dropoff_locations[1]: 0, 
            self.dropoff_locations[2]: 0 
        }
    
    def _init_carry(self):
        self.red_carry = 0
        self.blue_carry = 0
        self.black_carry = 0

    def display(self):
        self._init_locations()
        for row in self.grid:
            print('|' + '|'.join(row) + '|')

    def is_action_applicable(self, action, agent):
    
        grid_max_x, grid_max_y = self.rows - 1, self.cols - 1 

        position, carrying_block = self.get_agent_position_and_block_status(agent)

        agent_x, agent_y = position[0]

        # Check if moving off the grid
        if action == my_enums.Actions.UP and agent_y == 0:
            return False
        if action == my_enums.Actions.DOWN and agent_y == grid_max_x:
            return False
        if action == my_enums.Actions.LEFT and agent_x == 0:
            return False
        if action == my_enums.Actions.RIGHT and agent_x == grid_max_y:
            return False

        # Check if trying to pick up or drop off without being in the correct location
        if action == my_enums.Actions.PICKUP or action == my_enums.Actions.DROPOFF:
            
            applicable = False

            if action == my_enums.Actions.PICKUP:
                # Can only pick up if not carrying a block and at a pickup location with available blocks
                applicable = not carrying_block and any(loc in self.pickup_locations and self.pickup_dictionary[loc] > 0 for loc in position)
            elif action == my_enums.Actions.DROPOFF:
                # Can only drop off if carrying a block and at a dropoff location that is not full
                applicable = carrying_block and any(loc in self.dropoff_locations and self.dropoff_dictionary[loc] < self.block_capacity for loc in position)

            return applicable

        # Default case: if the action is not one of the above, it's applicable
        return True
    
    def transition(self, position, action, agent):
        x, y = position[0]

        if action == my_enums.Actions.UP:
            new_position = (max(x-1, 0), y)
        elif action == my_enums.Actions.DOWN:
            new_position =  (min(x+1, self.rows-1), y)
        elif action == my_enums.Actions.LEFT:
            new_position =  (x, max(y-1, 0))
        else: #action == my_enums.Actions.RIGHT
            new_position =  (x, min(y+1, self.rows-1))

        if agent == my_enums.Agent.RED:
            self.red_agent = [new_position]
            
        elif agent == my_enums.Agent.BLUE:
            self.blue_agent = [new_position]
        else:
            self.black_agent = [new_position]
            
    def update_carry(self, agent, update):
        if agent == my_enums.Agent.RED:
            self.red_carry = update
        elif agent == my_enums.Agent.BLUE:
            self.blue_carry = update
        else: # black agent
            self.black_carry = update

    def get_agent_position_and_block_status(self, agent):

        if agent == my_enums.Agent.RED:
            return self.red_agent, self.red_carry
        elif agent == my_enums.Agent.BLUE:
            return self.blue_agent, self.blue_carry
        else:
            return self.black_agent, self.black_carry
    
    def performAction(self, action, agent):
        
        terminal_state_reached = False
        
        position, _ = self.get_agent_position_and_block_status(agent)

        if (action != my_enums.Actions.PICKUP and action != my_enums.Actions.DROPOFF):
            reward = self.movement_penalty
            
            self.transition(position, action, agent)
        else:
            reward = self.block_reward
            
            if action == my_enums.Actions.PICKUP:
                carry_status = 1
                self.pickup_dictionary[position] -= 1
            
            elif action == my_enums.Actions.PICKUP:
                carry_status  = 0
                self.dropoff_dictionary[position] += 1
            
            self.update_carry(action, agent, carry_status)
        
                    
        return reward, terminal_state_reached, self.get_updated_state()
    
    def get_updated_state(self):

        return (self.red_agent[0][0],
                self.red_agent[0][1],
                self.blue_agent[0][0],
                self.blue_agent[0][1],
                self.black_agent[0][0],
                self.black_agent[0][1],
                self.red_carry,
                self.blue_carry,
                self.black_carry,
                self.pickup_dictionary[self.pickup_locations[0]],
                self.pickup_dictionary[self.pickup_locations[1]],
                self.pickup_dictionary[self.pickup_locations[2]],
                self.dropoff_dictionary[self.dropoff_locations[0]],
                self.dropoff_dictionary[self.dropoff_locations[1]],
                self.dropoff_dictionary[self.dropoff_locations[2]]
            )

            

    