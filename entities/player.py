import pygame
import numpy as np
from random import randint

from configs.game.weapon_config import weapon_data
from configs.game.spell_config import magic_data

from .components.stats import StatsHandler
from .components._input import InputHandler
from .components.animaton import AnimationHandler

from effects.particle_effects import AnimationPlayer

from agents.ppo.agent import Agent


class Player(pygame.sprite.Sprite):

    def __init__(self, position, groups, obstacle_sprites, visible_sprites, attack_sprites, attackable_sprites, role, player_id):
        super().__init__(groups)

        # Setup Sprites
        self.sprite_type = 'player'
        self.status = 'down'
        self.player_id = player_id
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

        # Setup AI
        self.score = 0
        self.learn_iters = 0
        self.n_steps = 0
        self.N = 20

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

    def get_current_state(self):

        if self.distance_direction_from_enemy != []:
            sorted_distances = sorted(
                self.distance_direction_from_enemy, key=lambda x: x[0])
        else:
            sorted_distances = np.zeros(self.num_features)

        nearest_dist, _, nearest_enemy = sorted_distances[0]

        self.action_features = [self._input.action]

        self.reward_features = [self.stats.exp,
                                np.exp(-(nearest_dist)),
                                np.exp(-(nearest_enemy.stats.health)),
                                - np.exp(self.stats.health)
                                ]

        self.state_features = [
            self.rect.center[0],
            self.rect.center[1],
            self.stats.health,
            self.stats.energy,
            self.stats.attack,
            self.stats.magic,
            self.stats.speed
        ]

        enemy_states = []

        for distance, direction, enemy in sorted_distances[:5]:

            enemy_states.extend([
                distance,
                direction[0],
                direction[1],
                enemy.stats.health,
                enemy.stats.attack,
                enemy.stats.speed,
                enemy.stats.exp,
                enemy.stats.attack_radius,
                enemy.stats.notice_radius
            ])

        self.state_features.extend(enemy_states)

        if hasattr(self, 'num_features'):
            while len(self.state_features) < self.num_features:
                self.state_features.append(0)

        self.state_features = np.array(self.state_features)
        min_feat = np.min(self.state_features)
        max_feat = np.max(self.state_features)
        self.state_features = (self.state_features -
                               min_feat) / (max_feat-min_feat)

    def get_max_num_states(self):
        self.get_current_state()
        self.num_features = len(self.state_features)

    def setup_agent(self):
        self.agent = Agent(
            input_dims=len(self.state_features),
            n_actions=len(self._input.possible_actions),
            batch_size=5,
            n_epochs=4)
        try:
            self.agent.load_models()
        except FileNotFoundError as e:
            print(f"{e}. Skipping loading...")

    def is_dead(self):
        if self.stats.health == 0:
            self.stats.exp = -100
            return True
        else:
            return False

    def update(self):

        # Get the current state
        self.get_current_state()

        # Choose action based on current state
        action, probs, value = self.agent.choose_action(self.state_features)

        self.n_steps += 1
        # Apply chosen action
        self._input.check_input(action,
                                self.stats.speed,
                                self.animation.hitbox,
                                self.obstacle_sprites,
                                self.animation.rect,
                                self)

        self.done = self.is_dead()

        self.score = self.stats.exp
        self.agent.remember(self.state_features, action,
                            probs, value, self.stats.exp, self.done)

        if self.n_steps % self.N == 0:
            self.agent.learn()
            self.learn_iters += 1

        self.get_current_state()

        if self.done:
            self.agent.learn()

        # Refresh objects based on input
        self.status = self._input.status

        # Animate
        self.get_status()
        self.animation.animate(self.status, self._input.combat.vulnerable)
        self.image = self.animation.image
        self.rect = self.animation.rect

        # Cooldowns and Regen
        self.stats.energy_recovery()
        self._input.cooldowns(self._input.combat.vulnerable)
