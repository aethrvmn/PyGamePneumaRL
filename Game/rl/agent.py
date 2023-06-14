import random

from rl.brain import PPONet


class Agent:
    
    def __init__(self, actions, inputs, player_info, reward):
        
        self.input_dim = len(inputs) + len(player_info)

        self.output_dim = len(actions)
        
        self.reward = reward
        
        self.net = PPONet(input_dim, output_dim)
