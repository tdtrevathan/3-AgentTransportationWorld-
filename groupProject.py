import my_enums
from PdWorld import PdWorld
from Experiment import Experiment
from LearningAlgorithm import LearningAlgorithm
from Visualizer import HeatMapGenerator


def print_min_max_vals(my_dict):
    # Finding the key with the maximum value
    max_key = max(my_dict, key=lambda k: my_dict[k])
    max_value_pair = (max_key, my_dict[max_key])

    # Finding the key with the minimum value
    min_key = min(my_dict, key=lambda k: my_dict[k])
    min_value_pair = (min_key, my_dict[min_key])

    print(f"Maximum key-value pair: {max_value_pair}")
    print(f"Minimum key-value pair: {min_value_pair}")


def plot_completion_steps(data, title):
    import matplotlib.pyplot as plt
    import numpy as np
    
    print(sum(data[0]))
    print(sum(data[1]))
    # Calculate the maximum length of the sublists to determine the number of x-ticks needed
    max_length = max(len(sublist) for sublist in data)

    # Prepare the x values based on the maximum length
    x = np.arange(max_length)

    # Width of each bar
    width = 0.35

    # Create a plot
    fig, ax = plt.subplots()

    # Plot each sublist as a set of bars
    for idx, sublist in enumerate(data):
        # Ensure that the length of each sublist matches the max_length by filling missing values with zeros
        y_values = sublist + [0] * (max_length - len(sublist))

        # Offset the x values for each set of bars
        x_offsets = x - width/2 + idx * width

        # Plot bars
        ax.bar(x_offsets, y_values, width, label=f'Run {idx + 1}')

    # Add labels and titles
    ax.set_title(f'{title} Steps to Completion Per Episode')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Steps to Completion')
    ax.set_ylim(0,2200)
    # Adding x-ticks (optional, improves clarity)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{i}' for i in x])

    # Add a legend to distinguish different sets
    ax.legend()

    # Show the plot
    plt.show()
    
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

initial_state = (red_agent[0][0], red_agent[0][1], blue_agent[0][0], blue_agent[0][1], black_agent[0][0], black_agent[0][1], 0, 0, 0, 5, 5, 5, 0, 0, 0)
    
total_steps = 9000
alpha = 0.1
gamma = 0.9

initial_steps = 1000
second_phase_steps = 8500

algorithm = my_enums.Algorithm.QLEARNING
learningAlgorithm = LearningAlgorithm(algorithm, alpha, gamma)

#episodes refer to runs essentially.
#the run could end due to all blocks being returned for example
#but this doesnt mean that the experiment is over
num_episodes =  1

#runs refers to how many time the entire experiment should be run
runs = 5

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


q_table_x1_a, paths_x1_a, completions_x1_a = experiment_1.run_experiment()

plot_completion_steps(completions_x1_a, "Experiment 1a")
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


q_table_x1_b, paths_x1_b, completions_x1_b = experiment_1.run_experiment()

second_exploration_method_per_episode = [my_enums.ExplorationMethod.PEXPLOIT]

plot_completion_steps(completions_x1_b, "Experiment 1b")
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


q_table_x1_c, paths_x1_c, completions_x1_c = experiment_1.run_experiment()

plot_completion_steps(completions_x1_c, "Experiment 1c")
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

q_table_x2, paths_x2, completions_x2 = experiment_2.run_experiment()

plot_completion_steps(completions_x2, "Experiment 2")
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

q_table_x3_a, paths_x3_a, completions_x3_a = experiment_3_a.run_experiment()

plot_completion_steps(completions_x3_a, "Experiment 3a")
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

q_table_x3_b, paths_x3_b, completions_x3_b = experiment_3_b.run_experiment()

plot_completion_steps(completions_x3_b, "Experiment 3b")
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

q_table_x4, paths_x4, completions_x4 = experiment_4.run_experiment()

plot_completion_steps(completions_x4, "Experiment 4")
print_min_max_vals(q_table_x4)

red_agent_index = 0
blue_agent_index = 1
black_agent_index = 2


visualizer = HeatMapGenerator(red_agent_index, blue_agent_index, black_agent_index)

visualizer.plot_paths(paths_x1_a)
visualizer.plot_paths(paths_x1_b)
visualizer.plot_paths(paths_x1_c)
visualizer.plot_paths(paths_x2)
visualizer.plot_paths(paths_x3_a)
visualizer.plot_paths(paths_x3_b)
visualizer.plot_paths(paths_x4)
