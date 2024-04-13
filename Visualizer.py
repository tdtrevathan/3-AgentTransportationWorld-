import matplotlib.pyplot as plt
import numpy as np
import os
import my_enums

class HeatMapGenerator:
    
    def __init__(self, red_agent_index, blue_agent_index, black_agent_index):
        self.red_agent_index = red_agent_index
        self.blue_agent_index = blue_agent_index
        self.black_agent_index = black_agent_index
        
        # Assuming you have a function to get the max Q-value for an agent at a given position
    def get_max_q_value_for_position(self, agent_position, q_table, agent_index):
        max_q_value = -float('inf')  # Start with negative infinity as the max Q-value
    
        # Iterate over the Q-table entries
        for (state, action), q_value in q_table.items():
        
            # Check if the current state corresponds to the agent's position and carry status
            if state[agent_index * 2:agent_index * 2 + 2] == agent_position and state[6 + agent_index] in (0, 1): # == carry:
                # If yes, check if this Q-value is greater than the current max
    
                if q_value > max_q_value:
                    max_q_value = q_value
                    #print(max_q_value)
    
        return max_q_value if max_q_value != -float('inf') else 0  # Return the max Q-value found, or 0 if none
    
    def get_avg_q_value_for_position(self, agent_position, q_table, agent_index):
        total_q_value = 0  # To sum up all the Q-values
        count = 0  # To count the number of actions contributing to the average

        # Iterate over the Q-table entries
        for (state, action), q_value in q_table.items():
        
            # Check if the current state corresponds to the agent's position and carry status
            if state[agent_index * 2:agent_index * 2 + 2] == agent_position and state[6 + agent_index] in (0, 1):
                # If yes, add this Q-value to the total and increment the count
                total_q_value += q_value
                count += 1

        # Compute the average if count is not 0, otherwise return 0
        return total_q_value / count if count > 0 else 0

    def create_agent_heat_map(self, agent_index, q_table, title, agent_name):
        # Define the grid size
        grid_size = (5, 5)  # Example grid size

        # Initialize an array for the heatmap
        heatmap_data = np.zeros(grid_size)

        # Generate heatmap data
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                agent_position = (x, y)
                #q_value = self.get_max_q_value_for_position(agent_position, q_table, agent_index)
                q_value = self.get_max_q_value_for_position(agent_position, q_table, agent_index)
                heatmap_data[x, y] = q_value

        # Plot the heatmap
        #min_value = min(q_table.values())
        #max_value = max(q_table.values())
        mask = (heatmap_data != 0) & (heatmap_data != -np.inf)

        # Use the mask to filter the data and then find the minimum of the remaining values
        min_value = np.min(heatmap_data[mask])
        max_value = np.max(heatmap_data)
        self.plot_map(min_value, max_value, heatmap_data, agent_name + ' ' + title)

    def create_general_heat_map(self, q_table, title):
        # Define the grid size
        grid_size = (5, 5)  # Example grid size

        red_agent_index = 0
        blue_agent_index = 1
        black_agent_index = 2
        
        # Initialize an array for the heatmap
        heatmap_data_1 = np.zeros(grid_size)

        # Generate heatmap data
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                agent_position = (x, y)
                q_value = self.get_max_q_value_for_position(agent_position, q_table, red_agent_index)
                heatmap_data_1[x, y] = q_value
            
        # Initialize an array for the heatmap
        heatmap_data_2 = np.zeros(grid_size)

        # Generate heatmap data
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                agent_position = (x, y)
                q_value = self.get_max_q_value_for_position(agent_position, q_table, blue_agent_index)
                heatmap_data_2[x, y] = q_value
                
        # Initialize an array for the heatmap
        heatmap_data_3 = np.zeros(grid_size)

        # Generate heatmap data
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                agent_position = (x, y)
                q_value = self.get_max_q_value_for_position(agent_position, q_table, black_agent_index)
                heatmap_data_3[x, y] = q_value

        heatmap_data = np.zeros(grid_size)
        
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                heatmap_data[x, y] = (heatmap_data_1[x, y] + heatmap_data_2[x, y] + heatmap_data_3[x, y]) / 3
        
        # Plot the heatmap
        min_value = min(q_table.values())
        max_value = max(q_table.values())
             
        self.plot_map(min_value, max_value, heatmap_data, title)


    def run_heat_maps(self, q_table, title):
        
        #self.print_create_centric(q_table, self.red_agent_index)
        self.create_agent_heat_map(self.red_agent_index, q_table, title, 'red agent')
        
        #self.print_create_centric(q_table, self.blue_agent_index)
        self.create_agent_heat_map(self.blue_agent_index, q_table, title, 'blue agent')

        #self.print_create_centric(q_table, self.black_agent_index)
        self.create_agent_heat_map(self.black_agent_index, q_table, title, 'black agent')

        self.create_general_heat_map(q_table, title)
        
        
    def plot_map(self, min_value, max_value, heatmap_data, title):

        plt.imshow(heatmap_data, cmap='hot', interpolation='nearest', vmin=min_value, vmax=max_value)
        plt.colorbar()
        plt.title(title)
        plt.show()
    
    def print_create_centric(self, full_q_table, agent_index):
        centric_q = self.create_agent_centric_q_table(full_q_table, self.red_agent_index)
        print(centric_q)
        min_value = min(centric_q.values())
        print('centric min')
        print(min_value)
        max_value = max(centric_q.values())
        print('centric max')
        print(max_value)
        
    def create_agent_centric_q_table(self, full_q_table, agent_index):

        agent_q_table = {}
        # Iterate over the full Q-table
        for (state, action), q_value in full_q_table.items():
            # Extract only the part of the state that pertains to the agent of interest
            # Extract x, y position for the agent
            agent_position = state[agent_index * 2:agent_index * 2 + 2]  # (red_x, red_y)

            # Extract carrying bit for the agent
            agent_carry = (state[6 + agent_index],)  # (red_carry,)

            # Combine position and carrying bit to form the full agent state
            agent_state = agent_position + agent_carry

            agent_q_table[agent_state, action] = q_value

        # Optionally, you could average the Q-values over all possible other states.

        return agent_q_table

    def plot_paths(self, paths):
        #fig, ax = plt.subplots()
        #colors = {'RED': 'r', 'BLUE': 'b', 'BLACK': 'k'}    
