import os
import pygame

from utils.resource_loader import import_folder
from random import choice


class AnimationPlayer:
    def __init__(self):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(
            script_dir, '..', 'assets')

        self.frames = {
            # magic
            'flame': import_folder(f'{asset_path}/graphics/particles/flame/frames'),
            'aura': import_folder(f'{asset_path}/graphics/particles/aura'),
            'heal': import_folder(f'{asset_path}/graphics/particles/heal/frames'),

            # attacks
            'claw': import_folder(f'{asset_path}/graphics/particles/claw'),
            'slash': import_folder(f'{asset_path}/graphics/particles/slash'),
            'sparkle': import_folder(f'{asset_path}/graphics/particles/sparkle'),
            'leaf_attack': import_folder(f'{asset_path}/graphics/particles/leaf_attack'),
            'thunder': import_folder(f'{asset_path}/graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder(f'{asset_path}/graphics/particles/smoke_orange'),
            'raccoon': import_folder(f'{asset_path}/graphics/particles/raccoon'),
            'spirit': import_folder(f'{asset_path}/graphics/particles/nova'),
            'bamboo': import_folder(f'{asset_path}/graphics/particles/bamboo'),

            # leafs
            'leaf': (
                import_folder(f'{asset_path}/graphics/particles/leaf1'),
                import_folder(f'{asset_path}/graphics/particles/leaf2'),
                import_folder(f'{asset_path}/graphics/particles/leaf3'),
                import_folder(f'{asset_path}/graphics/particles/leaf4'),
                import_folder(f'{asset_path}/graphics/particles/leaf5'),
                import_folder(f'{asset_path}/graphics/particles/leaf6'),
                self.reflect_images(import_folder(
                    f'{asset_path}/graphics/particles/leaf1')),
                self.reflect_images(import_folder(
                    f'{asset_path}/graphics/particles/leaf2')),
                self.reflect_images(import_folder(
                    f'{asset_path}/graphics/particles/leaf3')),
                self.reflect_images(import_folder(
                    f'{asset_path}/graphics/particles/leaf4')),
                self.reflect_images(import_folder(
                    f'{asset_path}/graphics/particles/leaf5')),
                self.reflect_images(import_folder(
                    f'{asset_path}/graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, position, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(position, animation_frames, groups)

    def generate_particles(self, animation_type, position, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(position, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=position)
        self.sprite_type = 'magic'

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
