import os
import random
import torch as T
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

import args
import folder_struct

import utils.seeds as seeds
import utils.metrics as metrics

from game import Pneuma

def main():

    parsed_args = args.parse_args()

    if not parsed_args.no_seed:
        seeds.set_seeds(parsed_args.seed)
        print(f"Seed set as {parsed_args.seed}")
    else:
        print("No seed set")

    chkpt_path, figure_path = folder_struct.setup_dirs()
        
    n_episodes = parsed_args.n_episodes
    episode_length = parsed_args.ep_length
    n_agents = parsed_args.n_agents

    horizon = parsed_args.horizon
    no_training = parsed_args.no_training
    
    learnings_per_episode = int(episode_length/horizon)
    learn_iters = 0

    show_pygame = parsed_args.show_pg

    # Setup AI metrics

    # Setup parameter monitoring
    score_history = np.zeros(
        shape=(parsed_args.n_agents, parsed_args.n_episodes))

    best_score = np.zeros(parsed_args.n_agents)

    actor_loss = np.zeros(shape=(parsed_args.n_agents,
                                 parsed_args.n_episodes))

    critic_loss = np.zeros(shape=(parsed_args.n_agents,
                                  parsed_args.n_episodes))

    total_loss = np.zeros(shape=(parsed_args.n_agents,
                                 parsed_args.n_episodes))

    entropy = np.zeros(shape=(parsed_args.n_agents,
                              parsed_args.n_episodes))

    advantage = np.zeros(shape=(parsed_args.n_agents,
                                parsed_args.n_episodes))

    time_alive = np.zeros(shape=(parsed_args.n_agents,
                                 parsed_args.n_episodes))
    # score_history, best_score, actor_loss, critic_loss, total_loss, entropy, advantage  = metrics.generate(parsed_args)
    
    
    game = Pneuma(show_pg=show_pygame, n_players=parsed_args.n_agents)

    print("Initializing agents ...")
    for player in tqdm(game.level.player_sprites,
                       dynamic_ncols=True):
        player.setup_agent(
            gamma=parsed_args.gamma,
            alpha=parsed_args.alpha,
            policy_clip=parsed_args.policy_clip,
            batch_size=parsed_args.batch_size,
            n_epochs=parsed_args.n_epochs,
            gae_lambda=parsed_args.gae_lambda,
            entropy_coef=parsed_args.entropy_coeff,
            chkpt_dir=chkpt_path,
            load=parsed_args.load
        )

    # Episodes start
    for episode in tqdm(range(n_episodes),
                        dynamic_ncols=True):

        game.level.reset()

        episode_reward = np.zeros(
            shape=(n_agents, episode_length))

        episode_actor_loss = np.zeros(
            shape=(n_agents, learnings_per_episode))

        episode_critic_loss = np.zeros(
            shape=(n_agents, learnings_per_episode))

        episode_total_loss = np.zeros(
            shape=(n_agents, learnings_per_episode))

        # Main game loop
        for step in tqdm(range(episode_length),
                         leave=False,
                         ascii=True,
                         dynamic_ncols=True):

            if not game.level.done:
                game.run()

                for player in game.level.player_sprites:

                    episode_reward[player.player_id][step] = player.reward

                    if not no_training and ((step % horizon == 0 and step != 0) or player.is_dead()):

                        player.agent.learn()

                        episode_actor_loss[player.player_id][learn_iters % learnings_per_episode]\
                            = player.agent.actor_loss

                        episode_critic_loss[player.player_id][learn_iters % learnings_per_episode]\
                            = player.agent.critic_loss

                        episode_total_loss[player.player_id][learn_iters % learnings_per_episode]\
                            = player.agent.total_loss

                        learn_iters += 1



        # Gather information about the episode
        for player in game.level.player_sprites:

            score = np.mean(episode_reward[player.player_id])

            # Update score
            score_history[player.player_id][episode] = score

            # Update actor/critic loss
            actor_loss[player.player_id][episode] = np.mean(
                episode_actor_loss)

            critic_loss[player.player_id][episode] = np.mean(
                episode_critic_loss)

            total_loss[player.player_id][episode] = np.mean(
                episode_total_loss)

            time_alive[player.player_id][episode] = step

            # Check for new best score
            if score > best_score[player.player_id]:
                print(f"\nEpisode:\
                          {episode}\
                        \nNew best score for player {player.player_id}:\
                          {score}\
                        \nOld best score for player {player.player_id}: \
                            {best_score[player.player_id]}")

                best_score[player.player_id] = score

                print(f"Saving models for player {player.player_id}...")

                # Save models
                player.agent.save_models(
                    f"A{player.player_id}",
                    f"C{player.player_id}")

                print(f"Models saved to {chkpt_path}")

        metrics.plot_learning_curve(score_history, parsed_args.n_agents, figure_path)

        metrics.plot_score(score_history, parsed_args.n_agents, figure_path)

        metrics.plot_loss('actor', actor_loss, parsed_args.n_agents, figure_path)

        metrics.plot_loss('critic', critic_loss, parsed_args.n_agents, figure_path)

        metrics.plot_parameter('entropy', entropy, parsed_args.n_agents, figure_path)

        metrics.plot_parameter('advantage', advantage, parsed_args.n_agents, figure_path)

        metrics.plot_avg_time(time_alive, parsed_args.n_agents, figure_path)    
    # End of training session
    print("End of episodes.\
        \nExiting game...")

    # Save models
    player.agent.save_models(
        f"A{player.player_id}_end",
        f"C{player.player_id}_end")

    print(f"Models saved to {chkpt_path}")

    game.quit()

if __name__ == '__main__':
    main()
