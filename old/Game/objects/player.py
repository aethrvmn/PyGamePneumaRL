import pygame
import random
import numpy as np

from utils.settings import *
from utils.support import import_folder

from objects.entity import Entity

from rl.agent import Agent
from rl.rl_settings import *


class Player(Entity):

    def __init__(self, position, groups, obstacle_sprites, create_attack_sprite, delete_attack_sprite, create_magic_sprite, is_AI, state):
        super().__init__(groups, is_AI, state)

        self.image = pygame.image.load(
            '../Graphics/graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(HITBOX_OFFSET['player'])
        self.sprite_type = 'player'

        # Graphics Setup
        self.import_player_assets()
        self.status = 'down'

        # Combat
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Weapons
        self.create_attack_sprite = create_attack_sprite
        self.delete_attack_sprite = delete_attack_sprite

        # Magic
        self.create_magic_sprite = create_magic_sprite

        # Weapon rotation
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_rotate_weapon = True
        self.weapon_rotation_time = None
        self.rotate_attack_cooldown = 600

        # Magic rotation
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_swap_magic = True
        self.magic_swap_time = None

        # Stats
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 5
        }
        self.max_stats = {
            'health': 300,
            'energy': 150,
            'attack': 20,
            'magic': 10,
            'speed': 10
        }
        self.upgrade_costs = {
            'health': 100,
            'energy': 100,
            'attack': 100,
            'magic': 100,
            'speed': 100
        }

        # AI setup
        self.is_AI = is_AI
        if self.is_AI:
            self.agent = Agent(self.possible_actions, input_dims=(list(self.stats.values(
            )) + self.distance_direction_to_player), batch_size=batch_size, alpha=alpha, n_epochs=n_epochs)

        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

        # Damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 300

        self.obstacle_sprites = obstacle_sprites

        # Import Sounds
        self.weapon_attack_sound = pygame.mixer.Sound(
            '../Graphics/audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.2)

    def import_player_assets(self):
        character_path = '../Graphics/graphics/player'

        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
        }
        for animation in self.animations.keys():
            full_path = f"{character_path}/{animation}"
            self.animations[animation] = import_folder(full_path)

    def get_status(self):

        # Idle Status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']

        return (base_damage + weapon_damage)

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return (base_damage + spell_damage)

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_costs.values())[index]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time > self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.delete_attack_sprite()

        if not self.can_rotate_weapon:
            if current_time - self.weapon_rotation_time > self.rotate_attack_cooldown:
                self.can_rotate_weapon = True

        if not self.can_swap_magic:
            if current_time - self.magic_swap_time > self.rotate_attack_cooldown:
                self.can_swap_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        if not self.can_move:
            if current_time - self.move_time >= self.move_cooldown:
                self.can_move = True

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
        self.distance_direction_to_player = self.state()
        # if self.is_AI:
        #   self.agent.act(self.distance_direction_to_player)
