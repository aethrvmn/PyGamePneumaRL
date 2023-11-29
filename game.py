import os
import sys
import pygame

from level import Level

from configs.system.window_config import WIDTH,\
    HEIGHT,\
    WATER_COLOR,\
    FPS


class Game:

    def __init__(self, show_pg=False, n_players=1,):
        print(f"Initializing Pneuma with {n_players} player(s).\
              \nShowing PyGame screen: {'True' if show_pg else 'False'}")

        pygame.init()

        if show_pg:

            self.screen = pygame.display.set_mode(
                (WIDTH, HEIGHT)
            )

        else:
            self.screen = pygame.display.set_mode(
                (WIDTH, HEIGHT),
                pygame.HIDDEN
            )

        pygame.display.set_caption("Pneuma")

        img = pygame.image.load(os.path.join('assets',
                                             'graphics',
                                             'icon.png'))
        pygame.display.set_icon(img)

        self.level = Level(n_players)

    def run(self):

        self.clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.level.pause()

        self.screen.fill(WATER_COLOR)

        self.level.run('observer', self.clock.get_fps())

        pygame.display.update()
        self.clock.tick(FPS)

    def quit(self):
        pygame.quit()
        sys.exit()
