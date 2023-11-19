import pygame
import sys

from level.level import Level
from configs.system.window_config import WIDTH, HEIGHT, WATER_COLOR, FPS


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
        main_sound.set_volume(0)
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
