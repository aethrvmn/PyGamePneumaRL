import numpy as np
import torch as T

from .brain import ActorNetwork, CriticNetwork, PPOMemory


class Agent:

    def __init__(self, input_dims, n_actions, gamma=0.99, alpha=0.0003,
                 policy_clip=0.2, batch_size=64, N=2048, n_epochs=10,
                 gae_lambda=0.95, entropy_coef=0.001, chkpt_dir='tmp/ppo'):

        self.gamma = gamma
        self.policy_clip = policy_clip
        self.n_epochs = n_epochs
        self.gae_lambda = gae_lambda
        self.entropy_coef = entropy_coef

        self.actor = ActorNetwork(
            input_dims, n_actions, alpha, chkpt_dir=chkpt_dir)

        self.critic = CriticNetwork(
            input_dims, alpha, chkpt_dir=chkpt_dir)

        self.memory = PPOMemory(batch_size)

    def remember(self, state, action, probs, vals, reward, done):
        self.memory.store_memory(state, action, probs, vals, reward, done)

    def save_models(self, actr_chkpt='actor_ppo', crtc_chkpt='critic_ppo'):
        self.actor.save_checkpoint(actr_chkpt)
        self.critic.save_checkpoint(crtc_chkpt)

    def load_models(self, actr_chkpt='actor_ppo', crtc_chkpt='critic_ppo'):
        self.actor.load_checkpoint(actr_chkpt)
        self.critic.load_checkpoint(crtc_chkpt)

    def choose_action(self, observation):
        state = T.tensor(observation, dtype=T.float).to(self.actor.device)
        dist = self.actor(state)
        value = self.critic(state)
        action = dist.sample()

        probs = T.squeeze(dist.log_prob(action)).item()
        action = T.squeeze(action).item()
        value = T.squeeze(value).item()

        self.entropy = dist.entropy().mean().item()

        return action, probs, value

    def learn(self):
        for _ in range(self.n_epochs):
            state_arr, action_arr, old_probs_arr, vals_arr, reward_arr, dones_arr, batches = self.memory.generate_batches()

            values = vals_arr
            advantage = np.zeros(len(reward_arr), dtype=np.float64)

            for t in range(len(reward_arr)-1):
                discount = 1
                a_t = 0
                for k in range(t, len(reward_arr)-1):
                    a_t += discount * \
                        (reward_arr[k] + self.gamma*values[k+1]
                         * (1-int(dones_arr[k])) - values[k])
                    discount *= self.gamma * self.gae_lambda
                advantage[t] = a_t
            advantage = T.tensor(advantage).to(self.actor.device)

            values = T.tensor(values).to(self.actor.device)

            for batch in batches:
                states = T.tensor(state_arr[batch], dtype=T.float).to(
                    self.actor.device)
                old_probs = T.tensor(old_probs_arr[batch]).to(
                    self.actor.device)
                actions = T.tensor(action_arr[batch]).to(self.actor.device)

                dist = self.actor(states)
                critic_value = self.critic(states)

                critic_value = T.squeeze(critic_value)

                new_probs = dist.log_prob(actions)
                prob_ratio = new_probs.exp() / old_probs.exp()
                weighted_probs = advantage[batch] * prob_ratio

                weighted_clipped_probs = T.clamp(
                    prob_ratio, 1-self.policy_clip, 1+self.policy_clip)*advantage[batch]

                self.actor_loss = -T.min(weighted_probs,
                                         weighted_clipped_probs).mean()

                returns = advantage[batch] + values[batch]
                self.critic_loss = (returns - critic_value)**2
                self.critic_loss = self.critic_loss.mean()

                self.total_loss = self.actor_loss + 0.5 * \
                    self.critic_loss - self.entropy_coef*self.entropy

                self.actor.optimizer.zero_grad()
                self.critic.optimizer.zero_grad()
                self.total_loss.backward()

                # Calculate the gradient norms for both networks
                actor_grad_norm = T.nn.utils.clip_grad_norm_(
                    self.actor.parameters(), max_norm=1)
                critic_grad_norm = T.nn.utils.clip_grad_norm_(
                    self.critic.parameters(), max_norm=1)

                T.nn.utils.clip_grad_norm_(
                    self.actor.parameters(), max_norm=1)
                T.nn.utils.clip_grad_norm_(
                    self.critic.parameters(), max_norm=1)
                # Log or print the gradient norms
                print(f"Actor Gradient Norm: {actor_grad_norm}")
                print(f"Critic Gradient Norm: {critic_grad_norm}")

                self.actor.optimizer.step()
                self.critic.optimizer.step()

        self.memory.clear_memory()
