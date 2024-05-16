
# Pneuma: Reinforcement Learning Platform

## Introduction

Pneuma is a Reinforcement Learning platform created as part of a thesis project. It is developed using PyGame and offers a customizable environment for testing and implementing reinforcement learning algorithms.

## Installation

To install Pneuma, clone this repository and install the requirements (`requirements.txt`)

After cloning, you can edit the agents, create your own, and modify pneuma.py (the main file). Additionally, consider editing player.setup_agent() for further customization.
Note

- [] TODO: Separate the update logic from the network logic inside the player.

## Usage

To run Pneuma, use the command-line interface with the following options:

-   `--no_seed`: If set to True, runs the program without a seed. Default is False.
-   `--seed [int]`: Specifies the seed for the random number generator. Default is 1.
-   `--n_episodes [int]`: Defines the number of episodes. Default is 300.
-   `--ep_length [int]`: Sets the length of each episode. Default is 5000.
-   `--n_players [int]`: Number of players. Default is 1.
-   `--chkpt_path [str]`: Path for saving/loading agent models. Default is "agents/saved_models".
-   `--figure_path [str]`: Path for saving figures. Default is "figures".
-   `--horizon [int]`: Number of steps per update. Default is 200.
-   `--show_pg`: If True, opens a PyGame window on the desktop. Default is False.
-   `--no_load`: If True, ignores saved models. Default is False.
-   `--gamma [float]`: The gamma parameter for PPO. Default is 0.99.
-   `--alpha [float]`: The alpha parameter for PPO. Default is 0.0003.
-   `--policy_clip [float]`: The policy clip. Default is 0.2.
-   `--batch_size [int]`: Size of each batch. Default is 64.
-   `--n_epochs [int]`: Number of epochs. Default is 10.
-   `--gae_lambda [float]`: The lambda parameter of the GAE. Default is 0.95.

### Example Command

```bash
$ python pneuma.py --seed 42 --n_episodes 300 --ep_length 5000 --n_players 2 --no_load
```

## License

Pneuma is licensed under the Mozilla Public License 2.0.