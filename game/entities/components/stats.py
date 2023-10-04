from configs.game.player_config import stats, max_stats, upgrade_costs
from configs.game.monster_config import monster_data


class StatsHandler:

    def __init__(self, sprite_type, monster_name=None):

        if sprite_type == 'player':

            self.stats = stats

            self.max_stats = max_stats

            self.upgrade_costs = upgrade_costs

            self.health = self.stats['health']
            self.energy = self.stats['energy']
            self.attack = self.stats['attack']
            self.magic = self.stats['magic']
            self.speed = self.stats['speed']
            self.exp = 10000

        if sprite_type == 'enemy':

            self.monster_info = monster_data[monster_name]
            self.health = self.monster_info['health']
            self.attack = self.monster_info['attack']
            self.attack_type = self.monster_info['attack_type']
            self.attack_radius = self.monster_info['attack_radius']
            self.speed = self.monster_info['speed']
            self.knockback = self.monster_info['knockback']
            self.notice_radius = self.monster_info['notice_radius']
            self.exp = self.monster_info['exp']

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.magic
        else:
            self.energy = self.stats['energy']

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_costs.values())[index]
