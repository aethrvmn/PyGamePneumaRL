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
game_len = 5000

figure_file = 'plots/score_sp.png'

game = Game()

agent = game.level.player_sprites[0].agent

score_history = np.zeros(shape=(game.max_num_players, n_episodes))
best_score = np.zeros(game.max_num_players)
avg_score = np.zeros(game.max_num_players)

for i in tqdm(range(n_episodes)):
    # TODO: Make game.level.reset_map() so we don't __init__ everything all the time (such a waste)
    if i != 0:
        game.level.__init__(reset=True)
    # TODO: Make game.level.reset_map() so we don't pull out and load the agent every time (There is -definitevly- a better way)

    for player in game.level.player_sprites:
        player.stats.exp = score_history[player.player_id][i-1]
        player.agent = agent

    for j in tqdm(range(game_len)):
        if not game.level.done:

            game.run()
            game.calc_score()

            for player in game.level.player_sprites:
                if player.is_dead():
                    player.kill()

            # if (j == game_len-1 or game.level.done) and game.level.enemy_sprites != []:
            #     for player in game.level.player_sprites:
            #         for enemy in game.level.enemy_sprites:
            #             player.stats.exp *= .95

    for player in game.level.player_sprites:
        exp_points = player.stats.exp
        score_history[player.player_id][i] = exp_points
        avg_score[player.player_id] = np.mean(
            score_history[player.player_id])

    if np.mean(avg_score) > np.mean(best_score):
        best_score = avg_score
        print("Saving models for agent...")
        player.agent.save_models(
            actr_chkpt="player_actor", crtc_chkpt="player_critic")
        print("Models saved ...\n")

    print(
        f"\nAverage score: {np.mean(avg_score)}\nBest score: {np.mean(best_score)}")


plt.plot(score_history)
plt.savefig(figure_file)
game.quit()

plt.show()
