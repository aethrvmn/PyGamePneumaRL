import pygame
from random import randint

from configs.game.spell_config import magic_data
from configs.game.weapon_config import weapon_data

from .movement import MovementHandler
from .combat import CombatHandler


class InputHandler:

    def __init__(self, sprite_type, status):
        self.status = status

        # Setup Movement
        self.movement = MovementHandler(sprite_type)
        self.move_cooldown = 15
        self.can_move = True
        self.move_time = None

        # Setup Combat
        self.combat = CombatHandler()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.can_move = True

        # Setup Special Actions
        self.can_rotate_weapon = True
        self.weapon_rotation_time = None
        self.rotate_attack_cooldown = 600

        self.can_swap_magic = True
        self.magic_swap_time = None

    def check_input(self, speed, hitbox, obstacle_sprites, rect, player):

        if not self.attacking and self.can_move:
            keys = pygame.key.get_pressed()
            button = randint(0, 7)

            self.move_time = pygame.time.get_ticks()

            # Movement Input
            if button == 0:  # keys[pygame.K_w]:
                self.movement.direction.y = -1
                self.status = 'up'
                self.can_move = False
            elif button == 1:  # keys[pygame.K_s]:
                self.movement.direction.y = 1
                self.status = 'down'
                self.can_move = False
            else:
                self.movement.direction.y = 0

            if button == 2:  # keys[pygame.K_a]:
                self.movement.direction.x = -1
                self.status = 'left'
                self.can_move = False
            elif button == 3:  # keys[pygame.K_d]:
                self.movement.direction.x = 1
                self.status = 'right'
                self.can_move = False
            else:
                self.movement.direction.x = 0

            self.movement.move(speed, hitbox, obstacle_sprites, rect)

            # Combat Input
            if button == 4 and not self.attacking:  # keys[pygame.K_e]
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.combat.create_attack_sprite(player)
                # self.weapon_attack_sound.play()

            # Magic Input
            if button == 5:  # keys[pygame.K_q]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

                self.combat.magic = list(magic_data.keys())[
                    self.combat.magic_index]

                strength = list(magic_data.values())[
                    self.combat.magic_index]['strength'] + player.stats.magic

                cost = list(magic_data.values())[
                    self.combat.magic_index]['cost']
                print(self.combat.magic)
                self.combat.create_magic_sprite(
                    player, self.combat.magic, strength, cost)

            # Rotating Weapons
            if button == 6 and self.can_rotate_weapon:  # keys[pygame.K_LSHIFT]
                self.can_rotate_weapon = False
                self.weapon_rotation_time = pygame.time.get_ticks()
                if self.combat.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.combat.weapon_index += 1
                else:
                    self.combat.weapon_index = 0

                self.combat.weapon = list(weapon_data.keys())[
                    self.combat.weapon_index]

            # Swap Spells
            if button == 7 and self.can_swap_magic:  # keys[pygame.K_LCTRL] :
                self.can_swap_magic = False
                self.magic_swap_time = pygame.time.get_ticks()
                if self.combat.magic_index < len(list(magic_data.keys())) - 1:
                    self.combat.magic_index += 1
                else:
                    self.combat.magic_index = 0

    def cooldowns(self, vulnerable):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time > self.attack_cooldown + weapon_data[self.combat.weapon]['cooldown']:
                self.attacking = False
                if self.combat.current_attack:
                    self.combat.delete_attack_sprite()

        if not self.can_rotate_weapon:
            if current_time - self.weapon_rotation_time > self.rotate_attack_cooldown:
                self.can_rotate_weapon = True

        if not self.can_swap_magic:
            if current_time - self.magic_swap_time > self.rotate_attack_cooldown:
                self.can_swap_magic = True

        if not vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                vulnerable = True

        if not self.can_move:
            if current_time - self.move_time >= self.move_cooldown:
                self.can_move = True
