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
        
        self.agent_specific = False
        
        self._init_locations()
        self._init_block_capacities()
        self._init_carry()
        
        self._init_initial_values(rows, 
                 cols, 
                 block_capacity, 
                 pickup_locations, 
                 dropoff_locations, 
                 red_agent, 
                 blue_agent, 
                 black_agent, 
                 movement_penalty, 
                 block_reward)
     
     
     
        
    def _init_initial_values(self, 
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
        
        self.init_rows = rows 
        self.init_cols = cols
        self.init_block_capacity = block_capacity
        self.init_pickup_locations = pickup_locations
        self.init_dropoff_locations = dropoff_locations
        self.init_red_agent = red_agent
        self.init_blue_agent = blue_agent
        self.init_black_agent = black_agent
        self.init_movement_penalty = movement_penalty
        self.init_block_reward = block_reward

    def _init_locations(self):

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col] = ' '
        for row, col in self.pickup_locations:
            self.grid[row][col] = 'P'
        for row, col in self.dropoff_locations:
            self.grid[row][col] = 'D'
        for row, col in self.black_agent[0]:
            self.grid[row][col] = 'b'
        for row, col in self.blue_agent[0]:
            self.grid[row][col] = 'B'
        for row, col in self.red_agent[0]:
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
    
    def set_agent_specific(self, val):
        self.agent_specific = val
    
    def _init_carry(self):
        self.red_carry = 0
        self.blue_carry = 0
        self.black_carry = 0

    def is_dropoff_full(self, index):
        return self.dropoff_dictionary[self.dropoff_locations[index]] == 5
    
    def is_pickup_empty(self, index):
        return self.pickup_dictionary[self.pickup_locations[index]] == 0
    
    def display(self):
        self._init_locations()
        for row in self.grid:
            print('|' + '|'.join(row) + '|')

    def is_action_applicable(self, action, agent):
    
        grid_max_x, grid_max_y = self.rows - 1, self.cols - 1 

        position, carrying_block = self.get_agent_position_and_block_status(agent)

        potential_position = self.transition(position, action)

        if agent != self.blue_agent[1] and potential_position == self.blue_agent[0][0]:
            return False
        if agent != self.black_agent[1] and potential_position == self.black_agent[0][0]:
            return False
        if agent != self.red_agent[1] and potential_position == self.red_agent[0][0]:
            return False

        # Check if moving off the grid
        if action == my_enums.Actions.UP and potential_position[0] < 0:
            return False
        if action == my_enums.Actions.DOWN and potential_position[0] > grid_max_y:
            return False
        if action == my_enums.Actions.LEFT and potential_position[1] < 0:
            return False
        if action == my_enums.Actions.RIGHT and potential_position[1] > grid_max_x:
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
    
    def apply_transition(self, position, action, agent):

        new_position = self.transition(position, action)
        
        if agent == my_enums.Agent.RED:
            self.red_agent = [new_position], my_enums.Agent.RED
            
        elif agent == my_enums.Agent.BLUE:
            self.blue_agent = [new_position], my_enums.Agent.BLUE
        else:
            self.black_agent = [new_position], my_enums.Agent.BLACK
            
    def transition(self, position, action):
        y, x = position[0]

        if action == my_enums.Actions.UP:
            new_position = (y-1, x)
        elif action == my_enums.Actions.DOWN:
            new_position =  (y+1, x)
        elif action == my_enums.Actions.LEFT:
            new_position =  (y, x-1)
        else: #action == my_enums.Actions.RIGHT
            new_position =  (y, x+1)

        return new_position
            
    def update_carry(self, agent, update):
        if agent == my_enums.Agent.RED:
            self.red_carry = update
        elif agent == my_enums.Agent.BLUE:
            self.blue_carry = update
        else: # black agent
            self.black_carry = update

    def get_agent_position_and_block_status(self, agent):

        if agent == my_enums.Agent.RED:
            return self.red_agent[0], self.red_carry
        elif agent == my_enums.Agent.BLUE:
            return self.blue_agent[0], self.blue_carry
        else:
            return self.black_agent[0], self.black_carry
    
    def performAction(self, action, agent):
        
        terminal_state_reached = False
        
        position, _ = self.get_agent_position_and_block_status(agent)
        
        if (action != my_enums.Actions.PICKUP and action != my_enums.Actions.DROPOFF):
            reward = self.movement_penalty
            
            self.apply_transition(position, action, agent)
        else:
            reward = self.block_reward
            
            if action == my_enums.Actions.PICKUP:
                carry_status = 1
                self.pickup_dictionary[position[0]] -= 1
            
            elif action == my_enums.Actions.DROPOFF:
                carry_status  = 0
                self.dropoff_dictionary[position[0]] += 1

            self.update_carry(agent, carry_status)
                    
        return reward, terminal_state_reached, self.get_updated_state(agent)
    
    def dropoffs_are_full(self):
        droppoff_full_1 = self.dropoff_dictionary[self.dropoff_locations[0]] == self.block_capacity
        droppoff_full_2 = self.dropoff_dictionary[self.dropoff_locations[1]] == self.block_capacity
        droppoff_full_3 = self.dropoff_dictionary[self.dropoff_locations[2]] == self.block_capacity

        return droppoff_full_1 and droppoff_full_2 and droppoff_full_3
    
    def get_updated_state(self, agent):
        
        if(not self.agent_specific):
            return (self.red_agent[0][0][0],
                    self.red_agent[0][0][1],
                    self.blue_agent[0][0][0],
                    self.blue_agent[0][0][1],
                    self.black_agent[0][0][0],
                    self.black_agent[0][0][1],
                    self.red_carry,
                    self.blue_carry,
                    self.black_carry,
                    self.is_pickup_empty(0),
                    self.is_pickup_empty(1),
                    self.is_pickup_empty(2),
                    self.is_dropoff_full(0),
                    self.is_dropoff_full(1),
                    self.is_dropoff_full(2),
                )
        else:
            if(agent == my_enums.Agent.RED):
                return (self.red_agent[0][0][0],
                    self.red_agent[0][0][1],
                    self.red_carry,
                    self.is_pickup_empty(0),
                    self.is_pickup_empty(1),
                    self.is_pickup_empty(2),
                    self.is_dropoff_full(0),
                    self.is_dropoff_full(1),
                    self.is_dropoff_full(2),
                )
            elif(agent == my_enums.Agent.BLUE):
                return (
                    self.blue_agent[0][0][0],
                    self.blue_agent[0][0][1],
                    self.blue_carry,
                    self.is_pickup_empty(0),
                    self.is_pickup_empty(1),
                    self.is_pickup_empty(2),
                    self.is_dropoff_full(0),
                    self.is_dropoff_full(1),
                    self.is_dropoff_full(2),
                )
            else: #BLACK
                return (
                    self.black_agent[0][0][0],
                    self.black_agent[0][0][1],
                    self.black_carry,
                    self.is_pickup_empty(0),
                    self.is_pickup_empty(1),
                    self.is_pickup_empty(2),
                    self.is_dropoff_full(0),
                    self.is_dropoff_full(1),
                    self.is_dropoff_full(2),
                )

    def reset_initial_values(self):
        self.rows = self.init_rows 
        self.cols = self.init_cols
        self.block_capacity = self.init_block_capacity
        self.pickup_locations = self.init_pickup_locations
        self.dropoff_locations = self.init_dropoff_locations
        self.red_agent = self.init_red_agent
        self.blue_agent = self.init_blue_agent
        self.black_agent = self.init_black_agent
        self.movement_penalty = self.init_movement_penalty
        self.block_reward = self.init_block_reward
        self._init_block_capacities()
        self._init_carry()
        
    def shift_pickups(self, new_pickups):
        self.init_pickup_locations = new_pickups
        self.pickup_locations = new_pickups
        self._init_block_capacities()
        