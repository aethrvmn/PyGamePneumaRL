import os
import numpy as np
import matplotlib.pyplot as plt


def plot_learning_curve(scores, num_players, figure_path, n_episodes):

    plt.figure()
    plt.title("Running Average - Score")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.legend([f"Agent {num}" for num in range(num_players)])
    for score in scores:
        running_avg = np.zeros(len(score))
        for i in range(len(score)):
            running_avg[i] = np.mean(score[max(0, i-int(n_episodes/10)):(i+1)])
        plt.plot(running_avg)
    plt.savefig(os.path.join(figure_path, "avg_score.png"))
    plt.close()

def plot_avg_time(time_steps, num_players, fig_path):

    plt.figure()
    plt.title("Average Time Steps per Episode")
    for player in time_steps:
        plt.plot(player)
    plt.savefig(os.path.join(fig_path, 'avg_time.png'))
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


def plot_loss(nn_type, losses, num_players, figure_path, n_episodes):

    plt.figure()
    plt.title(f"Running Average - {nn_type.capitalize()} Loss")
    plt.xlabel("Learning Iterations")
    plt.ylabel("Loss")
    plt.legend([f"Agent {num}" for num in range(num_players)])
    for loss in losses:
        running_avg = np.zeros(len(loss))
        for i in range(len(loss)):
            running_avg[i] = np.mean(loss[max(0, i-int(n_episodes/10)):(i+1)])
        plt.plot(running_avg)
    plt.savefig(os.path.join(figure_path, f"{nn_type}_loss.png"))
    plt.close()


def plot_parameter(name, parameter, num_players, figure_path, n_episodes):

    plt.figure()
    plt.title(f"Running Average - {name.capitalize()}")
    plt.xlabel("Learning Iterations")
    plt.ylabel(f"{name.capitalize()}")
    plt.legend([f"Agent {num}" for num in range(num_players)])
    for param in parameter:
        running_avg = np.zeros(len(param))
        for i in range(len(param)):
            running_avg[i] = np.mean(param[max(0, i-int(n_episodes/10)):(i+1)])
        plt.plot(running_avg)
    plt.savefig(os.path.join(figure_path, f"{name}.png"))
    plt.close()
