import numpy as np
import my_enums
from PdWorld import PdWorld

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


def update_q_value(q_table, 
                   state,
                   action,
                   reward,
                   next_state,
                   alpha,
                   gamma,
                   actions,
                   agent,
                   world):

    # Get the Q-values for the next state, filter for applicable actions only
    next_q_values = np.array([q_table.get((next_state, a), 0) if world.is_action_applicable(a, agent) else -np.inf for a in range(actions)])
    
    # Compute the maximum Q-value for the next state from applicable actions
    max_next_q = np.max(next_q_values)
    
    # Q-learning formula
    q_table[state, action] = (1 - alpha) * q_table.get((state, action), 0) + alpha * (reward + gamma * max_next_q)

#def sarsa_update(state, action, reward, next_state, next_action):
# Implement SARSA update

#def select_action(state, policy):
# Action selection based on the current policy

#def run_experiment(environment, agents, num_steps, policy):
# Main loop for running experiments

# Initialization of environment and agents

# Running experiments with different configurations

# Visualization and analysis of results

def get_next_agent(agent):
    if(agent == my_enums.Agent.RED):
        return my_enums.Agent.BLUE
    elif(agent == my_enums.Agent.BLUE):
        return my_enums.Agent.BLACK
    else:
        return my_enums.Agent.RED

BLOCK_CAPACITY = 5

# Define movement boundaries
MAX_X, MAX_Y = 5, 5

MOVEMENT_PENALTY = -1
BLOCK_REWARD = 13

q_table = {}  # Use a dict for sparse storage

pickup_locations = [(0, 4), (1, 3), (3, 2)]
dropoff_locations = [(0, 0), (2, 0), (3, 4)]
blue_agent = [(2,2)]
black_agent =[(0,2)]
red_agent = [(4,2)]

total_steps = 9000
alpha = 0.3
gamma = 0.5

initial_steps = 500
second_phase_steps = 8500


world = PdWorld(MAX_X, MAX_Y, BLOCK_CAPACITY, pickup_locations, dropoff_locations, (red_agent, my_enums.Agent.RED), (blue_agent, my_enums.Agent.BLUE), (black_agent, my_enums.Agent.BLACK), MOVEMENT_PENALTY, BLOCK_REWARD)
world.display()

#red_x, red_y, blue_x, blue_y, black_x, black_y, red_carry, blue_carry, black_carry, p1_blocks, p2_blocks, p3_blocks, d1_blocks, d2_blocks, d3_blocks
redInitialState = (2, 2, 2, 4, 2, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0)

num_episodes =  1
agent = my_enums.Agent.RED
state = redInitialState

if ([(0,1)] == [(2,1)]):
    print('contents dont matter')


for episode in range(num_episodes):
    #state = env.reset()  # Assuming an environment 'env' that can reset to start state
    
    num_actions = len(my_enums.Actions)
    
    done = False
    count = 0
    while not done:
        # Step 2: Select action randomly
        action = np.random.choice([a for a in my_enums.Actions if world.is_action_applicable(a, agent)])
        print('action')
        print(action)
        # Execute the action, get the new state and reward
        reward, done, *next_state = world.performAction(action, agent)

        next_state = tuple(next_state[0])

        # Step 3: Update the Q-table  actions, pickups, dropoffs
        update_q_value(q_table, state, action, reward, next_state, alpha, gamma, num_actions, agent, world)
        
        # Prepare for the next iteration
        state = next_state
        
        count += 1
        agent = get_next_agent(agent)
        print("count: {}".format(count))
        print()
        world.display()
        if count >= 20:
            done = True

print(q_table)
