class StatsHandler:

    def __init__(self):
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 5
        }

        self.max_stats = {
            'health': 300,
            'energy': 150,
            'attack': 20,
            'magic': 10,
            'speed': 10
        }

        self.upgrade_costs = {
            'health': 100,
            'energy': 100,
            'attack': 100,
            'magic': 100,
            'speed': 100
        }

        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.attack = self.stats['attack']
        self.magic = self.stats['magic']
        self.speed = self.stats['speed']
        self.exp = 10000

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_costs.values())[index]
