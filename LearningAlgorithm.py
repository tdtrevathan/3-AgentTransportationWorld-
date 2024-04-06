import my_enums
import numpy as np

class LearningAlgorithm:
    def __init__(self, algorithm, alpha, gamma):
        self.algorithm = algorithm
        self.alpha = alpha
        self.gamma = gamma
        
    def update_q(self,
                q_table, 
                state,
                action,
                reward,
                next_state,
                actions,
                agent,
                world):
        
        # Get the Q-values for the next state, filter for applicable actions only
        next_q_value = np.array([q_table.get((next_state, a), 0) if world.is_action_applicable(a, agent) else -np.inf for a in range(actions)])
        
        return self.apply_algorithm(q_table, state, action, reward, next_q_value)



    def apply_algorithm(self, q_table, state, action, reward, next_q_value):
        
        if(self.algorithm == my_enums.Algorithm.QLEARNING):

            return self.q_formula(q_table, state, action, reward, next_q_value)
        else:
            return self.sarsa_formula(q_table, state, action, reward, next_q_value)




    def q_formula(self, q_table, state, action, reward, next_q_value):
        # Compute the maximum Q-value for the next state from applicable actions
        max_next_q = np.max(next_q_value)
        
        return (1 - self.alpha) * q_table.get((state, action), 0) + self.alpha * (reward + self.gamma * max_next_q)
    
    def sarsa_formula(self, q_table, state, action, reward, next_q):
        
        current_q = q_table.get((state, action), 0)
        return current_q + self.alpha * (reward + self.gamma * next_q - current_q)