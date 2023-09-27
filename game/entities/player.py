import pygame

from .components.combat import CombatHandler
from .components.stats import StatsHandler
from .components._input import InputHandler
from .components.animaton import AnimationHandler


class Player(pygame.sprite.Sprite):

    def __init__(self, position, groups, obstacle_sprites, visible_sprites, attack_sprites):
        super().__init__(groups)

        # Setup Sprites
        self.sprite_type = 'player'
        self.visible_sprites = visible_sprites
        self.attack_sprites = attack_sprites
        self.obstacle_sprites = obstacle_sprites
        self.status = 'down'

        # Setup Inputs
        self._input = InputHandler(
            self.sprite_type, self.status)

        # Setup Graphics
        self.animation = AnimationHandler()
        self.animation.import_assets(self.sprite_type, position)
        self.animate = self.animation.animate
        self.image = self.animation.image
        self.animate(self.status, self._input.combat.vulnerable)
        self.rect = self.animation.rect

        # Setup Stats
        self.stats = StatsHandler()

    def get_status(self):
        if self._input.movement.direction.x == 0 and self._input.movement.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'

        if self._input.attacking:
            self._input.movement.direction.x = 0
            self._input.movement.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def update(self):
        # Refresh objects based on input
        self._input.check_input(
            self.stats.stats['speed'], self.animation.hitbox, self.obstacle_sprites, self.animation.rect, self)
        self.status = self._input.status

        # Animate
        self.get_status()
        self.animation.animate(self.status, self._input.combat.vulnerable)
        self.image = self.animation.image
        self.rect = self.animation.rect

        # Cooldowns and Regen
        self.stats.energy_recovery()
        self._input.cooldowns(self._input.combat.vulnerable)
