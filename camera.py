import os
import pygame

from utils.resource_loader import import_assets


class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

        # General Setup
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)

        self.floor_surf = pygame.image.load(
            import_assets(
                os.path.join('graphics',
                             'tilemap',
                             'ground.png')
            )
        ).convert()

        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, entity):

        self.sprite_type = entity.sprite_type
        # Getting the offset
        if hasattr(entity, 'animation'):
            self.offset.x = entity.animation.rect.centerx - self.half_width

            self.offset.y = entity.animation.rect.centery - self.half_height

        else:
            self.offset.x = entity.rect.centerx - self.half_width

            self.offset.y = entity.rect.centery - self.half_height

        # Drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(),
                             key=lambda sprite: sprite.animation.rect.centery
                             if hasattr(sprite, 'animation')
                             else sprite.rect.centery):

            if hasattr(sprite, 'animation'):
                offset_pos = sprite.animation.rect.topleft - self.offset
                self.display_surface.blit(sprite.animation.image, offset_pos)
            else:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
