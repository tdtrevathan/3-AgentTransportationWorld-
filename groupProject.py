import numpy as np
from enum import Enum
from PdWorld import PdWorld

class Actions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    PICKUP = 5
    DROPOFF = 6

class ExplorationMethod(Enum):
    PRANDOM = 1
    PEXPLOIT = 2
    PGREED = 3

def generate_surrounding_statuses(agent_position, grid):
    """
    Generates the statuses of the cells surrounding the agent in the grid.

    Parameters:
    - agent_position: A tuple (x, y) representing the agent's current position.
    - grid: A 2D list representing the grid environment where each cell has a type defined by CellType enum.

    Returns:
    - A dictionary with the status of the cells around the agent in each direction (up, right, down, left).
    """
    x, y = agent_position
    surroundings = {
        'up': None,
        'right': None,
        'down': None,
        'left': None
    }

    if x > 0:
        surroundings['up'] = grid[x - 1][y]
    if y < len(grid[0]) - 1:
        surroundings['right'] = grid[x][y + 1]
    if x < len(grid) - 1:
        surroundings['down'] = grid[x + 1][y]
    if y > 0:
        surroundings['left'] = grid[x][y - 1]

   # # Convert grid values to CellType enum
   # for direction in surroundings:
   #     cell_value = surroundings[direction]
   #     surroundings[direction] = CellType(cell_value) if cell_value is not None else None

    return surroundings


def is_action_applicable(action, state, pickup_locations, dropoff_locations, pickup_status, dropoff_status):
    
    grid_max_x, grid_max_y = MAX_X - 1, MAX_Y - 1 
     
    agent_x, agent_y, carrying_block = state[:3]
    
    # Check if moving off the grid
    if action == "up" and agent_y == 0:
        return False
    if action == "down" and agent_y == grid_max_x:
        return False
    if action == "left" and agent_x == 0:
        return False
    if action == "right" and agent_x == grid_max_y:
        return False

    # Check if trying to pick up or drop off without being in the correct location
    if action == "pickup" or action == "dropoff":
        adjacent_locations = [(agent_x-1, agent_y), (agent_x+1, agent_y), (agent_x, agent_y-1), (agent_x, agent_y+1)]
        applicable = False
        
        if action == "pickup":
            # Can only pick up if not carrying a block and at a pickup location with available blocks
            applicable = not carrying_block and any(loc in pickup_locations and pickup_status[loc] > 0 for loc in adjacent_locations)
        elif action == "dropoff":
            # Can only drop off if carrying a block and at a dropoff location that is not full
            applicable = carrying_block and any(loc in dropoff_locations and dropoff_status[loc] < BLOCK_CAPACITY for loc in adjacent_locations)

        return applicable
    
    # Default case: if the action is not one of the above, it's applicable
    return True



def update_q_value(q_table, 
                   state,
                   action,
                   reward,
                   next_state,
                   alpha,
                   gamma,
                   actions,
                   pickup_locations,
                   dropoff_locations,
                   pickup_ammounts,
                   dropoff_ammounts):
    
    # Get the Q-values for the next state, filter for applicable actions only
    next_q_values = np.array([q_table[next_state, a] if is_action_applicable(a, next_state, pickup_locations, dropoff_locations, pickup_ammounts, dropoff_ammounts) else -np.inf for a in range(actions)])
    
    # Compute the maximum Q-value for the next state from applicable actions
    max_next_q = np.max(next_q_values)
    
    # Q-learning formula
    q_table[state, action] = (1 - alpha) * q_table[state, action] + alpha * (reward + gamma * max_next_q)

#def sarsa_update(state, action, reward, next_state, next_action):
# Implement SARSA update

#def select_action(state, policy):
# Action selection based on the current policy

#def run_experiment(environment, agents, num_steps, policy):
# Main loop for running experiments

# Initialization of environment and agents

# Running experiments with different configurations

# Visualization and analysis of results

BLOCK_CAPACITY = 5

# Define movement boundaries
MAX_X, MAX_Y = 5, 5

q_table = {}  # Use a dict for sparse storage

pickup_locations = [(0, 4), (1, 3), (3, 2)]
dropoff_locations = [(0, 0), (2, 0), (3, 4)]
blue_agent = [(2,2)]
black_agent = [(0,2)]
red_agent = [(4,2)]

total_steps = 9000
alpha = 0.3
gamma = 0.5

initial_steps = 500
second_phase_steps = 8500


world = PdWorld(MAX_X, MAX_Y, pickup_locations, dropoff_locations, black_agent, blue_agent, red_agent)
world.display()

pickup_dictionary = { 
                        pickup_locations[0]: 5, 
                        pickup_locations[1]: 5, 
                        pickup_locations[2]: 5 
                    }

dropoff_dictionary = { 
                        dropoff_locations[0]: 0, 
                        dropoff_locations[1]: 0, 
                        dropoff_locations[2]: 0 
                    }

first_action = Actions.LEFT #Chosen left arbitrarily since we dont have a random or evaluation function yet

#red_x, red_y, blue_x, blue_y, black_x, black_y, red_carry, blue_carry, black_carry, p1_blocks, p2_blocks, p3_blocks
redInitialState = (2, 2, 2, 4, 2, 0, 0, 0, 0, 5, 5, 5)

q_table[(redInitialState, first_action)] = 0

#get next action

num_episodes =  1

state = redInitialState
for episode in range(num_episodes):
    #state = env.reset()  # Assuming an environment 'env' that can reset to start state
    
    num_actions = len(Actions)
    
    done = False
    count = 0
    while not done:
        # Step 2: Select action randomly
        action = np.random.choice([a for a in range(num_actions) if is_action_applicable(a, state, pickup_locations, dropoff_locations, pickup_dictionary, dropoff_dictionary)])
        
        # Execute the action, get the new state and reward
        next_state, reward, done = world.transition(state, action)
        
        # Step 3: Update the Q-table  actions, pickups, dropoffs
        update_q_value(q_table, state, action, reward, next_state, alpha, gamma, num_actions, pick)
        
        # Prepare for the next iteration
        state = next_state
        
        if count >= 9000:
            done = True


print(q_table)
