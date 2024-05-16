import argparse

def parse_args():

    parser = argparse.ArgumentParser(
        prog='Pneuma',
        allow_abbrev=False,
        description='A Reinforcement Learning platform made with Godot',
    )
    parser.add_argument(
        "--env_path",
        default=None,
        type=str,
        help="The Godot binary to use, do not include for in editor training",
    )
    parser.add_argument(
        "--exper_dir",
        default="logs/sb3",
        type=str,
        help="The name of the experiment directory, in which the tensorboard logs and checkpoints (if enabled) are "
        "getting stored.",
    )
    parser.add_argument(
        "--exper_name",
        default="experiment",
        type=str,
        help="The name of the experiment, which will be displayed in tensorboard and "
        "for checkpoint directory and name (if enabled).",
    )
    parser.add_argument(
        "--seed", 
        type=int, 
        default=1,
        help="seed of the experiment"
    )
    parser.add_argument(
        "--resume_model_path",
        default=None,
        type=str,
        help="The path to a model file previously saved using --save_model_path or a checkpoint saved using "
        "--save_checkpoints_frequency. Use this to resume training or infer from a saved model.",
    )
    parser.add_argument(
        "--save_model_path",
        default=None,
        type=str,
        help="The path to use for saving the trained sb3 model after training is complete. Saved model can be used later "
        "to resume training. Extension will be set to .zip",
    )
    parser.add_argument(
        "--save_checkpoint_frequency",
        default=None,
        type=int,
        help=(
            "If set, will save checkpoints every 'frequency' environment steps. "
            "Requires a unique --experiment_name or --experiment_dir for each run. "
            "Does not need --save_model_path to be set. "
        ),
    )
    parser.add_argument(
        "--onnx_export_path",
        default=None,
        type=str,
        help="If included, will export onnx file after training to the path specified.",
    )
    parser.add_argument(
        "--timesteps",
        default=1_000_000,
        type=int,
        help="The number of environment steps to train for, default is 1_000_000. If resuming from a saved model, "
        "it will continue training for this amount of steps from the saved state without counting previously trained "
        "steps",
    )
    parser.add_argument(
        "--inference",
        default=False,
        action="store_true",
        help="Instead of training, it will run inference on a loaded model for --timesteps steps. "
        "Requires --resume_model_path to be set.",
    )
    parser.add_argument(
        "--linear_lr_schedule",
        default=False,
        action="store_true",
        help="Use a linear LR schedule for training. If set, learning rate will decrease until it reaches 0 at "
        "--timesteps"
        "value. Note: On resuming training, the schedule will reset. If disabled, constant LR will be used.",
    )
    parser.add_argument(
        "--viz",
        action="store_true",
        help="If set, the simulation will be displayed in a window during training. Otherwise "
        "training will run without rendering the simulation. This setting does not apply to in-editor training.",
        default=False,
    )
    parser.add_argument(
        "--speedup", 
        default=1, 
        type=int, 
        help="Whether to speed up the physics in the env"
    )
    parser.add_argument(
        "--n_parallel",
        default=1,
        type=int,
        help="How many instances of the environment executable to " "launch - requires --env_path to be set if > 1.",
    )

    return parser.parse_known_args()
