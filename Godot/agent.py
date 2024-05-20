import args
import os
import pathlib

import torch as T
import torch.nn as nn

from typing import Callable

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env.vec_monitor import VecMonitor

from godot_rl.core.utils import can_import
from godot_rl.wrappers.onnx.stable_baselines_export import export_ppo_model_as_onnx
from godot_rl.wrappers.stable_baselines_wrapper import StableBaselinesGodotEnv

def main(policy_name=None, policy=None, parseargs=None):
    if can_import("ray"):
        print("WARNING: SB3 and ray[rllib] are not compatible.")

    args, extras = parseargs
    # args, extras = args.parse_args()

    def handle_onnx_export():
        '''
        Enforces the onnx and zip extentions when saving models.
        This avoids potential conflicts in case of identical names and extentions
        '''
        if args.onnx_export_path is not None:
            path_onnx = pathlib.Path(args.onnx_export_path).with_suffix(".onnx")
            print(f"Exporting onnx to: {os.path.abspath(path_onnx)}")
            export_ppo_model_as_onnx(model, str(path_onnx))

    def handle_model_save():
        if args.save_model_path is not None:
            zip_save_path = pathlib.Path(Args.save_model_path).with_suffix(".zip")
            print(f"Saving model to: {os.path.abspath(zip_save_path)}")
            model.save(zip_save_path)

    def close_env():
        try:
            print("Closing env...")
            env.close()
        except Exception as e:
            print(f"Exception while closing env: {e}")

    if policy_name is None:
        path_checkpoint = os.path.join(args.exper_dir, f"{args.exper_name}_checkpoints")
    else:
        path_checkpoint = os.path.join(args.exper_dir, f"{policy_name}_checkpoints")        
    
    abs_path_checkpoint = os.path.abspath(path_checkpoint)

    if args.save_checkpoint_frequency is not None and os.path.isdir(path_checkpoint):
        raise RuntimeError(
            f"{abs_path_checkpoint} already exists."
            "Use a different directory or different name."
            "If you want to override previous checkpoints you have to delete them manually."
        )

    if args.inference and args.resume_model_path is None:
        raise parser.error(
            "Using --inference requires --resume_model_path to be set."
        )

    if args.env_path is None and args.viz:
        print("Info: using --viz without --env_path set has no effect.")
        print("\nIn editor training will always render.")

    env = StableBaselinesGodotEnv(
        env_path=args.env_path,
        show_window=args.viz,
        seed=args.seed,
        n_parallel=args.n_parallel,
        speedup=args.speedup
    )
    env = VecMonitor(env)

    # LR schedule code snippet from:
    # https://stable-baselines3.readthedocs.io/en/master/guide/examples.html#learning-rate-schedule
    def linear_schedule(initial_value: float) -> Callable[[float], float]:
        """
        Linear learning rate schedule.

        :param initial_value: Initial learning rate.
        :return: schedule that computes
          current learning rate depending on remaining progress
        """

        def func(progress_remaining: float) -> float:
            """
            Progress will decrease from 1 (beginning) to 0.

            :param progress_remaining:
            :return: current learning rate
            """
            return progress_remaining * initial_value

        return func

    if args.resume_model_path is None:
        if not args.linear_lr_schedule:
            learning_rate = 0.0003
        else:
            linear_schedule(0.0003)

        model: PPO = PPO(
            # 'MultiInputPolicy' serves as an alias for MultiInputActorCriticPolicy
            "MultiInputPolicy",
            env,
            batch_size=64,
            ent_coef=0.01,
            verbose=2,
            n_steps=256,
            tensorboard_log=args.exper_dir,
            learning_rate=learning_rate,
            policy_kwargs=policy,
        )
    else:
        path_zip = pathlib.Path(args.resume_model_path)
        print(f"Loading model: {os.path.abspath(pathzip)}")
        model: PPO = PPO.load(
            path_zip, 
            env=env, 
            tensorboard_log=args.exper_dir
        )

    if args.inference:
        obs = env.reset()
        for i in range(args.timesteps):
            action, _state = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
    else:
        learn_arguments = dict(
            total_timesteps=args.timesteps, 
            tb_log_name=policy_name
        )
        if args.save_checkpoint_frequency:
            print("Checkpoint saving enabled.")
            print(f"\nCheckpoints will be saved to {abs_path_checkpoint}")
            checkpoint_callback = CheckpointCallback(
                save_freq=(args.save_checkpoint_frequency // env.num_envs),
                save_path=path_checkpoint,
                name_prefix=policy_name
            )
            learn_arguments["callback"] = checkpoint_callback
        try:
            model.learn(**learn_arguments)
        except KeyboardInterrupt:
            print(
                """
                    Training interrupted by user. Will save if --save_model_path was set and/or export if --onnx_export was set.
                """
            )

    close_env()
    handle_onnx_export()
    handle_model_save()
