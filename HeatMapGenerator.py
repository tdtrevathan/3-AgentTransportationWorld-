import matplotlib.pyplot as plt
import numpy as np
import os

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
    
        return max_q_value if max_q_value != -float('inf') else 0  # Return the max Q-value found, or 0 if none
    
    
    def create_agent_heat_map(self, agent_index, q_table, title, agent_name):
        # Define the grid size
        grid_size = (5, 5)  # Example grid size

        # Initialize an array for the heatmap
        heatmap_data = np.zeros(grid_size)

        # Generate heatmap data
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                agent_position = (x, y)
                q_value = self.get_max_q_value_for_position(agent_position, q_table, agent_index)
                heatmap_data[x, y] = q_value

        # Plot the heatmap
        min_value = min(q_table.values())
        max_value = max(q_table.values())
        
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
