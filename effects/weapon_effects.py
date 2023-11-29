import os
import pygame

from utils.resource_loader import import_assets


class Weapon(pygame.sprite.Sprite):

    def __init__(self, player, groups):
        super().__init__(groups)

        self.sprite_type = 'weapon'
        direction = player._input.status.split('_')[0]

        # Graphic
        self.image = pygame.image.load(import_assets(os.path.join(
            'graphics',
            'weapons',
            player._input.combat.weapon,
            f"{direction}.png"))
        ).convert_alpha()

        # Sprite Placement
        if direction == 'right':
            self.rect = self.image.get_rect(
                midleft=player.animation.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(
                midright=player.animation.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(
                midtop=player.animation.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(
                midbottom=player.animation.rect.midtop + pygame.math.Vector2(-10, 0))
