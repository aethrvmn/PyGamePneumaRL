import pygame
import sys

from level.level import Level
from configs.system.window_config import WIDTH, HEIGHT, WATER_COLOR, FPS


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT))  # , pygame.HIDDEN)

        pygame.display.set_caption('Pneuma')

        img = pygame.image.load('assets/graphics/icon.png')
        pygame.display.set_icon(img)
        self.clock = pygame.time.Clock()

        self.level = Level()

        self.max_num_players = len(self.level.player_sprites)

    def calc_score(self):

        self.scores = [0 for _ in range(self.max_num_players)]

        for player in self.level.player_sprites:
            self.scores[player.player_id] = player.stats.exp

    def run(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.level.toggle_menu()

        self.screen.fill(WATER_COLOR)

        self.level.run()

        pygame.display.update()
        self.clock.tick(FPS)

    def quit(self):
        pygame.quit()
        sys.exit()
