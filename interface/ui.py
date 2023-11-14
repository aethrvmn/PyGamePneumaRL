import pygame

from configs.game.weapon_config import *
from configs.game.spell_config import *

from .ui_settings import *


class UI:
    def __init__(self):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(
            script_dir, '../..', 'assets')

        # General info
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # Convert weapon dictionary
        self.magic_graphics = []
        for spell in magic_data.values():
            path = spell['graphic']
            spell = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(spell)

    def show_bar(self, current_amount, max_amount, bg_rect, color):

        # Draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Convert stat amount to pixels
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Draw stat bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 4)

    def show_exp(self, exp):
        if exp >= 0:
            text_surf = self.font.render(
                f"EXP: {str(int(exp))}", False, TEXT_COLOR)
            x = self.display_surface.get_size()[0] - 20
            y = self.display_surface.get_size()[1] - 20
            text_rect = text_surf.get_rect(bottomright=(x, y))

            pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                             text_rect.inflate(10, 10))
            self.display_surface.blit(text_surf, text_rect)
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR, text_rect.inflate(10, 10), 4)
        else:
            text_surf = self.font.render(f"OBSERVER", False, TEXT_COLOR)
            x = self.display_surface.get_size()[0] - 20
            y = self.display_surface.get_size()[1] - 20
            text_rect = text_surf.get_rect(bottomright=(x, y))

            pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                             text_rect.inflate(10, 10))
            self.display_surface.blit(text_surf, text_rect)
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR, text_rect.inflate(10, 10), 4)

    def selection_box(self, left, top, has_rotated):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if not has_rotated:
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR_ACTIVE, bg_rect, 4)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 4)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_rotated):
        bg_rect = self.selection_box(10, 630, has_rotated)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_swaped):
        bg_rect = self.selection_box(100, 630, has_swaped)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        if player.sprite_type == 'player':
            self.show_bar(
                player.stats.health, player.stats.stats['health'], self.health_bar_rect, HEALTH_COLOR)
            self.show_bar(
                player.stats.energy, player.stats.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
            self.show_exp(player.stats.exp)
            self.weapon_overlay(player._input.combat.weapon_index,
                                player._input.can_rotate_weapon)
            self.magic_overlay(player._input.combat.magic_index,
                               player._input.can_swap_magic)
        if player.sprite_type == 'camera':
            self.show_exp(player.exp)
