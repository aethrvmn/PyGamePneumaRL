from effects.weapon_effects import Weapon
from effects.magic_effects import MagicPlayer

from config.game.weapon_config import weapon_data
from config.game.spell_config import magic_data


class CombatHandler:

    def __init__(self, animation_player):

        self.animation_player = animation_player

        # Setup Combat
        self.magic_player = MagicPlayer(animation_player)
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

    def create_attack_sprite(self, player):
        self.current_attack = Weapon(
            player, [player.visible_sprites, player.attack_sprites])

    def delete_attack_sprite(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic_sprite(self, player, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(player, strength, cost, [
                                   player.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(
                player, cost, [player.visible_sprites, player.attack_sprites])