#
        #for agent, path in paths.items():
        #    states = [s for s, a, ns, q in path]
        #    x, y = zip(*[(s[0], s[1]) for s in states])  # Assuming states are tuples (x, y)
        #    ax.plot(x, y, color=colors[agent.name], label=f"Agent {agent.name}")    
#
        #ax.legend()
        #plt.show()
        
        # Define a dictionary for colors for clarity in plotting.
        #agent_colors = {
        #    my_enums.Agent.RED: 'r',
        #    my_enums.Agent.BLUE: 'b',
        #    my_enums.Agent.BLACK: 'k'
        #}
        #
        ## Assuming a square grid
        #fig, ax = plt.subplots()
        #for agent, path in paths.items():
        #    for s, a, ns, q in path:
#
        #        # Draw the line with arrow
        #        plt.arrow(s[0], s[1], ns[0], ns[1], head_width=0.1, head_length=0.1, fc=agent_colors[agent], ec=agent_colors[agent])
        #
        ## Set the limits and the aspect
        #ax.set_xlim(-0.5, max(max(x[0] for x, a, s, q in path) for path in paths.values()) + 0.5)
        #ax.set_ylim(-0.5, max(max(x[1] for x, a, s, q in path) for path in paths.values()) + 0.5)
        #ax.set_aspect('equal')
        #
        ## Adding grid
        #plt.grid(True)
        #
        ## Show the plot
        #plt.show()
    

        # Define the colors for each agent
        agent_colors = {
            my_enums.Agent.RED: 'r',
            my_enums.Agent.BLUE: 'b',
            my_enums.Agent.BLACK: 'k'
        }
        
        # Number of agents to create subplots
        num_agents = len(paths)
        fig, axes = plt.subplots(1, num_agents, figsize=(5*num_agents, 5))  # Adjust the figure size as needed

        # If there's only one agent, wrap axes in a list for consistent indexing
        if num_agents == 1:
            axes = [axes]
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
                optimal_paths[agent].append((current_state, best_action, next_state, actions_and_q_values[1]))

                # Update the current state
                current_state = next_state
                
        # Loop over each agent and its dedicated subplot
        for ax, (agent, path) in zip(axes, optimal_paths.items()):
            for s, a, ns, q in path:
                # Calculate the difference (dx, dy) for the arrow
                dx = ns[0] - s[0]
                dy = ns[1] - s[1]

                # Draw the line with arrow
                ax.arrow(s[0], s[1], dx, dy, head_width=0.1, head_length=0.1, fc=agent_colors[agent], ec=agent_colors[agent])

            # Set the limits and the aspect ratio for each subplot
            #ax.set_xlim(-0.5, max(x[0] for x, a, ns, q in path) + 0.5)
            #ax.set_ylim(-0.5, max(x[1] for x, a, ns, q in path) + 0.5)
            ax.set_xlim(-1,5)
            ax.set_ylim(-1,5)
            ax.set_aspect('equal')
            ax.set_title(f"Agent {agent}")
            ax.grid(True)

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Show the plot
        plt.show()