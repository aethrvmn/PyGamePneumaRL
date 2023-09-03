import pygame
from random import choice, randint

from utils.settings import *
from utils.debug import debug
from utils.support import *

from UI.ui import UI

from effects.particles import AnimationPlayer
from effects.magic import MagicPlayer
from effects.weapon import Weapon

from terrain.tiles import Tile

from view.observer import Observer
from view.camera import Camera

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

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../Map/FloorBlocks.csv'),
            'grass': import_csv_layout('../Map/Grass.csv'),
            'objects': import_csv_layout('../Map/Objects.csv'),
            'entities': import_csv_layout('../Map/Entities.csv')
        }

        graphics = {
            'grass': import_folder('../Graphics/grass'),
            'objects': import_folder('../Graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')

                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass', random_grass_image)

                        if style == 'objects':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            # The numbers represent their IDs in the map .csv files generated from TILED.
                            if col == '395':
                                self.observer = Observer((x,y), [self.visible_sprites])

                            elif col == '394':
                                pass
                                #player generation

                            else:
                                pass
                                #monster generation

    def create_attack_sprite(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def delete_attack_sprite(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic_sprite(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def run(self):
        # Draw the game
        self.visible_sprites.custom_draw(self.observer)
        self.ui.display(self.observer)

