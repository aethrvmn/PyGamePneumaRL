from game import Game
from tqdm import tqdm

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


if __name__ == '__main__':
    n_episodes = 3000

    figure_file = 'plots/score.png'
    score_history = []
    best_score = 0
    avg_score = 0

    agent_list = []

    game_len = 5000

    game = Game()

    for i in tqdm(range(n_episodes)):
        # TODO: Make game.level.reset_map() so we don't __init__ everything all the time (such a waste)
        if i != 0:
            game.level.__init__(reset=True)
        # TODO: Make game.level.reset_map() so we don't pull out and load the agent every time (There is -definitevly- a better way)
        for player in game.level.player_sprites:
            for player_id, agent in agent_list:
                if player.player_id == player_id:
                    player.agent = agent

        agent_list = []
        done = False
        score = 0
        for _ in tqdm(range(game_len)):
            if not game.level.done:
                game.run()
            else:
                break
        for player in game.level.player_sprites:
            agent_list.append((player.player_id, player.agent))

        if i == n_episodes-1 and game.level.enemy_sprites != []:
            for player in game.level.player_sprites:
                for enemy in game.level.enemy_sprites:
                    player.stats.exp -= 5
                player.update()

        for player in game.level.player_sprites:
            player.agent.save_models()

        # TODO: Make it so that scores appear here for each player
        # score_history.append(game.level.player.score)
        # print(score)
        # avg_score = np.mean(score_history[-100:])

        # if avg_score > best_score:
        #     best_score = avg_score
        #     game.level.player.agent.save_models()
