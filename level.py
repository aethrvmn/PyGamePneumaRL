import os
import pygame
import numpy as np

from random import choice

from configs.system.window_config import TILESIZE

from utils.debug import debug
from utils.resource_loader import import_csv_layout, import_folder

from interface.ui import UI

from entities.observer import Observer
from entities.player import Player
from entities.enemy import Enemy
from entities.terrain import Terrain

from camera import Camera


class Level:

    def __init__(self, n_players):

        self.paused = False
        self.done = False

        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Setup Sprite groups
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Map generation
        self.n_players = n_players
        self.generate_map()

        # Handle generated entities
        self.get_entities()
        self.get_distance_direction()
        self.dead_players = np.zeros(self.n_players)

        # Setup UI
        self.ui = UI()

    def generate_map(self):

        self.possible_player_locations = []

        player_id = 0

        self.layouts = {
            'boundary': import_csv_layout(os.path.join('map',
                                                       'FloorBlocks.csv')),
            'grass': import_csv_layout(os.path.join('map',
                                                    'Grass.csv')),
            'objects': import_csv_layout(os.path.join('map',
                                                      'Objects.csv')),
            'entities': import_csv_layout(os.path.join('map',
                                                       'Entities.csv'))
        }

        self.graphics = {
            'grass': import_folder(os.path.join('graphics', 'grass')),
            'objects': import_folder(os.path.join('graphics', 'objects'))
        }

        for style, layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if int(col) != -1:

                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        # Generate unpassable terrain
                        if style == 'boundary':

                            if col == '600':
                                self.map_edge = (x, y)

                            elif col != '700':
                                Terrain((x, y),
                                        [self.obstacle_sprites,
                                            self.visible_sprites],
                                        'invisible')
                            elif col == '700' and self.n_players > 1:
                                print(f"Prison set at:{(x, y)}")
                        # Generate grass
                        # if style == 'grass':
                        #     random_grass_image = choice(self.graphics['grass'])
                        #
                        #     Terrain((x, y), [
                        #         self.visible_sprites,
                        #         self.obstacle_sprites,
                        #         self.attackable_sprites
                        #     ],
                        #         'grass',
                        #         random_grass_image)

                        # Generate objects like trees and statues
                        # if style == 'objects':
                        #     surface = self.graphics['objects'][int(col)]
                        #     Terrain((x, y), [
                        #         self.visible_sprites,
                        #         self.obstacle_sprites
                        #     ],
                        #         'object',
                        #         surface)

                        # Generate observer, players and monsters
                        if style == 'entities':

                            # Generate observer
                            if col == '500':
                                self.observer = Observer(
                                    (x, y),
                                    [self.visible_sprites]
                                )

                            # Generate player(s)
                            # TODO: Make a way to generate players in random locations
                            elif col == '400':
                                self.possible_player_locations.append((x, y))
                            # Monster generation

                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                elif col == ' 393':
                                    monster_name = 'squid'
                                Enemy(name=monster_name,
                                      position=(x, y),
                                      groups=[self.visible_sprites,
                                              self.attackable_sprites],
                                      visible_sprites=self.visible_sprites,
                                      obstacle_sprites=self.obstacle_sprites)

        for player_id in range(self.n_players):
            Player(
                player_id,
                'tank',
                choice(self.possible_player_locations),
                self.map_edge,
                [self.visible_sprites],
                self.obstacle_sprites,
                self.visible_sprites,
                self.attack_sprites,
                self.attackable_sprites
            )

    def reset(self):

        for grass in self.grass_sprites:
            grass.kill()

        for enemy in self.enemy_sprites:
            enemy.kill()

        for style, layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if int(col) != -1:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        # # Regenerate grass
                        # if style == 'grass':
                        #     random_grass_image = choice(
                        #         self.graphics['grass'])
                        #
                        #     Terrain((x, y), [
                        #         self.visible_sprites,
                        #         self.obstacle_sprites,
                        #         self.attackable_sprites
                        #     ],
                        #         'grass',
                        #         random_grass_image)

                        if style == 'entities':

                            if col == '500':
                                continue

                            if col == '400':
                                continue

                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                elif col == ' 393':
                                    monster_name = 'squid'

                                Enemy(monster_name,
                                      (x, y),
                                      [self.visible_sprites,
                                       self.attackable_sprites],
                                      self.visible_sprites,
                                      self.obstacle_sprites)

        for player in self.player_sprites:

            player.animation.import_assets(
                choice(self.possible_player_locations))

            player.stats.health\
                = player.stats.stats['health']

            player.stats.energy\
                = player.stats.stats['energy']

            player.stats.exp = 0

        self.get_entities()
        self.get_distance_direction()
        self.dead_players = np.zeros(self.n_players)
        self.done = False

    def get_entities(self):

        self.player_sprites = [sprite
                               for sprite in self.visible_sprites.sprites()
                               if sprite.sprite_type == 'player']

        self.enemy_sprites = [sprite
                              for sprite in self.visible_sprites.sprites()
                              if sprite.sprite_type == 'enemy']

        self.grass_sprites = [sprite
                              for sprite in self.visible_sprites.sprites()
                              if sprite.sprite_type == 'grass']

    def get_distance_direction(self):
        for player in self.player_sprites:
            player.distance_direction_from_enemy = []

        for enemy in self.enemy_sprites:
            enemy.distance_direction_from_player = []

        for player in self.player_sprites:
            if not player.is_dead():
                player_vector = pygame.math.Vector2(
                    player.animation.rect.center
                )

                for enemy in self.enemy_sprites:
                    enemy_vector = pygame.math.Vector2(
                        enemy.animation.rect.center
                    )
                    distance\
                        = (player_vector - enemy_vector).magnitude()

                    if distance > 0:
                        direction\
                            = (player_vector - enemy_vector).normalize()
                    else:
                        direction\
                            = pygame.math.Vector2()

                    enemy.distance_direction_from_player.append(
                        (distance, direction, player))
                    player.distance_direction_from_enemy.append(
                        (distance, -direction, enemy))

    def apply_damage_to_player(self):
        for enemy in self.enemy_sprites:
            for distance, _, player in enemy.distance_direction_from_player:

                if (distance < enemy.stats.attack_radius
                        and player._input.combat.vulnerable):

                    player.stats.health -= enemy.stats.attack
                    player._input.combat.vulnerable = False
                    player._input.combat.hurt_time = pygame.time.get_ticks()

    def toggle_pause(self):
        self.paused = not self.paused

    def run(self, who='observer', fps='v0.9'):
        # Draw the game
        self.visible_sprites.custom_draw(self.observer)
        self.ui.display(self.observer)

        debug(f"{fps}")

        if not self.paused:
            # Update the game
            for player in self.player_sprites:
                if player.stats.health > 0:
                    player.attack_logic()

            self.get_entities()
            self.get_distance_direction()
            self.visible_sprites.update()
            self.apply_damage_to_player()

        else:
            debug('PAUSED')

        for player in self.player_sprites:
            if player.is_dead():
                print(f"\nPlayer {player.player_id} is dead")
                player.stats.exp = -10
                player.update()
                self.dead_players[player.player_id] = player.is_dead()

        self.done = True if (self.dead_players.all() == 1
                             or self.enemy_sprites == []) else False
