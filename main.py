import random
import torch as T
import numpy as np
import matplotlib.pyplot as plt

from game import Game
from tqdm import tqdm

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


random.seed(1)
np.random.seed(1)
T.manual_seed(1)

n_episodes = 1000
game_len = 10000

figure_file = 'plots/score.png'

game = Game()

agent_list = [0 for _ in range(game.max_num_players)]

score_history = np.zeros(
    shape=(game.max_num_players, n_episodes))
best_score = np.zeros(game.max_num_players)
avg_score = np.zeros(game.max_num_players)

for i in tqdm(range(n_episodes)):
    # TODO: Make game.level.reset_map() so we don't __init__ everything all the time (such a waste)
    if i != 0:
        game.level.__init__(reset=True)
    # TODO: Make game.level.reset_map() so we don't pull out and load the agent every time (There is -definitevly- a better way)
        for player in game.level.player_sprites:
            for agent in agent_list:
                player.agent = agent_list[player.player_id]
                player.stats.exp = score_history[player.player_id][i-1]

    agent_list = [0 for _ in range(game.max_num_players)]

    for j in range(game_len):
        if not game.level.done:

            game.run()
            game.calc_score()

            for player in game.level.player_sprites:
                if player.is_dead():
                    agent_list[player.player_id] = player.agent
                    player.kill()

            # if (j == game_len-1 or game.level.done) and game.level.enemy_sprites != []:
            #     for player in game.level.player_sprites:
            #         for enemy in game.level.enemy_sprites:
            #             player.stats.exp *= .95
        else:
            break

    for player in game.level.player_sprites:
        if not player.is_dead():
            agent_list[player.player_id] = player.agent
        exp_points = player.stats.exp
        score_history[player.player_id][i] = exp_points
        avg_score[player.player_id] = np.mean(
            score_history[player.player_id])
        if avg_score[player.player_id] > best_score[player.player_id]:
            best_score[player.player_id] = avg_score[player.player_id]
            print(f"Saving models for agent {player.player_id}...")
            player.agent.save_models(actr_chkpt = f"player_{player.player_id}_actor", crtc_chkpt = f"player_{player.player_id}_critic")
            print("Models saved ...\n")

        print(
            f"\nCumulative score for player {player.player_id}: {score_history[0][i]}\nAverage score for player {player.player_id}: {avg_score[player.player_id]}\nBest score for player {player.player_id}:                    {best_score[player.player_id]}")



plt.plot(score_history[0])

game.quit()

plt.show()
