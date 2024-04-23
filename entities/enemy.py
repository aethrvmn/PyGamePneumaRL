import pygame

from .entity import Entity

from effects.particle_effects import AnimationPlayer


class Enemy(Entity):

    def __init__(self,
                 name,
                 position,
                 groups,
                 visible_sprites,
                 obstacle_sprites
                 ):

        super().__init__(groups=groups,
                        visible_sprites=visible_sprites,
                        obstacle_sprites=obstacle_sprites,
                        attack_sprites=None,
                        attackable_sprites=None)

        # Setup stats
        self.sprite_type = 'enemy'
        self.name = name
        self.get_stats(self.sprite_type, monster_name=self.name)

        # Graphics Setup
        self.animation_player = AnimationPlayer()
        self.import_assets(position)

        self.distance_direction_from_player = None

    def get_action(self):
        player_distance = sorted(
            self.distance_direction_from_player, key=lambda x: x[0])[0]

        if player_distance[0] < self.notice_radius and player_distance[0] >= self.attack_radius:
            self.direction = player_distance[1]
            self.status = "move"
            self.move(
                self.speed, self.hitbox, self.obstacle_sprites, self.rect)
        elif player_distance[0] <= self.attack_radius:
            self.status = 'attack'
        else:
            self.status = 'idle'

    def add_exp(self, player):
        player.exp += self.exp

    def check_death(self, player):
        if self.health <= 0:
            self.add_exp(player)
            self.trigger_death_particles(
                self.rect.center, self.name, self.visible_sprites)
            self.kill()

    def get_damaged(self, player, attack_type):
        if self.vulnerable:
            for _, direction, attacking_player in self.distance_direction_from_player:
                if attacking_player == player:
                    self.direction = -direction
                    self.move(
                        self.speed * self.knockback, self.hitbox, self.obstacle_sprites, self.rect)
                    break
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.check_death(player)
            self.hurt_time = pygame.time.get_ticks()
            self.vulnerable = False

    def update(self):

        self.get_action()

        self.animate(self.status, self.vulnerable)
        self.image = self.image
        self.rect = self.rect

        self.cooldowns(self.vulnerable)
