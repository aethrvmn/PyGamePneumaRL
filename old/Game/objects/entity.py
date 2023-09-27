import pygame
from math import sin
import random

from utils.settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, is_AI, state=None):
        super().__init__(groups)

        # Animation
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement
        self.direction = pygame.math.Vector2()
        self.move_cooldown = 150
        self.can_move = True
        self.move_time = None

        # AI Setup
        if is_AI:
            self.possible_actions = {
                0: ('up', -1, 0),
                1: ('down', 1, 0),
                2: ('left', 0, -1),
                3: ('right', 0, 1),
                4: ('attack', None, None),
                5: ('magic', None, None),
                6: ('rotate_weapon', None, None),
                7: ('swap_magic', None, None)
            }
            self.state = state
            self.distance_direction_to_player = [
                float('inf'), 0, 0, None, None, None, None, None, None, None, None, None]*5

            # self.agent = Agent(self.possible_actions, self.distance_direction_to_player, self.stats, self.exp, None, None)

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # The following works for static obstacles only
                if sprite.hitbox.colliderect(self.hitbox):
                    # Moving Right
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    # Moving Left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                # The following works for static obstacles only
                if sprite.hitbox.colliderect(self.hitbox):
                    # Moving Down
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    # Moving Up
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def input(self):
        if not self.attacking and self.can_move:
            keys = pygame.key.get_pressed()
            button = random.randint(0, 5)

            self.move_time = pygame.time.get_ticks()

            # Movement Input
            if button == 0:  # keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
                self.can_move = False
            elif button == 1:  # keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
                self.can_move = False
            else:
                self.direction.y = 0

            if button == 2:  # keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
                self.can_move = False
            elif button == 3:  # keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
                self.can_move = False
            else:
                self.direction.x = 0

            # Combat Input
            if button == 4:  # keys[pygame.K_e]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack_sprite()
                self.weapon_attack_sound.play()

            # Magic Input
            if button == 5:  # keys[pygame.K_q]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[
                    self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic_sprite(style, strength, cost)

            # Rotating Weapons
            if keys[pygame.K_LSHIFT] and self.can_rotate_weapon:
                self.can_rotate_weapon = False
                self.weapon_rotation_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # Swap Spells
            if keys[pygame.K_LCTRL] and self.can_swap_magic:
                self.can_swap_magic = False
                self.magic_swap_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
