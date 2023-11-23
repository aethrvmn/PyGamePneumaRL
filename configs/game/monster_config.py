import os


script_dir = os.path.dirname(os.path.abspath(__file__))
asset_path = os.path.join(
    script_dir, '../..', 'assets')

monster_data = {
    'squid': {'id': 1, 'health': .1, 'exp': 1, 'attack': .5, 'attack_type': 'slash', 'speed': 3, 'knockback': 20, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'id': 2, 'health': .3, 'exp': 2.5, 'attack': .8, 'attack_type': 'claw',  'speed': 2, 'knockback': 20, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'id': 3, 'health': .1, 'exp': 1.1, 'attack': .6, 'attack_type': 'thunder', 'speed': 4, 'knockback': 20, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'id': 4, 'health': .07, 'exp': 1.2, 'attack': .4, 'attack_type': 'leaf_attack', 'speed': 3, 'knockback': 20, 'attack_radius': 50, 'notice_radius': 300}}
