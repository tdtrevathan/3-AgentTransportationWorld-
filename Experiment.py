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
                runs,
                track_terminals=False,
                new_pickups=None):
        
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
        self.track_terminals = track_terminals
        self.new_pickups = new_pickups
        

    def get_next_agent(self, agent):
        if(agent == my_enums.Agent.RED):
            return my_enums.Agent.BLUE
        elif(agent == my_enums.Agent.BLUE):
            return my_enums.Agent.BLACK
        else:
            return my_enums.Agent.RED


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
                
                completions = 0    
                second_phase_policy = self.second_phase_methods[episode_counter]

                num_actions = len(my_enums.Actions)

                done = False
                steps = 0

                terminal_counter = 0
                
                while not done:
                    
                    # Get available actions
                    applicable_actions = [a for a in my_enums.Actions if self.world.is_action_applicable(a, agent)]

                    #If terminal state reached
                    if((len(applicable_actions) == 0) or self.world.dropoffs_are_full()):
                        
                        if(self.world.dropoffs_are_full()):
                            completions += 1
                            
                        self.world.reset_initial_values()
                        state = self.initial_state
                        
                        if(self.track_terminals):
                            if(steps > self.initial_steps):
                                terminal_counter += 1
                            if(terminal_counter == 3):
                                self.world.shift_pickups(self.new_pickups)
                            if(terminal_counter == 6):
                                print('done')
                                done = True
                                break
                
                        continue


                    action = self.action_selector.determine_action(steps, state, applicable_actions, q_table, self.initial_steps, second_phase_policy)

                    # Execute the action, get the new state and reward
                    reward, done, *next_state = self.world.performAction(action, agent)

                    next_state = tuple(next_state[0])

                    q_table[state, action] = self.algorithm.update_q(q_table, state, action, reward, next_state, num_actions, agent, self.world)
                    
                    if(agent == my_enums.Agent.BLACK and action == my_enums.Actions.PICKUP or action == my_enums.Actions.DROPOFF):
                        print('action')
                        print(action)
                        print('reward')
                        print(reward)
                    #if(action == my_enums.Actions.PICKUP or action == my_enums.Actions.DROPOFF):
                    #    print(agent)
                    #    print(action)
                    #    self.world.display()
                    #    print()
                    
                    # Prepare for the next iteration
                    state = next_state
                    agent = self.get_next_agent(agent)

                    steps += 1


                    if steps >= self.total_steps:
                        if(not self.track_terminals):
                            print('done')
                            done = True

                episode_counter += 1

                if(steps < self.total_steps and not self.track_terminals):
                    #print(q_table)
                    self.world.display()
            
                print('completions')
                print(completions)
            
        self.world.display()    
        return q_table        