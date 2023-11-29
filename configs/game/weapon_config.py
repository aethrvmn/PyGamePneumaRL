import os

from utils.resource_loader import import_assets


weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': import_assets(
        os.path.join('graphics',
                     'weapons',
                     'sword',
                     'full.png')
    )
    },

    'lance': {'cooldown': 400, 'damage': 30, 'graphic': import_assets(
        os.path.join('graphics',
                     'weapons',
                     'lance',
                     'full.png')
    )
    },
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': import_assets(
        os.path.join('graphics',
                     'weapons',
                     'axe',
                     'full.png')
    )
    },
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': import_assets(
        os.path.join('graphics',
                     'weapons',
                     'rapier',
                     'full.png')
    )
    },
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': import_assets(
        os.path.join('graphics',
                     'weapons',
                     'sai',
                     'full.png')
    )
    },
}
