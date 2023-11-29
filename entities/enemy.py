import pygame

from .components.animaton import AnimationHandler
from .components.stats import StatsHandler
from .components._input import InputHandler

from effects.particle_effects import AnimationPlayer


class Enemy(pygame.sprite.Sprite):

    def __init__(self, name, position, groups, visible_sprites, obstacle_sprites):
        super().__init__(groups)

        self.sprite_type = "enemy"
        self.name = name

        self.visible_sprites = visible_sprites

        # Setup Graphics
        self.animation_player = AnimationPlayer()
        self.animation = AnimationHandler(self.sprite_type, self.name)
        self.animation.import_assets(position)
        self.image = self.animation.image
        self.rect = self.animation.rect

        # Setup Inputs
        self._input = InputHandler(
            self.sprite_type, self.animation_player)

        # Setup Stats
        self.stats = StatsHandler(self.sprite_type, monster_name=self.name)
        self.obstacle_sprites = obstacle_sprites

        self.distance_direction_from_player = None

    def get_action(self):
        player_distance = sorted(
            self.distance_direction_from_player, key=lambda x: x[0])[0]

        if player_distance[0] < self.stats.notice_radius and player_distance[0] >= self.stats.attack_radius:
            self._input.movement.direction = player_distance[1]
            self.animation.status = "move"
            self._input.movement.move(
                self.stats.speed, self.animation.hitbox, self.obstacle_sprites, self.animation.rect)
        elif player_distance[0] <= self.stats.attack_radius:
            self.animation.status = 'attack'
        else:
            self.animation.status = 'idle'

    def add_exp(self, player):
        player.stats.exp += self.stats.exp

    def check_death(self, player):
        if self.stats.health <= 0:
            self.add_exp(player)
            self.animation.trigger_death_particles(
                self.animation_player, self.rect.center, self.name, self.visible_sprites)
            self.kill()

    def get_damaged(self, player, attack_type):
        if self._input.combat.vulnerable:
            for _, direction, attacking_player in self.distance_direction_from_player:
                if attacking_player == player:
                    self._input.movement.direction = -direction
                    self._input.movement.move(
                        self.stats.speed * self.stats.knockback, self.animation.hitbox, self.obstacle_sprites, self.animation.rect)
                    break
            if attack_type == 'weapon':
                self.stats.health -= player.get_full_weapon_damage()
            else:
                self.stats.health -= player.get_full_magic_damage()
            self.check_death(player)
            self._input.combat.hurt_time = pygame.time.get_ticks()
            self._input.combat.vulnerable = False

    def update(self):

        self.get_action()

        self.animation.animate(self.animation.status,
                               self._input.combat.vulnerable)
        self.image = self.animation.image
        self.rect = self.animation.rect

        self._input.cooldowns(self._input.combat.vulnerable)
