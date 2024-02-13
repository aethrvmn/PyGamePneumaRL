import argparse
from utils.hyperparams import HPARAMS


def parse_args():

    parser = argparse.ArgumentParser(
        prog='Pneuma',
        description='A Reinforcement Learning platform made with PyGame'
    )

    # Define seed
    parser.add_argument('--no_seed',
                        default=False,
                        action="store_true",
                        help="Set to run without a seed.")

    parser.add_argument('--seed',
                        type=int,
                        default=1,
                        help="The seed for the RNG.")

    # Define episodes and agents
    parser.add_argument('--n_episodes',
                        type=int,
                        default=300,
                        help="Number of episodes.")

    parser.add_argument('--ep_length',
                        type=int,
                        default=5000,
                        help="Length of each episode.")

    parser.add_argument('--n_agents',
                        type=int,
                        default=1,
                        help="Number of agents.")

    # Define hyperparameters
    parser.add_argument('--horizon',
                        type=int,
                        default=HPARAMS["horizon"],
                        help="The number of steps per update")

    parser.add_argument('--gamma',
                        type=float,
                        default=HPARAMS["discount_factor"],
                        help="The discount factor for PPO")

    parser.add_argument('--entropy_coeff',
                        type=float,
                        default=HPARAMS["entropy_coeff"],
                        help="The entropy coefficient")

    parser.add_argument('--alpha',
                        type=float,
                        default=HPARAMS["learning_rate"],
                        help="The learning_rate for PPO")

    parser.add_argument('--policy_clip',
                        type=float,
                        default=HPARAMS["policy_clip"],
                        help="The policy clip for PPO")

    parser.add_argument('--batch_size',
                        type=int,
                        default=HPARAMS["batch_size"],
                        help="The size of each batch")

    parser.add_argument('--n_epochs',
                        type=int,
                        default=HPARAMS["num_epochs"],
                        help="The number of epochs")

    parser.add_argument('--gae_lambda',
                        type=float,
                        default=HPARAMS["GAE_lambda"],
                        help="The lambda parameter of the GAE")

    # Misc
    parser.add_argument('--no_training',
                        default=False,
                        action="store_true",
                        help="Set flag to disable learning. Useful for viewing trained agents interact in the environment.")

    parser.add_argument('--load',
                        type=int,
                        default=None,
                        help="Run id to load within chkpt_path")
    
    parser.add_argument('--show_pg',
                        default=False,
                        action="store_true",
                        help="Set flag to open a PyGame window on desktop")

    return parser.parse_args()
