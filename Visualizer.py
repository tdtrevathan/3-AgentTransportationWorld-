import matplotlib.pyplot as plt
import numpy as np
import os
import my_enums
from prettytable import PrettyTable

class Visualizer:

    def plot_paths(self, paths):
        # Define the colors for each agent
        agent_colors = {
            my_enums.Agent.RED: 'r',
            my_enums.Agent.BLUE: 'b',
            my_enums.Agent.BLACK: 'k'
        }
        
        # Number of agents to create subplots
        num_agents = len(paths)
        fig, axes = plt.subplots(1, num_agents, figsize=(5*num_agents, 5))  # Adjust the figure size as needed


       # Initialize a dictionary to store the optimal path for each agent
        optimal_paths = {agent: [] for agent in paths.keys()}

        # Determine the optimal path for each agent based on the highest Q-value
        for agent, path in paths.items():

            current_state, _, _, _ = path[0]  # Assuming 'initial_state' is defined

            # Assuming the path is a sequence of (state, action, next state, q-value)
            for paths in path:  # Define your own termination condition
                # Find the action with the highest Q-value in the current state
                actions_and_q_values = [(a, q, ns) for s, a, ns, q in path if s == current_state]

                if not actions_and_q_values:
                    # If there are no actions from the current state, it may be a terminal state
                    break
                
                best_state = max(actions_and_q_values, key=lambda item: item[1])
                best_action = best_state[0]
                next_state = best_state[2]

                # Store the best action taken at the current state
                optimal_paths[agent].append((current_state, best_action, next_state))

                # Update the current state
                current_state = next_state
                
        # Loop over each agent and its dedicated subplot
        for ax, (agent, path) in zip(axes, optimal_paths.items()):
            for s, a, ns in path:
                # Calculate the difference (dx, dy) for the arrow
                dx = ns[0] - s[0]
                dy = ns[1] - s[1]

                # Draw the line with arrow
                ax.arrow(s[0], s[1], dx, dy, head_width=0.1, head_length=0.1, fc=agent_colors[agent], ec=agent_colors[agent])

            ax.set_xlim(-1,5)
            ax.set_ylim(-1,5)
            ax.set_aspect('equal')
            ax.set_title(f"Agent {agent}")
            ax.grid(True)

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Show the plot
        plt.show()
        
    def plot_completion_steps(self, data, title):

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
        ax.set_ylim(0,2600)
        # Adding x-ticks (optional, improves clarity)
        ax.set_xticks(x)
        ax.set_xticklabels([f'{i}' for i in x])

        # Add a legend to distinguish different sets
        ax.legend()

        # Show the plot
        plt.show()
        
    def print_min_max_vals(self, my_dict, title):
        # Finding the key with the maximum value
        max_key = max(my_dict, key=lambda k: my_dict[k])
        max_value_pair = (max_key, my_dict[max_key])

        # Finding the key with the minimum value
        min_key = min(my_dict, key=lambda k: my_dict[k])
        min_value_pair = (min_key, my_dict[min_key])

        print(title)
        print(f"Maximum key-value pair: {max_value_pair}")
        print(f"Minimum key-value pair: {min_value_pair}")

    def print_pretty_table(self, q_table):

        # Create a PrettyTable object
        table = PrettyTable()

        # Add columns
        table.field_names = ["State", "Action", "Q-Value"]

        # Add rows to the table
        for state_action, value in q_table.items():
            state, action = state_action
            table.add_row([state, action, round(value, 2)])  # Round for better readability

        # Print the table
        print(table)