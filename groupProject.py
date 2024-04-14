import my_enums
from PdWorld import PdWorld
from Experiment import Experiment
from LearningAlgorithm import LearningAlgorithm
from Visualizer import Visualizer


visualizer = Visualizer()

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

initial_state = (red_agent[0][0], red_agent[0][1], blue_agent[0][0], blue_agent[0][1], black_agent[0][0], black_agent[0][1], 0, 0, 0, False, False, False, False, False, False)
    
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


q_table_x1_a, paths_x1_a, completions_x1_a = experiment_1.run_experiment()
q_table_x1_a_per_agent, paths_x1_a_per_agent, completions_x1_a_per_agent = experiment_1.run_experiment_q_per_agent()


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
q_table_x1_b_per_agent, paths_x1_b_per_agent, completions_x1_b_per_agent = experiment_1.run_experiment_q_per_agent()

second_exploration_method_per_episode = [my_enums.ExplorationMethod.PEXPLOIT]

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
q_table_x1_c_per_agent, paths_x1_c_per_agent, completions_x1_c_per_agent = experiment_1.run_experiment_q_per_agent()

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
q_table_x2_per_agent, paths_x2_per_agent, completions_x2_per_agent = experiment_2.run_experiment_q_per_agent()

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
q_table_x3_a_per_agent, paths_x3_a_per_agent, completions_x3_a_per_agent = experiment_3_a.run_experiment_q_per_agent()

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
q_table_x3_b_per_agent, paths_x3_b_per_agent, completions_x3_b_per_agent = experiment_3_b.run_experiment_q_per_agent()


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
q_table_x4_per_agent, paths_x4_per_agent, completions_x4_per_agent = experiment_4.run_experiment_q_per_agent()


#COMBINED Q TABLE DISPLAY
visualizer.print_min_max_vals(q_table_x1_a, "x1_a")
visualizer.print_min_max_vals(q_table_x1_b, "x1_b")
visualizer.print_min_max_vals(q_table_x1_c, "x1_c")
visualizer.print_min_max_vals(q_table_x2, "x2")
visualizer.print_min_max_vals(q_table_x3_a, "x3_a")
visualizer.print_min_max_vals(q_table_x3_b, "x3_b")
visualizer.print_min_max_vals(q_table_x4, "x4")

visualizer.plot_completion_steps(completions_x1_a, "Experiment 1a")
visualizer.plot_completion_steps(completions_x1_b, "Experiment 1b")
visualizer.plot_completion_steps(completions_x1_c, "Experiment 1c")
visualizer.plot_completion_steps(completions_x2, "Experiment 2")
visualizer.plot_completion_steps(completions_x3_a, "Experiment 3a")
visualizer.plot_completion_steps(completions_x3_b, "Experiment 3b")
visualizer.plot_completion_steps(completions_x4, "Experiment 4")

visualizer.plot_paths(paths_x1_a)
visualizer.plot_paths(paths_x1_b)
visualizer.plot_paths(paths_x1_c)
visualizer.plot_paths(paths_x2)
visualizer.plot_paths(paths_x3_a)
visualizer.plot_paths(paths_x3_b)
visualizer.plot_paths(paths_x4)

#INDIVIDUAL Q TABLE DISPLAY
visualizer.print_min_max_vals(q_table_x1_a_per_agent[0], "x1_a red")
visualizer.print_min_max_vals(q_table_x1_a_per_agent[1], "x1_a blue")
visualizer.print_min_max_vals(q_table_x1_a_per_agent[2], "x1_a black")

visualizer.print_min_max_vals(q_table_x1_b_per_agent[0], "x1_b red")
visualizer.print_min_max_vals(q_table_x1_b_per_agent[1], "x1_b blue")
visualizer.print_min_max_vals(q_table_x1_b_per_agent[2], "x1_b black")

visualizer.print_min_max_vals(q_table_x1_c_per_agent[0], "x1_c red")
visualizer.print_min_max_vals(q_table_x1_c_per_agent[1], "x1_c blue")
visualizer.print_min_max_vals(q_table_x1_c_per_agent[2], "x1_c black")

visualizer.print_min_max_vals(q_table_x2_per_agent[0], "x2_a red")
visualizer.print_min_max_vals(q_table_x2_per_agent[1], "x2_a blue")
visualizer.print_min_max_vals(q_table_x2_per_agent[2], "x2_a black")

visualizer.print_min_max_vals(q_table_x3_a_per_agent[0], "x3_a red")
visualizer.print_min_max_vals(q_table_x3_a_per_agent[1], "x3_a blue")
visualizer.print_min_max_vals(q_table_x3_a_per_agent[2], "x3_a black")

visualizer.print_min_max_vals(q_table_x3_b_per_agent[0], "x3_a red")
visualizer.print_min_max_vals(q_table_x3_b_per_agent[1], "x3_b blue")
visualizer.print_min_max_vals(q_table_x3_b_per_agent[2], "x3_b black")

visualizer.print_min_max_vals(q_table_x4_per_agent[0], "x1_a red")
visualizer.print_min_max_vals(q_table_x4_per_agent[1], "x4 blue")
visualizer.print_min_max_vals(q_table_x4_per_agent[2], "x4 black")

visualizer.plot_completion_steps(completions_x1_a_per_agent, "Experiment 1a Per Agent Q Table")
visualizer.plot_completion_steps(completions_x1_b_per_agent, "Experiment 1b Per Agent Q Table")
visualizer.plot_completion_steps(completions_x1_c_per_agent, "Experiment 1c Per Agent Q Table")
visualizer.plot_completion_steps(completions_x2_per_agent, "Experiment 2 Per Agent Q Table")
visualizer.plot_completion_steps(completions_x3_a_per_agent, "Experiment 3a Per Agent Q Table")
visualizer.plot_completion_steps(completions_x3_b_per_agent, "Experiment 3b Per Agent Q Table")
visualizer.plot_completion_steps(completions_x4_per_agent, "Experiment 4 Per Agent Q Table")

visualizer.plot_paths(paths_x1_a_per_agent)
visualizer.plot_paths(paths_x1_b_per_agent)
visualizer.plot_paths(paths_x1_c_per_agent)
visualizer.plot_paths(paths_x2_per_agent)
visualizer.plot_paths(paths_x3_a_per_agent)
visualizer.plot_paths(paths_x3_b_per_agent)
visualizer.plot_paths(paths_x4_per_agent)
