import os
import numpy as np
import torch as T
import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical

class PPOMemory:
    def __init__(self, batch_size):
        self.states = []
        self.probs = []
        self.vals = []
        self.actions = []
        self.rewards = []
        self.dones = []
        
        self.batch_size = batch_size
    
    def generate_batches(self):

        n_states = len(self.states)
        batch_start = np.arange(0, n_states, self.batch_size)
        indices = np.arange(n_states, dtype = np.int64)
        np.random.shuffle(indices)
        batches = [indices[i:i+self.batch_size] for i in batch_start]
        
        return  np.array(self.states),\
                np.array(self.actions),\
                np.array(self.probs),\
                np.array(self.vals),\
                np.array(self.rewards),\
                np.array(self.dones),\
                batches

    def store_memory(self, state, action, probs, vals, reward, done):
        self.states.append(state)
        self.probs.append(probs)
        self.vals.append(vals)
        self.rewards.append(reward)
        self.dones.append(done)
        
    def clear_memory(self):
        self.states = []
        self.probs = []
        self.vals = []
        self.actions = []
        self.rewards = []
        self.dones = []

class ActorNetwork(nn.Module):

    def __init__(self, input_dim, output_dim, alpha, fc1_dims = 256, fc2_dims = 256, chkpt_dir = 'tmp/ppo'):
        super(ActorNetwork, self).__init__()
        
        self.checkpoint_file = os.path.join(chkpt_dir, 'actor_torch_ppo')
        self.actor = nn.Sequential(
                        nn.Linear(len(input_dim), fc1_dims),
                        nn.ReLU(),
                        nn.Linear(fc1_dims, fc2_dims),
                        nn.ReLU(),
                        nn.Linear(fc2_dims, len(output_dim)),
                        nn.Softmax(dim=-1)
                        )
        
        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        
        self.device = T.device('cuda:0' if T.cuda.is_available() else ('mps' if T.backends.mps.is_available() else 'cpu'))
 
        self.to(self.device)

    def forward(self, state):
        dist = self.actor(state)
        dist = Categorical(dist)
        
        return dist

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)
        
    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))

class CriticNetwork(nn.Module):

    def __init__(self, input_dims, alpha, fc1_dims = 256, fc2_dims = 256, chkpt_dir = 'tmp/ppo'):
        super(CriticNetwork, self).__init__()
        
        self.checkpoint_file = os.path.join(chkpt_dir, 'critic_torch_ppo')
        self.critic = nn.Sequential(
                        nn.Linear(len(input_dims), fc1_dims),
                        nn.ReLU(),
                        nn.Linear(fc1_dims, fc2_dims),
                        nn.ReLU(),
                        nn.Linear(fc2_dims, 1)
                        )
        
        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else ('mps' if T.backends.mps.is_available() else 'cpu'))
        
        self.to(self.device)
        
    def forward(self, state):
        vale = self.critic(state)
        
        return value
        
    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)
        
    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
