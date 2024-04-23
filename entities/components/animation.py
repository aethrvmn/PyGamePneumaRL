import os
import pygame

from math import sin

from config.system.window import HITBOX_OFFSET

from effects.particle_effects import AnimationPlayer

from .stats import StatsHandler

from utils.resource_loader import import_folder, import_assets


class AnimationHandler(StatsHandler):

    def __init__(self):

        self.frame_index = 0
        self.animation_speed = 0.15

    def import_assets(self, position):

        # Import graphic assets
        if self.sprite_type == 'player':
            self.image = pygame.image.load(
                import_assets(os.path.join('graphics',
                                           'player',
                                           'down',
                                           'down_0.png'))).convert_alpha()

            self.rect = self.image.get_rect(topleft=position)
            self.hitbox = self.rect.inflate(HITBOX_OFFSET[self.sprite_type])

            self.animations = {
                'up': [], 'down': [],
                'left': [], 'right': [],
                'up_idle': [], 'down_idle': [],
                'left_idle': [], 'right_idle': [],
                'up_attack': [], 'down_attack': [],
                'left_attack': [], 'right_attack': []
            }

            for animation in self.animations.keys():
                self.animations[animation]\
                    = import_folder(os.path.join('graphics',
                                                 'player',
                                                 animation
                                                 ))

        elif self.sprite_type == 'enemy':

            self.status = 'idle'

            self.animations = {'idle': [], 'move': [], 'attack': []}

            for animation in self.animations.keys():
                self.animations[animation]\
                    = import_folder(os.path.join('graphics',
                                                 'monsters',
                                                 self.name,
                                                 animation))

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

    def trigger_death_particles(self, position, particle_type, groups):
        AnimationPlayer().generate_particles(
            particle_type, position, groups)

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
