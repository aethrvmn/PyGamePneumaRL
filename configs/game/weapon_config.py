import os

script_dir = os.path.dirname(os.path.abspath(__file__))
asset_path = os.path.join(
    script_dir, '../..', 'assets')

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': f"{asset_path}/graphics/weapons/sword/full.png"},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': f"{asset_path}/graphics/weapons/lance/full.png"},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': f"{asset_path}/graphics/weapons/axe/full.png"},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': f"{asset_path}/graphics/weapons/rapier/full.png"},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': f"{asset_path}/graphics/weapons/sai/full.png"}
}
