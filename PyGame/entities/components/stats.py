from config.game.player_config import warrior_stats, mage_stats,  tank_stats
from config.game.monster_config import monster_data

class StatsHandler:

    def get_stats(self, sprite_type, role=None, monster_name=None):

        if sprite_type == 'player':
            if role == 'warrior':
                self.stats = warrior_stats
            elif role == 'tank':
                self.stats = tank_stats
            elif role == 'mage':
                self.stats = mage_stats
            else:
                self.stats = base_stats

            self.role_id = self.stats['role_id']
            self.health = self.stats['health']
            self.energy = self.stats['energy']
            self.attack = self.stats['attack']
            self.magic = self.stats['magic']
            self.speed = self.stats['speed']
            self.exp = 0

        if sprite_type == 'enemy':
            self.monster_info = monster_data[monster_name]
            self.monster_id = self.monster_info['id']
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

    def health_recovery(self):
        if self.energy < self.stats['health']:
            self.energy += 0.15
        else:
            self.energy = self.stats['energy']

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_costs.values())[index]
