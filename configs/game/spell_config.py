import os

from utils.resource_loader import import_assets


magic_data = {
    'flame': {'strength': 5, 'cost': .020, 'graphic': import_assets(
        os.path.join('graphics',
                     'particles',
                     'flame',
                     'fire.png')
    )
    },

    'heal': {'strength': 20, 'cost': .010, 'graphic': import_assets(
        os.path.join('graphics',
                     'particles',
                     'heal',
                     'heal.png')
    )
    }
}
