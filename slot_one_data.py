player_base = {
    'class': 'plasmaslinger',
    'sprite': 'plasmaslinger.png',
    'coord': None,
    'gun': {
        'level': 1,
        'damage_min': 5,
        'damage_max': 7,
        'travel': 700,
        'range_min': 200,
        'range_max': 600,
        'velocity': 15,
        'accuracy': 85,
        'rof': 10,
        'recoil': 5,
        'crit': 10,
        'crit_damage': 1.5,
        'armor_pierce': 1,
        'image': 'magnum.png', # noqa
        'gun_fire_sound': 'shot.wav', # noqa
        'on_hit_sound': 'on_hit.wav', # noqa
        'effects': [],
        'gem_slots': {
            '1': {
                'color': 'topaz',
                'current_gem': {'color': 'diamond', 'level': 4, 'stats': {'accuracy': 6, 'shield_regen': 2, 'shield_on_hit': 1, 'health_max_perc': 8}, 'rarity': 3} # noqa
            },
        },
    },
    'armor': {
    'gem_slots': {
        '1': {
            'color': 'topaz',
            'current_gem': {'color': 'diamond', 'level': 4, 'stats': {'damage': 3, 'accuracy': 6, 'shield_regen': 2, 'shield_on_hit': 1, 'health_max_perc': 8}, 'rarity': 3} # noqa
            },
        },
    },
    # 'skillset': None,
    'build': {
        'slot_mouse_two': ['21', 1],
        'slot_one': ['18', 1],
        'slot_two': ['12', 1],
        'slot_three': ['12', 2],
        'slot_four': ['12', 3],
        'slot_q': ['1', 1],
        'slot_e': ['1', 1],
        'passive_one': ['1', 1],
        'passive_two': ['1', 1],
        'passive_three': ['1', 1],
    },
    'color': 'blue',
    'friends': 'blue',
    'enemies': 'red',
    'blood_color': (30, 30, 30, 255),
    # 'controller': None,
    'stats': {
        'level': 1,
        'damage': 0,
        'damage_min': 0,
        'damage_max': 0,
        'damage_perc': 0,
        'attack_speed_perc': 0,
        'crit': 5,
        'crit_damage': .1,
        'accuracy': 0,
        'armor_pierce': 0,
        'shield_max': 10,
        'shield_max_perc': 0,
        'shield_regen': .1,
        'shield_on_hit': 0,
        'health_max': 500,
        'health_max_perc': 0,
        'health_regen': 0,
        'health_on_hit': 0,
        'armor': 1,
        'evade': 0,
        'speed': 5,
    },
    'gem_inventory': [],
    'gun_inventory': [],
    'shield_inventory': [],
}