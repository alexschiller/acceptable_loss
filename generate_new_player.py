from data import plasmaslinger_class

def generate_new_player(player_name='Jimbob', player_class=plasmaslinger_class):
    return {
    'name': player_name,
    'class': plasmaslinger_class,
    'level': 1,
    'foo': [0, 0, 0, 50],
    'pow': [0, 0, 0, 50],
    'eng': [0, 0, 0, 50],
    'sci': [0, 0, 0, 50],
    'mon': [0, 0, 0, 50],

    'ability_levels': {
        'plasma': {
            'plasma_infusion': 1,
            'ace_in_the_hole': 0,
            'plasma_painter': 0,
            'plasma_shield': 0,
            'melt_armor': 0,
            'bright_lights': 0,
            'meltdown': 0,
        },
        'magnum': {
            'double_tap': 1,
            'action_shot': 0,
            'barking_irons': 0,
            'point_blank_plasma': 0,
            'california_prayer_book': 0,
            'one_at_atime': 0,
            'five_beans_in_the_wheel': 0,
        },
        'carbine': {
            'facemelt': 1,
            'bushwack': 0,
            'big_fifty': 0,
            'stand_and_deliver': 0,
            'cowboy_cocktail': 0,
            'in_for_it': 0,
            'zero': 0,
        },
    },

    'armor_gems': [],  # list of equipped gems here

    'gun_one': {
        'name': 'Level 1 Magnum (0/100)',
        'gun_class': 'magnum',
        'level': 1,
        'damage': 7,
        'travel': 300,
        'velocity': 30,
        'accuracy': 65,
        'rof': .5,
        'crit_chance': 10,
        'crit_multiplier': 3,
        'image': load_image('pm_magnum.png'), # noqa
        'gun_fire_sound': load_sound('laser.wav'), # noqa
        'on_hit_sound': load_sound('on_hit.wav'), # noqa
        'gem_slots': {},
        },
    'gun_two': {
        'name': 'Level 1 Carbine (0/100)',
        'gun_class': 'carbine',
        'level': 1,
        'damage': 3,
        'travel': 600,
        'velocity': 30,
        'accuracy': 85,
        'rof': 2,
        'crit_chance': 2,
        'crit_multiplier': 2,
        'image': load_image('pm_magnum.png'), # noqa
        'gun_fire_sound': load_sound('laser.wav'), # noqa
        'on_hit_sound': load_sound('on_hit.wav'), # noqa
        'effects': [],
        'gem_slots': {},
        },
    'gun_inventory': [],
    'gem_inventory': [],
    }
