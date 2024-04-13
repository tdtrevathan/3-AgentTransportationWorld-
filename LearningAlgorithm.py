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
        
        
        return self.apply_algorithm(q_table, state, action, reward, next_state, actions, agent, world)



    def apply_algorithm(self, q_table, state, action, reward, next_state, actions, agent, world):
        
        #if(self.algorithm == my_enums.Algorithm.QLEARNING):
        #    return self.q_formula(q_table, state, action, reward, next_state, actions, agent, world)
        #else:
            return self.sarsa_formula(q_table, state, action, reward, next_state)


    def q_formula(self, q_table, state, action, reward, next_state, actions, agent, world):
        
        # Get the Q-values for the next state, filter for applicable actions only
        next_q_value = np.array([q_table.get((next_state, a), 0) if world.is_action_applicable(a, agent) else -np.inf for a in my_enums.Actions])
        # Compute the maximum Q-value for the next state from applicable actions
        max_next_q = np.max(next_q_value)
                
        result = (1 - self.alpha) * q_table.get((state, action), 0) + self.alpha * (reward + self.gamma * max_next_q)
            
        return result
    
    def sarsa_formula(self, q_table, state, action, reward, next_state):

        next_q = q_table.get((next_state, action), 0)
        current_q = q_table.get((state, action), 0)
        
        result = current_q + self.alpha * (reward + self.gamma * next_q - current_q)
        
        if(result == -np.inf):
            print('bad one')
            print(state)
            print(next_state)
            
        return result