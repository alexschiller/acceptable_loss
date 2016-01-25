from pyglet.gl import * # noqa
from ability import * # noqa
from utility import * # noqa
from character import * # noqa
from controller import * # noqa
import random

def gen_zombie_gun(level):
    return {
        'gun_class': 'Melee',
        'level': level,
        'damage_min': 2 * level,
        'damage_max': 5 * level,
        'travel': 30,
        'velocity': 15,
        'accuracy': 85,
        'rof': .75,
        'crit': 5,
        'crit_damage': 4,
        'armor_pierce': 2,
        'image': load_image('slash.png'), # noqa
        'gun_fire_sound': load_sound('laser.wav'), # noqa
        'on_hit_sound': load_sound('on_hit.wav'), # noqa
        'effects': [],
        'gem_slots': {},
        }

def gen_soldier_gun(level):
    return {
        'gun_class': 'Rifle',
        'level': level,
        'damage_min': 2 * level,
        'damage_max': 5 * level,
        'travel': 400,
        'velocity': 100,
        'accuracy': 70,
        'rof': .75,
        'crit': 2,
        'crit_damage': 2,
        'armor_pierce': 1,
        'image': load_image('snipe.png'), # noqa
        'gun_fire_sound': load_sound('laser.wav'), # noqa
        'on_hit_sound': load_sound('on_hit.wav'), # noqa
        'effects': [],
        'gem_slots': {},
        }


def enemy_soldier_base(level):
    return {
        'sprite': load_image(random.choice(['soldier.png', 'green_soldier.png'])), # noqa
        'coord': random.choice([[-50, random.randint(0, window_height)], [random.randint(0, window_width), -50]]),  # noqa
        'weapon_slot_one': gen_soldier_gun(level),
        'weapon_slot_two': gen_soldier_gun(level),
        'armor': {'gem_slots': {}},
        'ability': Ability,
        'ability_build': None,
        'color': 'red',
        'friends': 'red',
        'enemies': 'blue',
        'blood_color': (255, 10, 10, 255),
        'controller': Controller,
        'stats': {
            'level': level,
            'damage': 0,
            'damage_min': 0,
            'damage_max': 0,
            'damage_perc': 0,
            'attack_speed_perc': 0,
            'crit': 5,
            'crit_damage': 2,
            'accuracy': 0,
            'armor_pierce': 0,
            'shield_max': 5,
            'shield_max_perc': 0,
            'shield_regen': 1,
            'shield_on_hit': 0,
            'health_max': 10 * level,
            'health_max_perc': 0,
            'health_regen': 1 * level / 2,
            'health_on_hit': 0,
            'armor': 1 * level,
            'evade': 0,
            'speed': 2,
        },
    }

def enemy_zombie_base(level):
    return {
        'sprite': load_image('zombie.png'),
        'coord': random.choice([[-50, random.randint(0, window_height)], [random.randint(0, window_width), -50]]),  # noqa
        'weapon_slot_one': gen_zombie_gun(level),
        'weapon_slot_two': gen_zombie_gun(level),
        'armor': {'gem_slots': {}},
        'ability': Ability,
        'ability_build': None,
        'color': 'red',
        'friends': 'red',
        'enemies': 'blue',
        'blood_color': (255, 10, 10, 255),
        'controller': Controller,
        'stats': {
            'level': level,
            'damage': 0,
            'damage_min': 0,
            'damage_max': 0,
            'damage_perc': 0,
            'attack_speed_perc': 0,
            'crit': 5,
            'crit_damage': 2,
            'accuracy': 0,
            'armor_pierce': 0,
            'shield_max': 0,
            'shield_max_perc': 0,
            'shield_regen': 0,
            'shield_on_hit': 0,
            'health_max': 10 * level,
            'health_max_perc': 0,
            'health_regen': 1 * level / 2,
            'health_on_hit': 0,
            'armor': 2 * level,
            'evade': 10,
            'speed': 3,
        },
    }
