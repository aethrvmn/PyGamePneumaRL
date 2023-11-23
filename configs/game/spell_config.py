import os

script_dir = os.path.dirname(os.path.abspath(__file__))
asset_path = os.path.join(
    script_dir, '../..', 'assets')

magic_data = {
    'flame': {'strength': 5, 'cost': .020, 'graphic': f"{asset_path}/graphics/particles/flame/fire.png"},
    'heal': {'strength': 20, 'cost': .010, 'graphic': f"{asset_path}/graphics/particles/heal/heal.png"}}
