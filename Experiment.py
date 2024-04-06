import my_enums
from ActionSelector import ActionSelector
import numpy as np

class Experiment:
    def __init__(self,
                world,
                total_steps,
                initial_steps,
                second_phase_steps,
                num_episodes,
                initial_state,
                algorithm,
                second_phase_methods,
                runs):
        
        self.world = world
        self.total_steps = total_steps
        self.initial_steps = initial_steps
        self.second_phase_steps = second_phase_steps
        self.num_episodes = num_episodes
        self.initial_state = initial_state
        self.algorithm = algorithm
        self.action_selector = ActionSelector()
        self.second_phase_methods = second_phase_methods
        self.runs = runs
        

    def get_next_agent(self, agent):
        if(agent == my_enums.Agent.RED):
            return my_enums.Agent.BLUE
        elif(agent == my_enums.Agent.BLUE):
            return my_enums.Agent.BLACK
        else:
            return my_enums.Agent.RED

    #Todo
    # Running experiments with different configurations
    #Todo
    # Visualization and analysis of results

    def run_experiment(self):
        q_table = {}  # Use a dict for sparse storage

        #starting agent and initial state
        agent = my_enums.Agent.RED
        state = self.initial_state

        for run in range(self.runs):
            episode_counter = 0
                    
            for episode in range(self.num_episodes):
                
                
                second_phase_policy = self.second_phase_methods[episode_counter]

                num_actions = len(my_enums.Actions)

                done = False
                count = 0

                while not done:
                    if(self.world.dropoffs_are_full()):
                        self.world.reset_initial_values()
                        state = self.initial_state
                        
                    # Get available actions
                    applicable_actions = [a for a in my_enums.Actions if self.world.is_action_applicable(a, agent)]

                    #If terminal state reached
                    if(len(applicable_actions) == 0):
                        self.world.reset_initial_values()
                        break

                    action = self.action_selector.determine_action(episode, state, applicable_actions, q_table, self.initial_steps, second_phase_policy)

                    # Execute the action, get the new state and reward
                    reward, done, *next_state = self.world.performAction(action, agent)

                    next_state = tuple(next_state[0])

                    q_table[state, action] = self.algorithm.update_q(q_table, state, action, reward, next_state, num_actions, agent, self.world)

                    # Prepare for the next iteration
                    state = next_state
                    agent = self.get_next_agent(agent)

                    count += 1

                    #self.world.display()
                    if count >= self.total_steps:
                        done = True

                episode_counter += 1


                #filtered_dict = {k: v for k, v in q_table.items() if v not in (-np.inf,-0.3) }

                #print(q_table)
                #print(filtered_dict)
                print(count)

                if(count < 9000):
                    print(q_table)
                    self.world.display()
            
            