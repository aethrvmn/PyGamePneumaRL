import random
import argparse
import torch as T
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

from game import Game


if __name__ == "__main__":

    # Create parser
    parser = argparse.ArgumentParser(
        prog='Pneuma',
        description='A Reinforcement Learning platform made with PyGame'
    )

    # Add args
    parser.add_argument('--no_seed',
                        default=False,
                        action="store_true",
                        help="Set to True to run without a seed.")

    parser.add_argument('--seed',
                        type=int,
                        default=1,
                        help="The seed for the RNG.")

    parser.add_argument('--n_episodes',
                        type=int,
                        default=300,
                        help="Number of episodes.")

    parser.add_argument('--ep_length',
                        type=int,
                        default=5000,
                        help="Length of each episode.")

    parser.add_argument('--n_players',
                        type=int,
                        default=1,
                        help="Number of players.")

    parser.add_argument('--chkpt_path',
                        type=str,
                        default="agents/saved_models",
                        help="Save/load location for agent models.")

    parser.add_argument('--figure_path',
                        type=str,
                        default="figures",
                        help="Save location for figures.")

    parser.add_argument('--horizon',
                        type=int,
                        default=2048,
                        help="The number of steps per update")

    parser.add_argument('--show_pg',
                        default=False,
                        action="store_true",
                        help="Set to True to open PyGame window on desktop")

    parser.add_argument('--no_load',
                        default=False,
                        action="store_true",
                        help="Set to True to ignore saved models")

    parser.add_argument('--gamma',
                        type=float,
                        default=0.99,
                        help="The gamma parameter for PPO")

    parser.add_argument('--entropy',
                        type=float,
                        default=0.01,
                        help="The entropy coefficient")

    parser.add_argument('--alpha',
                        type=float,
                        default=0.0003,
                        help="The alpha parameter for PPO")

    parser.add_argument('--policy_clip',
                        type=float,
                        default=0.2,
                        help="The policy clip")

    parser.add_argument('--batch_size',
                        type=int,
                        default=64,
                        help="The size of each batch")

    parser.add_argument('--n_epochs',
                        type=int,
                        default=10,
                        help="The number of epochs")

    parser.add_argument('--gae_lambda',
                        type=float,
                        default=0.95,
                        help="The lambda parameter of the GAE")

    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    T.manual_seed(args.seed)

    n_episodes = args.n_episodes
    episode_length = args.ep_length
    n_players = args.n_players

    chkpt_path = args.chkpt_path
    figure_folder = args.figure_path

    horizon = args.horizon
    learnings_per_episode = int(episode_length/horizon)
    learn_iters = 0

    show_pygame = args.show_pg

    # Setup AI stuff
    score_history = np.zeros(shape=(n_players, n_episodes))

    best_score = np.zeros(n_players)

    actor_loss = np.zeros(shape=(n_players,
                                 n_episodes))

    critic_loss = np.zeros(shape=(n_players,
                                  n_episodes))

    total_loss = np.zeros(shape=(n_players,
                                 n_episodes))

    game = Game(show_pg=show_pygame, n_players=n_players)

    print("Initializing agents ...")
    for player in tqdm(game.level.player_sprites,
                       dynamic_ncols=True):
        player.setup_agent(
            gamma=args.gamma,
            alpha=args.alpha,
            policy_clip=args.policy_clip,
            batch_size=args.batch_size,
            n_epochs=args.n_epochs,
            gae_lambda=args.gae_lambda,
            entropy_coef=args.entropy,
            chkpt_dir=chkpt_path,
            no_load=args.no_load
        )

    # Episodes start
    for episode in tqdm(range(n_episodes),
                        dynamic_ncols=True):

        game.level.reset()

        episode_reward = np.zeros(
            shape=(n_players, episode_length))

        episode_actor_loss = np.zeros(
            shape=(n_players, learnings_per_episode))

        episode_critic_loss = np.zeros(
            shape=(n_players, learnings_per_episode))

        episode_total_loss = np.zeros(
            shape=(n_players, learnings_per_episode))

        # Main game loop
        for step in tqdm(range(episode_length),
                         leave=False,
                         ascii=True,
                         dynamic_ncols=True):

            if not game.level.done:
                game.run()

                for player in game.level.player_sprites:

                    episode_reward[player.player_id][step] = player.reward

                    if (step % horizon == 0 and step != 0) or player.is_dead():

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

        plt.figure()
        plt.title("Agent Rewards")
        plt.xlabel("Episode")
        plt.ylabel("Score")
        plt.legend([f"Agent {num}" for num in range(n_players)])
        for player_score in score_history:
            plt.plot(player_score)
        plt.savefig(f"{figure_folder}/score.png")
        plt.close()

        plt.figure()
        plt.suptitle("Actor Loss")
        plt.xlabel("Episode")
        plt.ylabel("Loss")
        plt.legend([f"Agent {num}" for num in range(n_players)])
        for actor in actor_loss:
            plt.plot(actor)
        plt.savefig(f"{figure_folder}/actor_loss.png")
        plt.close()

        plt.figure()
        plt.suptitle("Critic Loss")
        plt.xlabel("Episode")
        plt.ylabel("Loss")
        plt.legend([f"Agent {num}" for num in range(n_players)])
        for critic in critic_loss:
            plt.plot(critic)
        plt.savefig(f"{figure_folder}/critic_loss.png")
        plt.close()

        plt.figure()
        plt.suptitle("Total Loss")
        plt.xlabel("Episode")
        plt.ylabel("Loss")
        plt.legend([f"Agent {num}" for num in range(n_players)])
        for total in total_loss:
            plt.plot(total)
        plt.savefig(f"{figure_folder}/total_loss.png")
        plt.close()

    # End of training session
    print("End of episodes.\
        \nExiting game...")

    game.quit()
