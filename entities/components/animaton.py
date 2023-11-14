import os
import pygame
from math import sin

from utils.resource_loader import import_folder

from configs.system.window_config import HITBOX_OFFSET


class AnimationHandler:

    def __init__(self, sprite_type, name=None):
        self.frame_index = 0
        self.animation_speed = 0.15

        self.sprite_type = sprite_type
        self.name = name

    def import_assets(self, position):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(
            script_dir, '../..', 'assets', 'graphics')

        if self.sprite_type == 'player':

            character_path = f"{asset_path}/player"

            # Import Graphic Assets
            self.image = pygame.image.load(
                f"{character_path}/down/down_0.png").convert_alpha()
            self.rect = self.image.get_rect(topleft=position)
            self.hitbox = self.rect.inflate(HITBOX_OFFSET[self.sprite_type])

            self.animations = {
                'up': [], 'down': [], 'left': [], 'right': [],
                'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
            }
            for animation in self.animations.keys():
                full_path = f"{character_path}/{animation}"
                self.animations[animation] = import_folder(full_path)

        elif self.sprite_type == 'enemy':

            self.status = 'idle'

            character_path = f"{asset_path}/monsters/{self.name}"

            self.animations = {'idle': [], 'move': [], 'attack': []}

            for animation in self.animations.keys():
                self.animations[animation] = import_folder(
                    f"{character_path}/{animation}")

            self.image = self.animations[self.status][self.frame_index]
            self.rect = self.image.get_rect(topleft=position)
            self.hitbox = self.rect.inflate(0, -10)

    def animate(self, status, vulnerable=True, can_attack=False):

        animation = self.animations[status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.sprite_type == 'enemy':
                if status == 'attack':
                    self.can_attack = False
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def trigger_death_particles(self, animation_player, position, particle_type, groups):
        animation_player.generate_particles(
            particle_type, position, groups)

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
