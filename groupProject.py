from enum import Enum

class Actions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    PICKUP = 5
    DROPOFF = 6

class Cell_Stauts(Enum):
    EMPTY = 1
    OCCUPIED = 2
    PICKUP_STATION = 3
    DROPOFF_STATION = 4


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

class Agent:
    def __init__(self, start_position, agent_type):
        self.position = start_position
        self.agent_type = agent_type
        self.has_block = False

    def move(self, action, grid_size):
        # Update self.position based on the action
        # Ensure movements are within grid bounds
        pass

    def update_status(self, environment):
        # Handle interactions, like picking up or dropping a block
        pass

def get_valid_actions(surroundings, carrying_block):

    available_actions = []
    # Check for movement actions based on surroundings
    if surroundings[0] == Cell_Status.DEMPTY:  # Up is free
        actions.append(Actions.UP)
    if surroundings[1] == Cell_Status.EMPTY:  # Right is free
        actions.append(Actions.RIGHT)
    if surroundings[2] == Cell_Status.EMPTY:  # Down is free
        actions.append(Actions.DOWN)
    if surroundings[3] == Cell_Status.EMPTY:  # Left is free
        actions.append(Actions.LEFT)

    # Check for pickup action
    if not carrying_block and (PICKUP_STATION in surroundings):
        actions.append(Actions.PICKUP)

    # Check for drop-off action
    if carrying_block and (DROPOFF_STATION in surroundings):
        actions.append(Actions.DROPOFF)

    return available_actions


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

#def q_learning_update(state, action, reward, next_state):
    # Implement Q-learning update

#def sarsa_update(state, action, reward, next_state, next_action):
# Implement SARSA update

#def select_action(state, policy):
# Action selection based on the current policy

#def run_experiment(environment, agents, num_steps, policy):
# Main loop for running experiments

# Initialization of environment and agents

# Running experiments with different configurations

# Visualization and analysis of results

q_table = {}  # Use a dict for sparse storage

pickup_locations = [(0, 4), (1, 3), (3, 2)]
dropoff_locations = [(0, 0), (2, 0), (3, 4)]
blue_agent = [(2,2)]
black_agent = [(0,2)]
red_agent = [(4,2)]
world = PdWorld(5, 5, pickup_locations, dropoff_locations, black_agent, blue_agent, red_agent)
world.display()

#surroundings = generate_surrounding_statuses([4,2], world.grid)

print(surroundings)

