import os
import numpy as np
import matplotlib.pyplot as plt


def generate(parsed_args):

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

    return score_history, best_score, actor_loss,
    critic_loss, total_loss, entropy,
    advantage


def plot_learning_curve(scores, num_players, figure_path):

    plt.figure()
    plt.title("Running Average - Score")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.legend([f"Agent {num}" for num in range(num_players)])
    for score in scores:
        running_avg = np.zeros(len(score))
        for i in range(len(score)):
            running_avg[i] = np.mean(score[max(0, i-100):(i+1)])
        plt.plot(running_avg)
    plt.savefig(os.path.join(figure_path, "avg_score.png"))
    plt.close()


def plot_score(scores, num_players, figure_path):

    plt.figure()
    plt.title("Agent Rewards - No Averaging")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.legend([f"Agent {num}" for num in range(num_players)])
    for player_score in scores:
        plt.plot(player_score)
    plt.savefig(os.path.join(figure_path, 'score.png'))
    plt.close()


def plot_loss(nn_type, losses, num_players, figure_path):

    plt.figure()
    plt.title(f"Running Average - {nn_type.capitalize()} Loss")
    plt.xlabel("Learning Iterations")
    plt.ylabel("Loss")
    plt.legend([f"Agent {num}" for num in range(num_players)])
    for loss in losses:
        running_avg = np.zeros(len(loss))
        for i in range(len(loss)):
            running_avg[i] = np.mean(loss[max(0, i-100):(i+1)])
        plt.plot(running_avg)
    plt.savefig(os.path.join(figure_path, f"{nn_type}_loss.png"))
    plt.close()


def plot_parameter(name, parameter, num_players, figure_path):

    plt.figure()
    plt.title(f"Running Average - {name.capitalize()}")
    plt.xlabel("Learning Iterations")
    plt.ylabel(f"{name.capitalize()}")
    plt.legend([f"Agent {num}" for num in range(num_players)])
    for param in parameter:
        running_avg = np.zeros(len(param))
        for i in range(len(param)):
            running_avg[i] = np.mean(param[max(0, i-100):(i+1)])
        plt.plot(running_avg)
    plt.savefig(os.path.join(figure_path, f"{name}.png"))
    plt.close()
