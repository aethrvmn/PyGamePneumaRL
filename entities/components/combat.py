from config.game.weapon_config import weapon_data
from config.game.spell_config import magic_data

from effects.magic_effects import MagicPlayer
from effects.particle_effects import AnimationPlayer
from effects.weapon_effects import Weapon




class CombatHandler:

    def __init__(self):

        # Setup Combat
        self.magic_player = MagicPlayer(AnimationPlayer())
        self.current_attack = None

        # Spell and Weapon Rotation
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]

        # Damage Timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 300

    def create_attack_sprite(self):
        self.current_attack = Weapon(
            self, [self.visible_sprites, self.attack_sprites])

    def delete_attack_sprite(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic_sprite(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self, strength, cost, [
                                   self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(
                self, cost, [self.visible_sprites, self.attack_sprites])
