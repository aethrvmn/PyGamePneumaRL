import sys
import numpy as np
import torch
import pygame

from configs.system.window_config import WIDTH, HEIGHT, WATER_COLOR, FPS

from level.level import Level


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT))
        pygame.display.set_caption('Pneuma')
        self.clock = pygame.time.Clock()

        self.level = Level()

        # Sound
        main_sound = pygame.mixer.Sound('../assets/audio/main.ogg')
        main_sound.set_volume(0.4)
        main_sound.play(loops=-1)

    def extract_features(self):
        self.features = []
        for i, player in enumerate(self.level.player_sprites):

            player_features = {
                "player_position": player.rect.center,
                "player role": player.stats.role_id,
                "player_health": player.stats.health,
                "player_energy": player.stats.energy,
                "player_attack": player.stats.attack,
                "player_magic": player.stats.magic,
                "player_speed": player.stats.speed,
                "player_exp": player.stats.exp,
                "player_vulnerable": int(player._input.combat.vulnerable),
                "player_can_move": int(player._input.can_move),
                "player_attacking": int(player._input.attacking),
                "player_can_rotate_weapon": int(player._input.can_rotate_weapon),
                "playercan_swap_magic": int(player._input.can_swap_magic)
            }

            distances_directions = []

            for distance, direction, enemy in player.distance_direction_from_enemy:
                distances_directions.append({
                    "enemy_id": enemy.stats.monster_id,
                    "enemy_status": 0 if enemy.animation.status == "idle" else (1 if enemy.animation.status == "move" else 2),
                    "enemy_health": enemy.stats.health,
                    "enemy_attack": enemy.stats.attack,
                    "enemy_speed": enemy.stats.speed,
                    "enemy_attack_radius": enemy.stats.attack_radius,
                    "enemy_notice_radius": enemy.stats.notice_radius,
                    "enemy_exp": enemy.stats.exp,
                    "enemy_distance": distance,
                    "enemy_direction": direction
                })

                player_features["enemies"] = distances_directions
            self.features.append(player_features)

    def convert_features_to_tensor(self):

        self.tensors = []
        for player_features in self.features:
            info_array = []

            # Adding player features to tensor
            player_info = [
                player_features['player_position'][0],
                player_features['player_position'][1],
                player_features['player role'],
                player_features['player_health'],
                player_features['player_energy'],
                player_features['player_attack'],
                player_features['player_magic'],
                player_features['player_speed'],
                player_features['player_exp'],
                player_features['player_vulnerable'],
                player_features['player_can_move'],
                player_features['player_attacking'],
                player_features['player_can_rotate_weapon'],
                player_features['playercan_swap_magic'],
            ]
            info_array.extend(player_info)

            for enemy in player_features['enemies']:
                enemy_info = [
                    enemy['enemy_id'],
                    enemy['enemy_status'],
                    enemy['enemy_health'],
                    enemy['enemy_attack'],
                    enemy['enemy_speed'],
                    enemy['enemy_attack_radius'],
                    enemy['enemy_notice_radius'],
                    enemy['enemy_exp'],
                    enemy['enemy_distance'],
                    enemy['enemy_direction'][0],
                    enemy['enemy_direction'][1]
                ]
                info_array.extend(enemy_info)

            player_tensor = torch.tensor(
                np.array(info_array, dtype=np.float32))
            self.tensors.append(player_tensor)

    def run(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.level.toggle_menu()

        self.screen.fill(WATER_COLOR)

        self.extract_features()
        self.convert_features_to_tensor()

        self.level.run('observer')
        pygame.display.update()
        self.clock.tick(FPS)


if __name__ == '__main__':

    game = Game()
    for _ in range(0, 10000):
        game.run()
        game.extract_features()
        game.convert_features_to_tensor()
