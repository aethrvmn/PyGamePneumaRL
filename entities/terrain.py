import pygame

from config.system.window import TILESIZE,\
    HITBOX_OFFSET


class Terrain(pygame.sprite.Sprite):

    def __init__(self,
                 position,
                 groups,
                 sprite_type,
                 surface=pygame.Surface((TILESIZE, TILESIZE))
                 ):

        super().__init__(groups)

        self.sprite_type = sprite_type

        self.position = position

        self.image = surface

        if sprite_type == 'object':
            # Offset
            self.rect = self.image.get_rect(
                topleft=(position[0], position[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=position)

        self.hitbox = self.rect.inflate(HITBOX_OFFSET[sprite_type])
