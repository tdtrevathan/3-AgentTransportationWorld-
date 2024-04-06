import my_enums
import numpy as np

class ActionSelector:
    

    def determine_action(self, episode, state, applicable_actions, q_table, initial_steps, second_policy):
                # Decide which policy to use
        if episode < initial_steps:
            policy = my_enums.Pstrategy.PRANDOM
        else:
            policy = second_policy

        # Select an action based on the current policy
        if policy == my_enums.Pstrategy.PRANDOM:
            action = self.select_prandom_action(applicable_actions)
        elif policy == my_enums.Pstrategy.PEXPLOIT:
            action = self.select_pexploit_action(state, applicable_actions, q_table)
        elif policy == my_enums.Pstrategy.PGREEDY:
            action = self.select_pgreedy_action(state, applicable_actions, q_table)

        return action
    
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