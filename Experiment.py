import numpy as np
import my_enums

class Experiment:
    def __init__(self,
                world,
                total_steps,
                alpha,
                gamma,
                initial_steps,
                second_phase_steps,
                num_episodes,
                initial_state):
        
        self.world = world
        self.total_steps = total_steps
        self.alpha = alpha
        self.gamma = gamma
        self.initial_steps = initial_steps
        self.second_phase_steps = second_phase_steps
        self.num_episodes = num_episodes
        self.initial_state = initial_state
        
        
    def update_q_value(self,
                       q_table, 
                       state,
                       action,
                       reward,
                       next_state,
                       alpha,
                       gamma,
                       actions,
                       agent,
                       world):

        # Get the Q-values for the next state, filter for applicable actions only
        next_q_values = np.array([q_table.get((next_state, a), 0) if world.is_action_applicable(a, agent) else -np.inf for a in range(actions)])

        # Compute the maximum Q-value for the next state from applicable actions
        max_next_q = np.max(next_q_values)

        # Q-learning formula
        q_table[state, action] = (1 - alpha) * q_table.get((state, action), 0) + alpha * (reward + gamma * max_next_q)

    def sarsa_update(self, state, action, reward, next_state, next_action, q_table, alpha, gamma):
        # Implement SARSA update
        current_q = q_table.get((state, action), 0)
        next_q = q_table.get((next_state, next_action), 0)
        updated_q = current_q + alpha * (reward + gamma * next_q - current_q)
        q_table[state, action] = updated_q

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

                # Decide which policy to use
                if episode < self.initial_steps:
                    policy = "PRANDOM"
                else:
                    scenario = 'c'  # Change as needed for each experiment run

                    if scenario == 'a':
                        policy = "PRANDOM"
                    elif scenario == 'b':
                        policy = "PGREEDY"
                    elif scenario == 'c':
                        policy = "PEXPLOIT"

                # Select an action based on the current policy
                if policy == "PRANDOM":
                    action = self.select_prandom_action(applicable_actions)
                elif policy == "PEXPLOIT":
                    action = self.select_pexploit_action(state, applicable_actions, q_table)
                elif policy == "PGREEDY":
                    action = self.select_pgreedy_action(state, applicable_actions, q_table)

                # Update Q-value using SARSA update equation
                # sarsa_update(q_table, state, action, reward, next_state, next_action, alpha, gamma) # need to implement next_action

                print('action')
                print(action)
                # Execute the action, get the new state and reward
                reward, done, *next_state = self.world.performAction(action, agent)

                next_state = tuple(next_state[0])

                # Step 3: Update the Q-table  actions, pickups, dropoffs
                self.update_q_value(q_table, state, action, reward, next_state, self.alpha, self.gamma, num_actions, agent, self.world)

                # Prepare for the next iteration
                state = next_state

                count += 1
                agent = self.get_next_agent(agent)
                print("count: {}".format(count))
                print()
                self.world.display()
                if count >= 20:
                    done = True

        print(q_table)