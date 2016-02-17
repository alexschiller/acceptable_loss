from pyglet.gl import * # noqa
from ability import * # noqa
from utility import * # noqa
from character import * # noqa
from controller import * # noqa
import random
from baseskills import * # noqa


enemy_skillset = {
    '1': BasicTrigger,
    '2': Skill,
    '3': Skill,
    '4': Skill,
}

enemy_build = {
    'slot_mouse_two': ['1', 1],
    'slot_one': ['1', 1],
    'slot_two': ['2', 1],
    'slot_three': ['3', 2],
    'slot_four': ['4', 3],
    'slot_q': ['1', 1],
    'slot_e': ['1', 1],
    'passive_one': ['1', 1],
    'passive_two': ['1', 1],
    'passive_three': ['1', 1],
}


def gen_zombie_gun(level):
    return {
        'gun_class': 'Melee',
        'level': level,
        'damage_min': 2 * level,
        'damage_max': 5 * level,
        'travel': 30,
        'range_min': 0,
        'range_max': 30,
        'velocity': 15,
        'recoil': 10,
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

def gen_tank_gun(level):
    return {
        'gun_class': 'Rifle',
        'level': level,
        'damage_min': 4 * level,
        'damage_max': 9 * level,
        'travel': 800,
        'range_min': 200,
        'range_max': 700,
        'velocity': 100,
        'recoil': 10,
        'accuracy': 70,
        'rof': .25,
        'crit': 2,
        'crit_damage': 2,
        'armor_pierce': 10,
        'image': load_image('tank_gun.png'), # noqa
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
        'range_min': 200,
        'range_max': 500,
        'velocity': 100,
        'accuracy': 70,
        'rof': .75,
        'recoil': 10,
        'crit': 2,
        'crit_damage': 2,
        'armor_pierce': 1,
        'image': load_image('snipe.png'), # noqa
        'gun_fire_sound': load_sound('laser.wav'), # noqa
        'on_hit_sound': load_sound('on_hit.wav'), # noqa
        'effects': [],
        'gem_slots': {},
        }

def enemy_soldier_base(level, x, y):
    return {
        'sprite': load_image(random.choice(['soldier.png', 'green_soldier.png'])), # noqa
        'coord': [x, y],
        'weapon_slot_one': gen_soldier_gun(level),
        'weapon_slot_two': gen_soldier_gun(level),
        'armor': {'gem_slots': {}},
        'skillset': enemy_skillset,
        'build': enemy_build,
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

def enemy_tank_base(level, x, y):
    return {
        'sprite': load_image('tank.png'), # noqa
        'coord': [x, y],
        'weapon_slot_one': gen_tank_gun(level),
        'weapon_slot_two': gen_tank_gun(level),
        'armor': {'gem_slots': {}},
        'skillset': enemy_skillset,
        'build': enemy_build,
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
            'health_max': 20 * level,
            'health_max_perc': 0,
            'health_regen': 0 * level / 2,
            'health_on_hit': 0,
            'armor': 2 * level,
            'evade': 0,
            'speed': 1,
        },
    }


def enemy_zombie_base(level, x, y):
    return {
        'sprite': load_image('zombie.png'),
        'coord': [x, y],
        'weapon_slot_one': gen_zombie_gun(level),
        'weapon_slot_two': gen_zombie_gun(level),
        'armor': {'gem_slots': {}},
        'skillset': enemy_skillset,
        'build': enemy_build,
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
            'armor': 0 * level,
            'evade': 10,
            'speed': 3,
        },
    }

def gen_drone_gun(level):
    return {
        'gun_class': 'Rifle',
        'level': level,
        'damage_min': 1 * level,
        'damage_max': 2 * level,
        'travel': 200,
        'range_min': 100,
        'range_max': 400,
        'velocity': 100,
        'accuracy': 30,
        'rof': .75,
        'recoil': 10,
        'crit': 2,
        'crit_damage': 2,
        'armor_pierce': 0,
        'image': load_image('drone_bullet.png'), # noqa
        'gun_fire_sound': load_sound('laser.wav'), # noqa
        'on_hit_sound': load_sound('on_hit.wav'), # noqa
        'effects': [],
        'gem_slots': {},
        }

def enemy_drone_base(level, x, y):
    return {
        'sprite': load_image('drone.png'), # noqa
        'coord': [x, y],
        'weapon_slot_one': gen_drone_gun(level),
        'weapon_slot_two': gen_drone_gun(level),
        'armor': {'gem_slots': {}},
        'skillset': enemy_skillset,
        'build': enemy_build,
        'color': 'red',
        'friends': 'red',
        'enemies': 'blue',
        'blood_color': (140, 140, 140, 255),
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
            'health_max': 3 * level,
            'health_max_perc': 0,
            'health_regen': 1 * level / 2,
            'health_on_hit': 0,
            'armor': 1 * level,
            'evade': 20,
            'speed': 4,
        },
    }
