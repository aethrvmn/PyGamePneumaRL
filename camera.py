import os
import pygame

from utils.resource_loader import import_assets


class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

        # General Setup
        self.display_surface = pygame.display.get_surface()
        self.display_size = self.display_surface.get_size()

        self.floor_surf = pygame.image.load(
            import_assets(
                os.path.join('graphics',
                             'tilemap',
                             'ground.png')
            )
        ).convert()

        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        self.calculate_scale()

    def calculate_scale(self):
        map_width, map_height = self.floor_rect.size
        screen_width, screen_height = self.display_size

        # Calculating the scale to fit the map on the screen
        self.scale = min(screen_width / map_width, screen_height / map_height)
        self.scaled_floor_surf = pygame.transform.scale(self.floor_surf,
                                                        (int(map_width * self.scale),
                                                         int(map_height * self.scale)))
        self.scaled_floor_rect = self.scaled_floor_surf.get_rect()

    def custom_draw(self):
        # Drawing the scaled floor
        self.display_surface.blit(
            self.scaled_floor_surf, self.scaled_floor_rect.topleft)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery if not hasattr(sprite, 'animation') else sprite.animation.rect.centery):
            # Check for sprites with 'animation' attribute
            if hasattr(sprite, 'animation'):
                scaled_sprite_image = pygame.transform.scale(sprite.animation.image,
                                                             (int(sprite.animation.rect.width * self.scale),
                                                              int(sprite.animation.rect.height * self.scale)))
                scaled_position = (int(sprite.animation.rect.x * self.scale),
                                   int(sprite.animation.rect.y * self.scale))
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery if not hasattr(sprite, 'animation') else sprite.animation.rect.centery):
            # Check for sprites with 'animation' attribute
            if hasattr(sprite, 'animation'):
                scaled_sprite_image = pygame.transform.scale(sprite.animation.image,
                                                             (int(sprite.animation.rect.width * self.scale),
                                                              int(sprite.animation.rect.height * self.scale)))
                scaled_position = (int(sprite.animation.rect.x * self.scale),
                                   int(sprite.animation.rect.y * self.scale))
            else:
                scaled_sprite_image = pygame.transform.scale(sprite.image,
                                                             (int(sprite.rect.width * self.scale),
                                                              int(sprite.rect.height * self.scale)))
                scaled_position = (int(sprite.rect.x * self.scale),
                                   int(sprite.rect.y * self.scale))

            self.display_surface.blit(scaled_sprite_image, scaled_position)
