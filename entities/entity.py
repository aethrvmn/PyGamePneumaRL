import pygame
import numpy as np

from random import randint

from .components._input import InputHandler
from .components.animation import AnimationHandler

from effects.particle_effects import AnimationPlayer


class Entity(pygame.sprite.Sprite, AnimationHandler, InputHandler):
    def __init__(
             self,
             groups,
             obstacle_sprites,
             visible_sprites,
             attack_sprites = None,
             attackable_sprites = None
            ):

        super().__init__(groups)
        AnimationHandler.__init__(self)
        InputHandler.__init__(self)

        # Sprite Setup
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites
        self.attack_sprites = attack_sprites
        self.attackable_sprites = attackable_sprites



