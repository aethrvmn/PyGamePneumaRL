import pygame
from random import randint

from configs.game.weapon_config import weapon_data
from configs.game.spell_config import magic_data

from .components.stats import StatsHandler
from .components._input import InputHandler
from .components.animaton import AnimationHandler

from effects.particle_effects import AnimationPlayer


class Player(pygame.sprite.Sprite):

    def __init__(self, position, groups, obstacle_sprites, visible_sprites, attack_sprites, attackable_sprites, role):
        super().__init__(groups)

        # Setup Sprites
        self.sprite_type = 'player'
        self.visible_sprites = visible_sprites
        self.attack_sprites = attack_sprites
        self.obstacle_sprites = obstacle_sprites
        self.attackable_sprites = attackable_sprites

        # Setup Graphics
        self.animation_player = AnimationPlayer()
        self.animation = AnimationHandler(self.sprite_type)
        self.animation.import_assets(position)
        self.image = self.animation.image
        self.rect = self.animation.rect

        # Setup Inputs
        self._input = InputHandler(
            self.sprite_type, self.animation_player)  # , self.status)

        # Setup Stats
        self.role = role
        self.stats = StatsHandler(self.sprite_type, self.role)

        self.distance_direction_from_enemy = None

    def get_status(self):
        if self._input.movement.direction.x == 0 and self._input.movement.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status += '_idle'

        if self._input.attacking:
            self._input.movement.direction.x = 0
            self._input.movement.direction.y = 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    position=pos - offset, groups=[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damaged(
                                self, attack_sprite.sprite_type)

    def get_full_weapon_damage(self):
        base_damage = self.stats.attack
        weapon_damage = weapon_data[self._input.combat.weapon]['damage']
        return (base_damage + weapon_damage)

    def get_full_magic_damage(self):
        base_damage = self.stats.magic
        spell_damage = magic_data[self._input.combat.magic]['strength']
        return (base_damage + spell_damage)

    def update(self):
        # Refresh objects based on input
        self._input.check_input(
            self.stats.speed, self.animation.hitbox, self.obstacle_sprites, self.animation.rect, self)
        self.status = self._input.status

        # Animate
        self.get_status()
        self.animation.animate(self.status, self._input.combat.vulnerable)
        self.image = self.animation.image
        self.rect = self.animation.rect

        # Cooldowns and Regen
        self.stats.energy_recovery()
        self._input.cooldowns(self._input.combat.vulnerable)
