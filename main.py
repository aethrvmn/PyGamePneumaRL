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

        self.level = Level(self.extract_features,
                           self.convert_features_to_tensor)

        # Sound
        main_sound = pygame.mixer.Sound('assets/audio/main.ogg')
        main_sound.set_volume(0.4)
        main_sound.play(loops=-1)

    def extract_features(self):
        self.state_features = []
        self.reward_features = []
        self.action_features = []
        self.features = []

        for i, player in enumerate(self.level.player_sprites):

            player_action_features = {
                "player_id": player.player_id,
                "player_action": player._input.action
            }

            player_reward_features = {
                "player_id": player.player_id,
                "player_exp": player.stats.exp
            }

            player_state_features = {
                "player_id": player.player_id,
                "player_position": player.rect.center,
                "player role": player.stats.role_id,
                "player_health": player.stats.health,
                "player_energy": player.stats.energy,
                "player_attack": player.stats.attack,
                "player_magic": player.stats.magic,
                "player_speed": player.stats.speed,
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

                player_state_features["enemies"] = distances_directions
            self.reward_features.append(player_reward_features)
            self.state_features.append(player_state_features)
            self.action_features.append(player_action_features)

    def convert_features_to_tensor(self):

        for features in self.state_features:
            info_array = []

            # Adding player features to tensor
            player_info = [
                features['player_position'][0],
                features['player_position'][1],
                features['player role'],
                features['player_health'],
                features['player_energy'],
                features['player_attack'],
                features['player_magic'],
                features['player_speed'],
                features['player_vulnerable'],
                features['player_can_move'],
                features['player_attacking'],
                features['player_can_rotate_weapon'],
                features['playercan_swap_magic'],
            ]
            info_array.extend(player_info)

            # Adding enemy features per player
            for enemy in features['enemies']:
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

            state_tensor = torch.tensor(
                np.array(info_array, dtype=np.float32))

            for player in self.level.player_sprites:
                if player.player_id == features["player_id"]:
                    player.state_tensor = state_tensor

        for features in self.action_features:
            info_array = []

            # Adding action features
            action_info = [
                features["player_action"]
            ]

            action_tensor = torch.tensor(
                np.array(action_info, dtype=np.float32))

            for player in self.level.player_sprites:
                if player.player_id == features["player_id"]:
                    player.action_tensor = action_tensor

        for features in self.reward_features:
            info_array = []

            # Adding reward features
            reward_info = [
                features["player_exp"]
            ]

            reward_tensor = torch.tensor(
                np.array(reward_info, dtype=np.float32))

            for player in self.level.player_sprites:
                if player.player_id == features["player_id"]:
                    player.reward_tensor = reward_tensor

    def run(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.level.toggle_menu()

        self.screen.fill(WATER_COLOR)

        self.level.run(who='observer')

        pygame.display.update()
        self.clock.tick(FPS)


if __name__ == '__main__':

    game = Game()
    for i in range(0, 10000):
        game.run()
        print(i)
