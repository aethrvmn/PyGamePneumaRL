import sys
import numpy as np
import torch
import pygame
from tqdm import tqdm
from configs.system.window_config import WIDTH, HEIGHT, WATER_COLOR, FPS

from level.level import Level


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT))
        pygame.display.set_caption('Pneuma')
        self.clock = pygame.time.Clock()

        self.level = Level()

        # Sound
        main_sound = pygame.mixer.Sound('assets/audio/main.ogg')
        main_sound.set_volume(0.4)
        main_sound.play(loops=-1)

    def run(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.level.toggle_menu()

        self.screen.fill(WATER_COLOR)

        self.level.run(who='observer')

        pygame.display.update()
        self.clock.tick(FPS)


if __name__ == '__main__':
    n_games = 300

    figure_file = 'plots/score.png'
    score_history = []
    best_score = 0
    avg_score = 0

    agent_list = []

    game_len = 10000

    game = Game()

    for i in tqdm(range(n_games)):
        # TODO: Make game.level.reset_map() so we don't __init__ everything all the time (such a waste)
        game.level.__init__()
        # TODO: Make game.level.reset_map() so we don't pull out and load the agent every time (There is -definitevly- a better way)
        for player in game.level.player_sprites:
            for player_id, agent in agent_list:
                if player.player_id == player_id:
                    player.agent = agent
        agent_list = []
        done = False
        score = 0
        for _ in range(game_len):
            if not game.level.done:
                game.run()
            else:
                break
        for player in game.level.player_sprites:
            agent_list.append((player.player_id, player.agent))

        if i == n_games-1 and game.level.enemy_sprites != []:
            for player in game.level.player_sprites:
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
