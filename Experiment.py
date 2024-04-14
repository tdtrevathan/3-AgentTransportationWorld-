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
        
        paths = {agent: [] for agent in my_enums.Agent}
        
        #starting agent and initial state
        agent = my_enums.Agent.RED
        state = self.initial_state
        
        run_counter = 0
        
        completion_steps_per_episode = []
        
        for run in range(self.runs):
            completion_steps_per_episode.append([])
        
        for run in range(self.runs):
                        
            episode_counter = 0

            completions = 0    
            second_phase_policy = self.second_phase_methods[episode_counter]

            num_actions = len(my_enums.Actions)
            done = False
            
            steps = 0
            episode_initial_step = 0
            terminal_counter = 0
            
            reset = True

            while not done:
                if(reset):
                    applicable_actions = [a for a in my_enums.Actions if self.world.is_action_applicable(a, agent)]
                    action = self.action_selector.determine_action(steps, 
                                                                   state,
                                                                   applicable_actions,
                                                                   q_table,
                                                                   self.initial_steps,
                                                                   second_phase_policy)
                    reset = False
              
                # Get available actions
                #applicable_actions = [a for a in my_enums.Actions if self.world.is_action_applicable(a, agent)]
                
                #action = self.action_selector.determine_action(steps, state, applicable_actions, q_table, self.initial_steps, second_phase_policy)
                # Execute the action, get the new state and reward

                reward, done, *next_state = self.world.performAction(action, agent)

                steps += 1
                
                next_state = tuple(next_state[0])

                next_agent = self.get_next_agent(agent)
                
                applicable_actions = [a for a in my_enums.Actions if self.world.is_action_applicable(a, next_agent)]
                
                #If terminal state reached
                if((len(applicable_actions) == 0) or self.world.dropoffs_are_full()):
                    
                    reset = True
                    
                    if(self.world.dropoffs_are_full()):
                        completions += 1

                        episode_total_steps = steps - episode_initial_step
                        completion_steps_per_episode[run_counter].append(episode_total_steps)
                                            
                        #print(f'Completion: {completions}')
                        #print(f'Step: {steps}')
                        #print(f'episode initial: {episode_initial_step}')
                        #print(f'episode total steps: {episode_total_steps}')
                        
                        episode_initial_step = steps
                        
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
                
                
                
                next_action = self.action_selector.determine_action(steps, next_state, applicable_actions, q_table, self.initial_steps, second_phase_policy)
              
                #Determine next action on new itteration
                q_value = self.algorithm.update_q(q_table, state, action, reward, next_state, next_action, next_agent, self.world)
                
                q_table[state, action] = q_value
                
                paths[agent].append(self.GetAgentPathState(agent, state, action, next_state, q_value))
                
                # Prepare for the next iteration
                state = next_state
                action = next_action
                agent = next_agent

                if steps >= self.total_steps:
                    if(not self.track_terminals):
                        print('done')
                        done = True

                episode_counter += 1

            if(steps < self.total_steps and not self.track_terminals):
                #print(q_table)
                self.world.display()
            
            run_counter += 1
            
        self.world.display()    
        return q_table, paths, completion_steps_per_episode
    
    
    def run_experiment_q_per_agent(self):
        
        self.world.set_agent_specific(True)
        
        q_tables = []
        q_table_red = {}
        q_table_blue = {}
        q_table_black = {}
        q_tables.append(q_table_red)
        q_tables.append(q_table_blue)
        q_tables.append(q_table_black)
        
        agent_indicies = {
            my_enums.Agent.RED: 0,
            my_enums.Agent.BLUE: 1,
            my_enums.Agent.BLACK: 2
        }
        
        paths = {agent: [] for agent in my_enums.Agent}
        
        #starting agent and initial state
        agent = my_enums.Agent.RED
        q_table = q_tables[agent_indicies[agent]]
        state = (self.initial_state[0], self.initial_state[1], self.initial_state[6], self.initial_state[9], self.initial_state[10], self.initial_state[11], self.initial_state[12], self.initial_state[13], self.initial_state[14])
        
        run_counter = 0
        
        completion_steps_per_episode = []
        
        for run in range(self.runs):
            completion_steps_per_episode.append([])
        
        for run in range(self.runs):
                        
            episode_counter = 0

            completions = 0    
            second_phase_policy = self.second_phase_methods[episode_counter]

            done = False
            
            steps = 0
            episode_initial_step = 0
            terminal_counter = 0
            
            reset = True

            while not done:
                if(reset):
                    applicable_actions = [a for a in my_enums.Actions if self.world.is_action_applicable(a, agent)]
                    action = self.action_selector.determine_action(steps, 
                                                                   state,
                                                                   applicable_actions,
                                                                   q_table,
                                                                   self.initial_steps,
                                                                   second_phase_policy)
                    reset = False
              
                reward, done, *next_state = self.world.performAction(action, agent)
                
                steps += 1
                
                next_state = tuple(next_state[0])

                next_agent = self.get_next_agent(agent)
                q_table = q_tables[agent_indicies[next_agent]]
                
                applicable_actions = [a for a in my_enums.Actions if self.world.is_action_applicable(a, next_agent)]
                
                #If terminal state reached
                if((len(applicable_actions) == 0) or self.world.dropoffs_are_full()):
                    
                    reset = True
                    
                    if(self.world.dropoffs_are_full()):
                        completions += 1

                        episode_total_steps = steps - episode_initial_step
                        completion_steps_per_episode[run_counter].append(episode_total_steps)
                                            
                        episode_initial_step = steps
                        
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
                
                
                next_action = self.action_selector.determine_action(steps, next_state, applicable_actions, q_table, self.initial_steps, second_phase_policy)
              
                #Determine next action on new itteration
                q_value = self.algorithm.update_q(q_table, state, action, reward, next_state, next_action, next_agent, self.world)
                
                q_table[state, action] = q_value
                
                paths[agent].append((state, action, next_state, q_value))
                
                # Prepare for the next iteration
                action = next_action
                agent = next_agent
                state = self.world.get_updated_state(agent)

                if steps >= self.total_steps:
                    if(not self.track_terminals):
                        print('done')
                        done = True

                episode_counter += 1

            if(steps < self.total_steps and not self.track_terminals):
                #print(q_table)
                self.world.display()
            
            run_counter += 1
            
        self.world.display()    
        return q_tables, paths, completion_steps_per_episode
    
    
    
    def GetAgentPathState(self, agent, state, action, next_state, q_value):
        
        if(agent == my_enums.Agent.RED):
            agent_index = 0
        elif(agent == my_enums.Agent.BLUE):
            agent_index = 1
        else:
            agent_index = 2
            
        agent_current_position = state[agent_index * 2:agent_index * 2 + 2]
        agent_current_carry = state[6 + agent_index]
        
        agent_state = (agent_current_position[0], agent_current_position[1], agent_current_carry)
        
        agent_next_position = next_state[agent_index * 2:agent_index * 2 + 2]
        agent_next_carry = next_state[6 + agent_index]
        
        agent_next_state = (agent_next_position[0], agent_next_position[1], agent_next_carry)
        
        return (agent_state, action, agent_next_state, q_value)
        