import os
import pygame

from random import choice, randint

from configs.game.spell_config import magic_data
from configs.game.weapon_config import weapon_data
from configs.game.monster_config import monster_data
from configs.system.window_config import TILESIZE

from utils.debug import debug
from utils.resource_loader import import_csv_layout, import_folder

from interface.ui import UI
from interface.upgrade import Upgrade

from effects.magic_effects import MagicPlayer
from effects.particle_effects import AnimationPlayer
from effects.weapon_effects import Weapon

from entities.observer import Observer
from entities.player import Player

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
                                    (x, y), [self.visible_sprites], self.obstacle_sprites, self.visible_sprites, self.attack_sprites)

                            else:
                                pass
                                # monster generation

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        # Draw the game
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        debug(self.player.status)
        if not self.game_paused:
            # Update the game
            # self.player.distance_direction_to_player = self.get_state()
            self.visible_sprites.update()
            # self.visible_sprites.enemy_update(self.player)
            # self.player_attack_logic()
        else:
            if self.visible_sprites.sprite_type == 'player':
                self.upgrade.display()

        if self.player.stats.health <= 0:
            self.__init__()
