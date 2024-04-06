import numpy as np
import my_enums

class Experiment:
    def __init__(self,
                world,
                total_steps,
                initial_steps,
                second_phase_steps,
                num_episodes,
                initial_state,
                algorithm):
        
        self.world = world
        self.total_steps = total_steps
        self.initial_steps = initial_steps
        self.second_phase_steps = second_phase_steps
        self.num_episodes = num_episodes
        self.initial_state = initial_state
        self.algorithm = algorithm
        
        
    def select_prandom_action(self, applicable_actions):
        # Prioritize 'PICKUP' and 'DROPOFF' if applicable
        for action in [my_enums.Actions.PICKUP, my_enums.Actions.DROPOFF]:
            if action in applicable_actions:
                return action

        # If 'PICKUP' and 'DROPOFF' are not applicable, select randomly among the rest
        return np.random.choice(applicable_actions)

    def select_pgreedy_action(self, state, applicable_actions, q_table):
        # If 'pickup' or 'dropoff' is applicable, prioritize it
        for action in [my_enums.Actions.PICKUP, my_enums.Actions.DROPOFF]:
            if action in applicable_actions:
                return action

        # Filter Q-values for applicable actions only and find the max Q-value
        q_values = {action: q_table.get((state, action), 0) for action in applicable_actions}
        max_q = max(q_values.values())

        # Get actions with the max Q-value
        max_actions = [action for action, q in q_values.items() if q == max_q]

        # Randomly select among the actions with the highest Q-value
        return np.random.choice(max_actions)

    def select_pexploit_action(self, state, applicable_actions, q_table):
        # Check for priority actions first
        for action in [my_enums.Actions.PICKUP, my_enums.Actions.DROPOFF]:
            if action in applicable_actions:
                return action

        # Decide to exploit or explore based on probability
        if np.random.rand() < 0.8:  # 80% chance to exploit
            # Exploit: Choose the action with the highest Q-value
            q_values = {action: q_table.get((state, action), 0) for action in applicable_actions}
            max_q = max(q_values.values())
            max_actions = [action for action, q in q_values.items() if q == max_q]
            return np.random.choice(max_actions)
        else:
            # Explore: Choose a random action
            return np.random.choice(applicable_actions)
        


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


        #episodes refer to runs essentially.
        #the run could end due to all blocks being returned for example
        #but this doesnt mean that the experiment is over
        num_episodes =  1

        for episode in range(num_episodes):


            num_actions = len(my_enums.Actions)

            done = False
            count = 0
            
            while not done:
                # Get available actions
                applicable_actions = [a for a in my_enums.Actions if self.world.is_action_applicable(a, agent)]
                
                #If terminal state reached
                if(len(applicable_actions) == 0):
                    self.world.reset_initial_values()
                    break

                # Decide which policy to use
                if episode < self.initial_steps:
                    policy = my_enums.Pstrategy.PRANDOM
                else:
                    scenario = 'c'  # Change as needed for each experiment run

                    if scenario == 'a':
                        policy = my_enums.Pstrategy.PRANDOM
                    elif scenario == 'b':
                        policy = my_enums.Pstrategy.PGREEDY
                    elif scenario == 'c':
                        policy = my_enums.Pstrategy.PEXPLOIT
                
                # Select an action based on the current policy
                if policy == my_enums.Pstrategy.PRANDOM:
                    action = self.select_prandom_action(applicable_actions)
                elif policy == my_enums.Pstrategy.PEXPLOIT:
                    action = self.select_pexploit_action(state, applicable_actions, q_table)
                elif policy == my_enums.Pstrategy.PGREEDY:
                    action = self.select_pgreedy_action(state, applicable_actions, q_table)

                # Update Q-value using SARSA update equation
                # sarsa_update(q_table, state, action, reward, next_state, next_action, alpha, gamma) # need to implement next_action


                # Execute the action, get the new state and reward
                reward, done, *next_state = self.world.performAction(action, agent)

                next_state = tuple(next_state[0])

                q_table[state, action] = self.algorithm.update_q(q_table, state, action, reward, next_state, num_actions, agent, self.world)
                
                # Prepare for the next iteration
                state = next_state
                agent = self.get_next_agent(agent)
                
                if(self.world.dropoffs_are_full()):
                    self.world.reset_initial_values()
                    
                count += 1

                #self.world.display()
                if count >= self.total_steps:
                    done = True

        #filtered_dict = {k: v for k, v in q_table.items() if v not in (-np.inf,-0.3) }

        #print(q_table)
        #print(filtered_dict)
        print(count)
        
        if(count < 9000):
            print(q_table)
            self.world.display()