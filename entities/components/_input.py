import pygame
from random import randint, choice

from config.game.spell_config import magic_data
from config.game.weapon_config import weapon_data

from .movement import MovementHandler
from .combat import CombatHandler


class InputHandler:

    def __init__(self, sprite_type, animation_player, ai_controller=False):
        self.status = 'down'
        self.sprite_type = sprite_type

        # Setup Movement
        self.movement = MovementHandler(self.sprite_type)
        self.move_cooldown = 15
        self.can_move = True
        self.move_time = None

        # Setup Combat
        self.combat = CombatHandler(animation_player)
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
        self.possible_actions = [0, 1, 2, 3, 4, 5]
        self.action = 10

    def check_input(self,
                    button,
                    speed,
                    hitbox,
                    obstacle_sprites,
                    rect,
                    player):

        if not self.attacking and self.can_move:

            self.move_time = pygame.time.get_ticks()

            # Movement Input
            if button == 0:  # keys[pygame.K_w]:
                self.movement.direction.y = -1
                self.status = 'up'
                self.can_move = False
                self.action = 0

            elif button == 1:  # keys[pygame.K_s]:
                self.movement.direction.y = 1
                self.status = 'down'
                self.can_move = False
                self.action = 1

            else:
                self.movement.direction.y = 0

            if button == 2:  # keys[pygame.K_a]:
                self.movement.direction.x = -1
                self.status = 'left'
                self.can_move = False
                self.action = 2

            elif button == 3:  # keys[pygame.K_d]:
                self.movement.direction.x = 1
                self.status = 'right'
                self.can_move = False
                self.action = 3

            else:
                self.movement.direction.x = 0

            self.movement.move(speed, hitbox, obstacle_sprites, rect)

            # Combat Input
            if button == 4 and not self.attacking:  # keys[pygame.K_e]
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.combat.create_attack_sprite(player)
                self.action = 4

            # Magic Input
            if button == 5:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

                self.combat.magic = list(magic_data.keys())[
                    self.combat.magic_index]

                strength = list(magic_data.values())[
                    self.combat.magic_index]['strength'] + player.stats.magic

                cost = list(magic_data.values())[
                    self.combat.magic_index]['cost']
                self.combat.create_magic_sprite(
                    player, self.combat.magic, strength, cost)
                self.action = 5

            # Rotating Weapons
            if button == 6 and self.can_rotate_weapon:

                self.can_rotate_weapon = False
                self.weapon_rotation_time = pygame.time.get_ticks()

                if self.combat.weapon_index\
                        < len(list(weapon_data.keys())) - 1:

                    self.combat.weapon_index += 1
                else:
                    self.combat.weapon_index = 0

                self.combat.weapon = list(weapon_data.keys())[
                    self.combat.weapon_index]
                self.action = 6

            # Swap Spells
            if button == 7 and self.can_swap_magic:
                self.can_swap_magic = False
                self.magic_swap_time = pygame.time.get_ticks()
                if self.combat.magic_index < len(list(magic_data.keys())) - 1:
                    self.combat.magic_index += 1
                else:
                    self.combat.magic_index = 0
                self.action = 7

    def cooldowns(self, vulnerable):
        current_time = pygame.time.get_ticks()
        self.vulnerable = vulnerable

        if self.attacking:
            if current_time - self.attack_time\
                > self.attack_cooldown\
                    + weapon_data[self.combat.weapon]['cooldown']:

                self.attacking = False
                if self.combat.current_attack:
                    self.combat.delete_attack_sprite()

        if not self.can_rotate_weapon:
            if current_time - self.weapon_rotation_time\
                    > self.rotate_attack_cooldown:

                self.can_rotate_weapon = True

        if not self.can_swap_magic:
            if current_time - self.magic_swap_time\
                    > self.rotate_attack_cooldown:

                self.can_swap_magic = True

        if not vulnerable:
            if current_time - self.combat.hurt_time\
                    >= self.combat.invulnerability_duration:

                self.combat.vulnerable = True

        if not self.can_move:
            if current_time - self.move_time\
                    >= self.move_cooldown:

                self.can_move = True
