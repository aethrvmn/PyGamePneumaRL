import pygame
from random import randint, choice

from config.game.spell_config import magic_data
from config.game.weapon_config import weapon_data
#
from .movement import MovementHandler
from .combat import CombatHandler


class InputHandler(MovementHandler, CombatHandler):

    def __init__(self):

        MovementHandler.__init__(self)
        CombatHandler.__init__(self)

        self.status = 'down'

        # Setup Movement
        self.move_cooldown = 15
        self.can_move = True
        self.move_time = None

        # Setup Combat
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Setup Special Actions
        self.can_rotate_weapon = True
        self.weapon_rotation_time = None
        self.rotate_attack_cooldown = 600

        self.can_swap_magic = True
        self.magic_swap_time = None

        # Setup Action Space
        self.possible_actions = [0, 1, 2, 3, 4]
        self.action = 10

    def check_input(self,
                    button,
                    speed,
                    hitbox,
                    obstacle_sprites,
                    rect
                    ):

        if not self.attacking and self.can_move:

            self.move_time = pygame.time.get_ticks()

            # Movement Input
            if self.action == 0:  # keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
                self.can_move = False
                self.action = 0

            elif self.action == 1:  # keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
                self.can_move = False
                self.action = 1

            else:
                self.direction.y = 0

            if self.action == 2:  # keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
                self.can_move = False
                self.action = 2

            elif self.action == 3:  # keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
                self.can_move = False
                self.action = 3

            else:
                self.direction.x = 0

            self.move(speed, hitbox, obstacle_sprites, rect)

            # Combat Input
            if self.action == 4 and not self.attacking:  # keys[pygame.K_e]
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack_sprite()
                self.action = 4

            # Magic Input
            if self.action == 5:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

                self.magic = list(magic_data.keys())[
                    self.magic_index]

                strength = list(magic_data.values())[
                    self.magic_index]['strength'] + self.stats['magic']

                cost = list(magic_data.values())[
                    self.magic_index]['cost']
                self.create_magic_sprite(
                    self.magic, strength, cost)
                self.action = 5

            # Rotating Weapons
            if self.action == 6 and self.can_rotate_weapon:

                self.can_rotate_weapon = False
                self.weapon_rotation_time = pygame.time.get_ticks()

                if self.weapon_index\
                        < len(list(weapon_data.keys())) - 1:

                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[
                    self.weapon_index]
                self.action = 6

            # Swap Spells
            if self.action == 7 and self.can_swap_magic:
                self.can_swap_magic = False
                self.magic_swap_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.action = 7

    def cooldowns(self, vulnerable):
        current_time = pygame.time.get_ticks()
        self.vulnerable = vulnerable

        if self.attacking:
            if current_time - self.attack_time\
                > self.attack_cooldown\
                    + weapon_data[self.weapon]['cooldown']:

                self.attacking = False
                if self.current_attack:
                    self.delete_attack_sprite()

        if not self.can_rotate_weapon:
            if current_time - self.weapon_rotation_time\
                    > self.rotate_attack_cooldown:

                self.can_rotate_weapon = True

        if not self.can_swap_magic:
            if current_time - self.magic_swap_time\
                    > self.rotate_attack_cooldown:

                self.can_swap_magic = True

        if not vulnerable:
            if current_time - self.hurt_time\
                    >= self.invulnerability_duration:

                self.vulnerable = True

        if not self.can_move:
            if current_time - self.move_time\
                    >= self.move_cooldown:

                self.can_move = True
