import my_enums
from PdWorld import PdWorld
from Experiment import Experiment
from LearningAlgorithm import LearningAlgorithm
from HeatMapGenerator import HeatMapGenerator


def print_min_max_vals(my_dict):
    # Finding the key with the maximum value
    max_key = max(my_dict, key=lambda k: my_dict[k])
    max_value_pair = (max_key, my_dict[max_key])

    # Finding the key with the minimum value
    min_key = min(my_dict, key=lambda k: my_dict[k])
    min_value_pair = (min_key, my_dict[min_key])

    print(f"Maximum key-value pair: {max_value_pair}")
    print(f"Minimum key-value pair: {min_value_pair}")

BLOCK_CAPACITY = 5

# Define movement boundaries
MAX_X, MAX_Y = 5, 5

MOVEMENT_PENALTY = -1
BLOCK_REWARD = 13

q_table = {}  # Use a dict for sparse storage

pickup_locations = [(0, 4), (1, 3), (4, 1)]
dropoff_locations = [(0, 0), (2, 0), (3, 4)]
blue_agent = [(4,2)]
black_agent =[(0,2)]
red_agent = [(2,2)]


#EXPERIMENT 1

world = PdWorld(MAX_X, MAX_Y, BLOCK_CAPACITY, pickup_locations, dropoff_locations, (red_agent, my_enums.Agent.RED), (blue_agent, my_enums.Agent.BLUE), (black_agent, my_enums.Agent.BLACK), MOVEMENT_PENALTY, BLOCK_REWARD)

print('initail world')
world.display()
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
num_episodes =  1

#runs refers to how many time the entire experiment should be run
runs = 2

second_exploration_method_per_episode = [my_enums.ExplorationMethod.PRANDOM]

num_episodes = len(second_exploration_method_per_episode)

experiment_1 = Experiment(world,
                        total_steps,
                        initial_steps,
                        second_phase_steps,
                        num_episodes,
                        initial_state,
                        learningAlgorithm,
                        second_exploration_method_per_episode,
                        runs)


q_table_x1_a = experiment_1.run_experiment()

print_min_max_vals(q_table_x1_a)

second_exploration_method_per_episode = [my_enums.ExplorationMethod.PGREEDY]

experiment_1 = Experiment(world,
                        total_steps,
                        initial_steps,
                        second_phase_steps,
                        num_episodes,
                        initial_state,
                        learningAlgorithm,
                        second_exploration_method_per_episode,
                        runs)


q_table_x1_b = experiment_1.run_experiment()

second_exploration_method_per_episode = [my_enums.ExplorationMethod.PEXPLOIT]

print_min_max_vals(q_table_x1_b)

experiment_1 = Experiment(world,
                        total_steps,
                        initial_steps,
                        second_phase_steps,
                        num_episodes,
                        initial_state,
                        learningAlgorithm,
                        second_exploration_method_per_episode,
                        runs)


q_table_x1_c = experiment_1.run_experiment()

print_min_max_vals(q_table_x1_c)


#EXPERIMENT 2

num_episodes = 1
second_exploration_method_per_episode = [my_enums.ExplorationMethod.PEXPLOIT]
algorithm = my_enums.Algorithm.SARSA
learningAlgorithm = LearningAlgorithm(algorithm, alpha, gamma)

num_episodes = len(second_exploration_method_per_episode)

experiment_2 = Experiment(world,
                        total_steps,
                        initial_steps,
                        second_phase_steps,
                        num_episodes,
                        initial_state,
                        learningAlgorithm,
                        second_exploration_method_per_episode,
                        runs)

q_table_x2 = experiment_2.run_experiment()
print_min_max_vals(q_table_x2)

#EXPERIMENT 3

#First new alpha value

alpha = 0.15
learningAlgorithm = LearningAlgorithm(algorithm, alpha, gamma)

experiment_3_a = Experiment(world,
                        total_steps,
                        initial_steps,
                        second_phase_steps,
                        num_episodes,
                        initial_state,
                        learningAlgorithm,
                        second_exploration_method_per_episode,
                        runs)

q_table_x3_a = experiment_3_a.run_experiment()
print_min_max_vals(q_table_x3_a)

#second new alpha value
alpha = 0.45
learningAlgorithm = LearningAlgorithm(algorithm, alpha, gamma)

experiment_3_b = Experiment(world,
                        total_steps,
                        initial_steps,
                        second_phase_steps,
                        num_episodes,
                        initial_state,
                        learningAlgorithm,
                        second_exploration_method_per_episode,
                        runs)

q_table_x3_b = experiment_3_b.run_experiment()

print_min_max_vals(q_table_x3_b)
#EXPERIMENT 4

alpha = 0.3
gamma = 0.5
track_terminals = True
new_pickup_locations = [(4, 2), (3, 3), (2, 4)]

experiment_4 = Experiment(world,
                        total_steps,
                        initial_steps,
                        second_phase_steps,
                        num_episodes,
                        initial_state,
                        learningAlgorithm,
                        second_exploration_method_per_episode,
                        runs,
                        track_terminals,
                        new_pickup_locations)

q_table_x4 = experiment_4.run_experiment()

print_min_max_vals(q_table_x4)
red_agent_index = 0
blue_agent_index = 1
black_agent_index = 3


heat_map_generator = HeatMapGenerator(red_agent_index, blue_agent_index, black_agent_index)


heat_map_generator.run_heat_maps(q_table_x1_a, 'Experiment 1a')
heat_map_generator.run_heat_maps(q_table_x1_b, 'Experiment 1b')
heat_map_generator.run_heat_maps(q_table_x1_c, 'Experiment 1c')
heat_map_generator.run_heat_maps(q_table_x2, 'Experiment 2')
heat_map_generator.run_heat_maps(q_table_x3_a, 'Experiment 3a')
heat_map_generator.run_heat_maps(q_table_x3_b, 'Experiment 3b')
heat_map_generator.run_heat_maps(q_table_x4, 'Experiment 4')

