import pygame
import numpy as np
from random import randint

from config.game.weapon_config import weapon_data
from config.game.spell_config import magic_data

from .components.stats import StatsHandler
from .components._input import InputHandler
from .components.animation import AnimationHandler

from effects.particle_effects import AnimationPlayer

from ml.ppo.agent import Agent


class Player(pygame.sprite.Sprite):
    def __init__(self,
                 player_id,
                 role,
                 position,
                 map_edge,
                 groups,
                 obstacle_sprites,
                 visible_sprites,
                 attack_sprites,
                 attackable_sprites
                 ):
        super().__init__(groups)

        self.initial_position = position
        self.map_edge = map_edge
        self.player_id = player_id
        self.distance_direction_from_enemy = None

        # Sprite Setup
        self.sprite_type = "player"
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites
        self.attack_sprites = attack_sprites
        self.attackable_sprites = attackable_sprites

        # Graphics Setup
        self.animation_player = AnimationPlayer()
        self.animation = AnimationHandler(self.sprite_type)
        self.animation.import_assets(position)
        # Input Setup
        self._input = InputHandler(
            self.sprite_type, self.animation_player)

        # Setup Stats
        self.role = role
        self.stats = StatsHandler(self.sprite_type, self.role)

    def setup_agent(self,
                    gamma,
                    alpha,
                    policy_clip,
                    batch_size,
                    n_epochs,
                    gae_lambda,
                    chkpt_dir,
                    entropy_coef,
                    load=None):

        self.max_num_enemies = len(self.distance_direction_from_enemy)
        self.get_current_state()
        self.num_features = len(self.state_features)

        self.agent = Agent(
            input_dims=self.num_features,
            n_actions=len(self._input.possible_actions),
            gamma=gamma,
            alpha=alpha,
            policy_clip=policy_clip,
            batch_size=batch_size,
            n_epochs=n_epochs,
            gae_lambda=gae_lambda,
            entropy_coef=entropy_coef,
            chkpt_dir=chkpt_dir
        )
        print(
            f"\nAgent initialized on player {self.player_id} using {self.agent.actor.device}.")

        if load:
            print("Attempting to load models ...")
            try:
                self.agent.load_models(
                    actr_chkpt=f"{chkpt_dir}/../run{load}/A{self.player_id}",
                    crtc_chkpt=f"{chkpt_dir}/../run{load}/C{self.player_id}"
                )
                print("Models loaded ...\n")

            except FileNotFoundError:
                print(
                    f"FileNotFound for player {self.player_id}.\
                    \nSkipping loading ...\n")

    def get_status(self):
        if self._input.movement.direction.x == 0\
                and self._input.movement.direction.y == 0:

            if 'idle' not in self._input.status and 'attack' not in self._input.status:
                self._input.status += '_idle'

        if self._input.attacking:
            self._input.movement.direction.x = 0
            self._input.movement.direction.y = 0
            if 'attack' not in self._input.status:
                if 'idle' in self._input.status:
                    self._input.status = self._input.status.replace(
                        'idle', 'attack')
                else:
                    self._input.status += '_attack'
        else:
            if 'attack' in self._input.status:
                self._input.status = self._input.status.replace('_attack', '')

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
                                    position=pos - offset,
                                    groups=[self.visible_sprites])

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

        nearest_dist, nearest_en_dir, nearest_enemy = sorted_distances[0]

        self.action_features = [self._input.action]
        if hasattr(self, 'state_features'):
            self.old_state_features = self.state_features

            self.reward = self.stats.exp\
                + self.stats.health/self.stats.stats['health'] - 1
                # - nearest_dist/np.sqrt(np.sum(self.map_edge))

        self.state_features = [
            self.animation.rect.center[0]/self.map_edge[0],
            self.animation.rect.center[1]/self.map_edge[1],
            self._input.movement.direction.x,
            self._input.movement.direction.y,
            self.stats.health/self.stats.stats['health'],
            self.stats.energy/self.stats.stats['energy'],
        ]

        # self.state_features.extend([
        #     nearest_dist/np.sqrt(np.sum(self.map_edge)),
        #     nearest_en_dir[0],
        #     nearest_en_dir[1],
        #     nearest_enemy.stats.exp
        # ])

         for distance, direction, enemy in sorted_distances[:5]:
             self.state_features.extend([
        
                 distance/np.sqrt(np.sum(self.map_edge)),
        
                 direction[0],
        
                 direction[1],
        
                 enemy.stats.health /
                 enemy.stats.monster_info['health'],
        
                 enemy.stats.exp,
             ])

        if hasattr(self, 'num_features'):
            while len(self.state_features) < self.num_features:
                self.state_features.append(0)

        self.state_features = np.array(self.state_features)

    def is_dead(self):
        if self.stats.health <= 0:
            self.stats.health = 0
            self.animation.import_assets((3264, 448))
            return True
        else:
            return False

    def agent_update(self):

        # Get the current state
        self.get_current_state()

        # Choose action based on current state
        action, probs, value\
            = self.agent.choose_action(self.state_features)

        # Apply chosen action
        self._input.check_input(action,
                                self.stats.speed,
                                self.animation.hitbox,
                                self.obstacle_sprites,
                                self.animation.rect,
                                self)

        self.agent.remember(self.state_features, action,
                            probs, value, self.reward, self.is_dead())

        self.get_current_state()

    def update(self):

        self.agent_update()

        # Cooldowns and Regen
        self.stats.health_recovery()
        self.stats.energy_recovery()

        # Refresh player based on input and animate
        self.get_status()
        self.animation.animate(
            self._input.status, self._input.combat.vulnerable)
        self._input.cooldowns(self._input.combat.vulnerable)
