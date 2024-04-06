import my_enums
from PdWorld import PdWorld
from Experiment import Experiment
from LearningAlgorithm import LearningAlgorithm

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


world = PdWorld(MAX_X, MAX_Y, BLOCK_CAPACITY, pickup_locations, dropoff_locations, (red_agent, my_enums.Agent.RED), (blue_agent, my_enums.Agent.BLUE), (black_agent, my_enums.Agent.BLACK), MOVEMENT_PENALTY, BLOCK_REWARD)

#red_x, red_y, blue_x, blue_y, black_x, black_y, red_carry, blue_carry, black_carry, p1_blocks, p2_blocks, p3_blocks, d1_blocks, d2_blocks, d3_blocks
initial_state = (2, 2, 2, 4, 2, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0)
    
total_steps = 9000
alpha = 0.3
gamma = 0.5

initial_steps = 500
second_phase_steps = 8500

algorithm = my_enums.Algorithm.QLEARNING
learningAlgorithm = LearningAlgorithm(algorithm, alpha, gamma)

#episodes refer to runs essentially.
#the run could end due to all blocks being returned for example
#but this doesnt mean that the experiment is over
num_episodes =  3

second_exploration_method_per_episode = [my_enums.ExplorationMethod.PRANDOM,
                                         my_enums.ExplorationMethod.PGREED,
                                         my_enums.ExplorationMethod.PEXPLOIT]

num_episodes = len(second_exploration_method_per_episode)

experiment = Experiment(world,
                        total_steps,
                        initial_steps,
                        second_phase_steps,
                        num_episodes,
                        initial_state,
                        learningAlgorithm,
                        second_exploration_method_per_episode)

experiment.run_experiment()

