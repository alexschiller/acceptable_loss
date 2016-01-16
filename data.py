
plasma_infusion = {
    'flavor_text': 0,
    'description': 0,
    'function': lambda: None,
    'min_level': 1,
},

plasmaslinger_abilities = {
    'plasma': {
        'plasma_infusion': plasma_infusion,
        'ace_in_the_hole': plasma_infusion,
        'plasma_painter': plasma_infusion,
        'plasma_shield': plasma_infusion,
        'melt_armor': plasma_infusion,
        'bright_lights': plasma_infusion,
        'meltdown': plasma_infusion,
    },
    'magnum': {
        'double_tap': plasma_infusion,
        'action_shot': plasma_infusion,
        'barking_irons': plasma_infusion,
        'point_blank_plasma': plasma_infusion,
        'california_prayer_book': plasma_infusion,
        'one_at_atime': plasma_infusion,
        'five_beans_in_the_wheel': plasma_infusion,
    },
    'carbine': {
        'facemelt': plasma_infusion,
        'bushwack': plasma_infusion,
        'big_fifty': plasma_infusion,
        'stand_and_deliver': plasma_infusion,
        'cowboy_cocktail': plasma_infusion,
        'in_for_it': plasma_infusion,
        'zero': plasma_infusion,
    },

}

plasmaslinger_class = {
    'pilot_image': 'mech.png',
    'mech': 'plasmaslinger.png',
    'abilities': plasmaslinger_abilities,
    'base_stats': {
        'hp': 50,
        'armor': 4,
        'shield': 10,
        'shield_regen': 1,
        'speed': 3,
        'evade': 0,
    },
}

save_1 = {
    'name': 'Rambo',
    'class': plasmaslinger_class,
    'level': 3,
    'foo': [0, 0, 1, 10],
    'pow': [0, 0, 2, 71],
    'eng': [0, 0, 4, 6],
    'sci': [0, 0, 2, 90],
    'mon': [0, 0, 1, 15],

    'ability_levels': {
        'plasma': {
            'plasma_infusion': 1,
            'ace_in_the_hole': 1,
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
        'name': 'Level 2 Carbine (10/100)',
        'gun_class': 'magnum',
        'level': 2,
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
        'gem_slots': {
            '1': {
                'color': 'blue',
                'current_gem': {
                    'color': 'blue',
                    'damage': 10,
                    'accuracy': 5,
                    'effect': 'fire'
                },
            },
        },
    },
    'gun_two': {
        'name': 'Level 1 Carbine (50/100)',
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
        'gem_slots': {
            '1': {
                'color': 'red',
                'current_gem': {
                    'color': 'red',
                    'level': 2,
                    'damage': 10,
                    'accuracy': 5,
                    'effect': 'fire'
                },
            },
        },
    },
    'gun_inventory': [],
    'gem_inventory': [

        {'color': 'red',
        'level': 2,
        'damage': 12,
        'accuracy': 5,
        'effect': 'fire'},

        {'color': 'green',
        'level': 1,
        'damage': 5,
        'accuracy': 3,
        'effect': 'fire'},

        {'color': 'blue',
        'level': 2,
        'damage': 10,
        'accuracy': 8,
        'effect': 'fire'},
    ]
}
