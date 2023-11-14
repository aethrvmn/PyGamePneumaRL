import os
import pygame
from random import randint

from configs.system.window_config import TILESIZE


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(
            script_dir, '..', 'assets')

        # Sound Setup
        self.sounds = {
            'heal': pygame.mixer.Sound(f'{asset_path}/audio/heal.wav'),
            'flame': pygame.mixer.Sound(f'{asset_path}/audio/flame.wav')
        }

    def heal(self, player, strength, cost, groups):
        if player.stats.energy >= cost:
            self.sounds['heal'].play()
            player.stats.health += strength
            player.stats.energy -= cost
            if player.stats.health >= player.stats.stats['health']:
                player.stats.health = player.stats.stats['health']
            self.animation_player.generate_particles(
                'aura', player.rect.center, groups)
            self.animation_player.generate_particles(
                'heal', player.rect.center + pygame.math.Vector2(0, -50), groups)

    def flame(self, player, cost, groups):
        if player.stats.energy >= cost:
            player.stats.energy -= cost
            self.sounds['flame'].play()

            if player._input.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player._input.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player._input.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:
                    offset_x = direction.x * i * TILESIZE
                    x = player.rect.centerx + offset_x + \
                        randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + \
                        randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.generate_particles(
                        'flame', (x, y), groups)
                else:
                    offset_y = direction.y * i * TILESIZE
                    x = player.rect.centerx + \
                        randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + \
                        randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.generate_particles(
                        'flame', (x, y), groups)
