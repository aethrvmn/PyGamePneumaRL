import os
import pygame

from configs.game.monster_config import monster_data


class AudioHandler:

    def __init__(self, sprite_type, monster_name=None):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(
            script_dir, '../..', 'assets', 'audio')

        if sprite_type == 'player':
            pass

        elif sprite_type == 'enemy':

            # Sounds
            self.attack_sound = pygame.mixer.Sound(
                monster_data[monster_name]['attack_sound'])
            self.death_sound = pygame.mixer.Sound(
                f'{asset_path}/death.wav')
            self.hit_sound = pygame.mixer.Sound(f'{asset_path}/hit.wav')
            self.death_sound.set_volume(0)
            self.hit_sound.set_volume(0)
            self.attack_sound.set_volume(0)
