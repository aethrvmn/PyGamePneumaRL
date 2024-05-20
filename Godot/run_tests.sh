#!/bin/sh

python main.py --env_path="/home/valapeos/Projects/thesis/Godot/pneuma.x86_64" --speedup=200 --n_parallel=4 --exper_dir="logs/sb3_full_1" &&

python main.py --env_path="/home/valapeos/Projects/thesis/Godot/pneuma.x86_64" --speedup=200 --n_parallel=4 --exper_dir="logs/sb3_full_2" &&

python main.py --env_path="/home/valapeos/Projects/thesis/Godot/pneuma.x86_64" --speedup=200 --n_parallel=4 --exper_dir="logs/sb3_full_3" &&

python main.py --env_path="/home/valapeos/Projects/thesis/Godot/pneuma.x86_64" --speedup=200 --n_parallel=4 --exper_dir="logs/sb3_full_4"
