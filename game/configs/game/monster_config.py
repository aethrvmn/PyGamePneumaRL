import os


script_dir = os.path.dirname(os.path.abspath(__file__))
asset_path = os.path.join(
    script_dir, '../../..', 'assets')

monster_data = {
    'squid': {'id': 1, 'health': 100, 'exp': 100, 'attack': 20, 'attack_type': 'slash', 'attack_sound': f'{asset_path}/audio/attack/slash.wav', 'speed': 3, 'knockback': 20, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'id': 2, 'health': 300, 'exp': 250, 'attack': 40, 'attack_type': 'claw',  'attack_sound': f'{asset_path}/audio/attack/claw.wav', 'speed': 2, 'knockback': 20, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'id': 3, 'health': 100, 'exp': 110, 'attack': 8, 'attack_type': 'thunder', 'attack_sound': f'{asset_path}/audio/attack/fireball.wav', 'speed': 4, 'knockback': 20, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'id': 4, 'health': 70, 'exp': 120, 'attack': 6, 'attack_type': 'leaf_attack', 'attack_sound': f'{asset_path}/audio/attack/slash.wav', 'speed': 3, 'knockback': 20, 'attack_radius': 50, 'notice_radius': 300}}
