import os
import pygame

from random import choice

from configs.system.window_config import TILESIZE

from utils.debug import debug
from utils.resource_loader import import_csv_layout, import_folder

from interface.ui import UI
from interface.upgrade import Upgrade

from entities.observer import Observer
from entities.player import Player
from entities.enemy import Enemy

from .terrain import Tile
from .camera import Camera


class Level:

    def __init__(self):

        # General Settings
        self.game_paused = False

        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite Group setup
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Sprite setup and entity generation
        self.create_map()

        # UI setup
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        self.get_players_enemies()
        self.get_distance_direction()

    def create_map(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(
            script_dir, '../..', 'assets')
        layouts = {
            'boundary': import_csv_layout(f"{asset_path}/map/FloorBlocks.csv"),
            'grass': import_csv_layout(f"{asset_path}/map/Grass.csv"),
            'objects': import_csv_layout(f"{asset_path}/map/Objects.csv"),
            'entities': import_csv_layout(f"{asset_path}/map/Entities.csv")
        }

        graphics = {
            'grass': import_folder(f"{asset_path}/graphics/grass"),
            'objects': import_folder(f"{asset_path}/graphics/objects")
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites,
                                 self.attackable_sprites], 'grass', random_grass_image)

                        if style == 'objects':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            # The numbers represent their IDs in .csv files generated from TILED.
                            if col == '395':
                                self.observer = Observer(
                                    (x, y), [self.visible_sprites])

                            elif col == '394':
                                # Player Generation
                                self.player = Player(
                                    (x, y), [self.visible_sprites], self.obstacle_sprites, self.visible_sprites, self.attack_sprites, self.attackable_sprites)

                            else:
                                # Monster Generation
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'

                                Enemy(monster_name, (x, y), [
                                      self.visible_sprites, self.attackable_sprites], self.visible_sprites, self.obstacle_sprites)

    def get_players_enemies(self):
        self.player_sprites = [sprite for sprite in self.visible_sprites.sprites(
        ) if hasattr(sprite, 'sprite_type') and sprite.sprite_type in ('player')]

        self.enemy_sprites = [sprite for sprite in self.visible_sprites.sprites(
        ) if hasattr(sprite, 'sprite_type') and sprite.sprite_type in ('enemy')]

    def get_distance_direction(self):
        for player in self.player_sprites:
            player.distance_direction_from_enemy = []

        for enemy in self.enemy_sprites:
            enemy.distance_direction_from_player = []

        for player in self.player_sprites:
            player_vector = pygame.math.Vector2(player.rect.center)
            for enemy in self.enemy_sprites:
                enemy_vector = pygame.math.Vector2(enemy.rect.center)
                distance = (player_vector - enemy_vector).magnitude()

                if distance > 0:
                    direction = (player_vector - enemy_vector).normalize()
                else:
                    direction = pygame.math.Vector2()

                enemy.distance_direction_from_player.append(
                    (distance, direction, player))
                player.distance_direction_from_enemy.append(
                    (distance, -direction, enemy))

    def apply_damage_to_player(self):
        for enemy in self.enemy_sprites:
            for distance, _, player in enemy.distance_direction_from_player:
                if distance < enemy.stats.attack_radius and player._input.combat.vulnerable:
                    player.stats.health -= enemy.stats.attack
                    player._input.combat.vulnerable = False
                    player._input.combat.hurt_time = pygame.time.get_ticks()

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self, who='observer'):
        # Draw the game
        if who == 'observer':
            self.visible_sprites.custom_draw(self.observer)
            self.ui.display(self.observer)
        elif who == 'player':
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
        debug('v0.5')
        if not self.game_paused:
            # Update the game
            for player in self.player_sprites:
                player.attack_logic()

            self.get_players_enemies()
            self.get_distance_direction()
            self.apply_damage_to_player()
            self.visible_sprites.update()

            # self.visible_sprites.enemy_update(self.player)
            # self.player_attack_logic()
        else:
            self.upgrade.display()

        if self.player.stats.health <= 0:
            self.__init__()
