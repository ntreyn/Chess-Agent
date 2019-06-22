import numpy as np 
import random

class learner:
    def __init__(self, e):
        self.env = e
    
    def learn(self):
        state_size = self.env.state_size
        action_size = self.env.action_size

        self.qtable = np.zeros((state_size, action_size))

        total_episodes = 1
        max_steps = 100
        learning_rate = 0.7
        gamma = 0.9

        epsilon = 1.0
        max_epsilon = 1.0
        min_epsilon = 0.3
        decay_rate = 0.0001

        for episode in range(total_episodes):

            print(episode, end='\r')

            state = self.env.reset()
            step = 0
            done = False
            reward = 0

            for step in range(max_steps):

                exp_exp_tradeoff = random.uniform(0,1)

                if exp_exp_tradeoff > epsilon:
                    potential_actions = self.env.get_actions()
                    action_values = [-1] * action_size

                    for a in potential_actions:
                        action_values[a] = self.qtable[state, a]

                    action = np.argmax(action_values)
                else:
                    action = self.env.sample_action()
                
                move = self.env.convert_action(action)
                new_state, reward, done, next_moves, status = self.env.step(move)

                potential_actions = self.env.get_actions()
                action_values = [-1] * action_size

                for a in potential_actions:
                    action_values[a] = self.qtable[state, a]

                self.qtable[state, action] = self.qtable[state, action] + learning_rate * (reward + gamma * np.max(action_values) - self.qtable[state, action])

                state = new_state

                if done:
                    print(reward)
                    break

            epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

        self.env.reset()