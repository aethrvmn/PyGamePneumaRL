import pygame

from .ui_settings import UI_FONT, UI_FONT_SIZE, TEXT_COLOR, TEXT_COLOR_SELECTED, UPGRADE_BG_COLOR_SELECTED, UI_BORDER_COLOR, UI_BG_COLOR, BAR_COLOR_SELECTED, BAR_COLOR


class Upgrade:

    def __init__(self, player):

        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_num = len(player.stats.stats)
        self.attribute_names = list(player.stats.stats.keys())
        self.max_values = list(player.stats.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Defining upgrade boxes
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[
            0] // (self.attribute_num + 1)
        self.create_boxes()

        # Selection System
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_d]:
                self.selection_index += 1
                if self.selection_index == self.attribute_num:
                    self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_a]:
                self.selection_index -= 1
                if self.selection_index == -1:
                    self.selection_index = self.attribute_num - 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.box_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 150:
                self.can_move = True

    def create_boxes(self):
        self.box_list = []

        for box, index in enumerate(range(self.attribute_num)):

            # Horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_num
            left = (box * increment) + (increment - self.width) // 2

            # Vertical position
            top = self.display_surface.get_size()[1] * 0.1

            box = Box(left, top, self.width, self.height, index, self.font)
            self.box_list.append(box)

    def display(self):

        self.input()
        self.selection_cooldown()

        for index, box in enumerate(self.box_list):
            # Get attributes
            name = self.attribute_names[index]
            value = self.player.stats.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.stats.get_cost_by_index(index)
            box.display(self.display_surface, self.selection_index,
                        name, value, max_value, cost)


class Box:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # Title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(
            midtop=self.rect.midtop + pygame.math.Vector2(0, 20))
        # Cost
        cost_surf = self.font.render(f'Cost: {int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(
            midbottom=self.rect.midbottom + - pygame.math.Vector2(0, 20))

        # Draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):

        # Line setup
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # Bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(
            top[0] - 15, bottom[1] - relative_number, 30, 10)

        # Draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.stats.keys())[self.index]

        if player.stats.exp >= player.stats.upgrade_costs[upgrade_attribute] and player.stats.stats[upgrade_attribute] < player.stats.max_stats[upgrade_attribute]:
            player.stats.exp -= player.stats.upgrade_costs[upgrade_attribute]
            player.stats.stats[upgrade_attribute] *= 1.2
            player.stats.upgrade_costs[upgrade_attribute] *= 1.4

        if player.stats.stats[upgrade_attribute] > player.stats.max_stats[upgrade_attribute]:
            player.stats.stats[upgrade_attribute] = player.stats.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value,
                         self.index == selection_num)
