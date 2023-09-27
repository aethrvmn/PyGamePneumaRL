import pygame
from random import choice, randint

from utils.settings import *
from utils.debug import debug
from utils.support import *

from UI.ui import UI
from UI.upgrade import Upgrade

from effects.particles import AnimationPlayer
from effects.magic import MagicPlayer
from effects.weapon import Weapon

from objects.tile import Tile
from objects.player import Player
from objects.enemy import Enemy
from objects.camera import Camera


class Level:

    def __init__(self):

        # General Settings
        self.game_paused = False

        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite Group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Combat Sprite setup
        self.current_attack = None

        # Sprite setup
        self.create_map()

        # UI setup
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # Particle setup
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../Graphics/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../Graphics/map/map_Grass.csv'),
            'objects': import_csv_layout('../Graphics/map/map_Objects.csv'),
            'entities': import_csv_layout('../Graphics/map/map_Entities.csv')
        }

        graphics = {
            'grass': import_folder('../Graphics/graphics/grass'),
            'objects': import_folder('../Graphics/graphics/objects')
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

                        # The numbers represent their IDs in the map .csv files generated from TILED.
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack_sprite,
                                                     self.delete_attack_sprite, self.create_magic_sprite, is_AI=True, state=self.get_state)

                            elif col == '395':
                                self.camera = Camera(
                                    (x, y), [self.visible_sprites])

                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'

                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                                      self.damage_player, self.trigger_death_particles, self.add_exp, is_AI=False, state=None)

    def create_attack_sprite(self):
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites])

    def delete_attack_sprite(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic_sprite(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [
                                   self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(
                self.player, cost, [self.visible_sprites, self.attack_sprites])

    def player_attack_logic(self):
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
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type)

    def get_state(self):
        state = []

        enemy_sprites = [sprite for sprite in self.visible_sprites if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            distance, direction = enemy.get_player_distance_direction(
                self.player)
            state.append([(distance, direction.x, direction.y, enemy.monster_name, enemy.health, enemy.exp, enemy.speed,
                         enemy.attack_damage, enemy.resistance, enemy.attack_radius, enemy.notice_radius, enemy.attack_type)])

        # Sort by distance
        state = sorted(state, key=lambda x: x[0])

        # Consider only the closest 5 enemies
        state = state[:5]

        # If there are fewer than 5 enemies, pad the state with placeholder values
        while len(state) < 5:
            state.append((float('inf'), 0, 0, None, None, None,
                         None, None, None, None, None, None))

        # Flatten the state to be a single list of numbers and strings
        state = [item for sublist in state for item in sublist]

        return state

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            if self.player.health < 0:
                self.player.health = 0
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.generate_particles(
                attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, position, particle_type):
        self.animation_player.generate_particles(
            particle_type, position, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        # Draw the game
        self.visible_sprites.custom_draw(self.camera)
        self.ui.display(self.camera)
        if self.game_paused:
            if self.visible_sprites.sprite_type == 'player':
                self.upgrade.display()
                pass
        else:
            # Update the game
            self.player.distance_direction_to_player = self.get_state()
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

            if self.player.health <= 0:
                self.__init__()
