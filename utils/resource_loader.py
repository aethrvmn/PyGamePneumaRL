import pygame
from csv import reader
import os


def import_csv_layout(path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir,
                        '..',
                        'assets',
                        path)
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map


def import_folder(path):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    path = os.path.join(script_dir,
                        '..',
                        'assets',
                        path)
    surface_list = []

    for _, __, img_files in os.walk(path):
        for image in img_files:
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()

            surface_list.append(image_surf)
    return surface_list


def import_assets(path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir,
                        '..',
                        'assets', path)
