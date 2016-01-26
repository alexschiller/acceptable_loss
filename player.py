from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa
from functools import partial # noqa
from longbow import * # noqa
from controller import Controller

class Player(Character):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.hp_shield_bar = pyglet.sprite.Sprite(load_image('hp_shield.png', anchor=False), window_width - 1050, 0, batch=gfx_batch),  # noqa
        self.evade_acc_bar = pyglet.sprite.Sprite(load_image('evade_acc.png', anchor=False), window_width - 415, 0, batch=gfx_batch),  # noqa
        self.energy = 100
        self.inventory = []

    def update_bars(self):
        if self.energy < 100:
            self.energy = 100
        sw = int(max(115 * self.stats.shield / self.stats.shield_max, 1))
        hw = int(max(115 * self.stats.health / self.stats.health_max, 1))
        ae = (window_width - 410) + self.stats.evade_move / 10 * 70

        self.shield_bar = pyglet.sprite.Sprite(
            pyglet.image.create(sw, 15, blue_sprite),
            window_width - 1045, 30, batch=BarBatch)

        self.health_bar = pyglet.sprite.Sprite(
            pyglet.image.create(hw, 15, red_sprite),
            window_width - 1045, 5, batch=BarBatch)

        self.ae_bar = pyglet.sprite.Sprite(
            pyglet.image.create(70, 20, white_sprite),
            ae, 5, batch=BarBatch)


class PlayerController(Controller):
    def __init__(self, *args, **kwargs):
        super(PlayerController, self).__init__(*args, **kwargs)
        self.master = master
        self.black_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 150))
        self.black_dot = pyglet.image.create(10, 10, self.black_sprite)

        self.sprite = pyglet.sprite.Sprite(self.black_dot,
                    0, 0, batch=gfx_batch)

        self.collision = SpriteCollision(self.sprite)

        red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
        self.red_dot = pyglet.image.create(5, 5, red_sprite)
        self.marker = []

    def slot_one_fire(self):
        self.puppet.ability.missile_launch()

    def slot_two_fire(self):
        #elf.puppet.ability.magnum_california_prayer_book()
        pass

    def on_hit(self):
        pass

    def update_target(self):
        for e in self.puppet.enemies:
            if collide(self.collision, e.collision):
                self.build_target(e)
                break

    def build_target(self, e):
        bar = 2
        self.puppet.target = e
        h = e.sprite.height
        w = e.sprite.width
        v = max(h, w)
        v2 = v / 2
        x = e.sprite.x
        y = e.sprite.y

        vs = pyglet.image.create(bar, v2, red_sprite)
        hs = pyglet.image.create(v2, bar, red_sprite)

        self.marker = [
            #  Bottom two verticals
            pyglet.sprite.Sprite(vs, x - v - 2, y - v, batch=gfx_batch),  # noqa 
            pyglet.sprite.Sprite(vs, x + v, y - v, batch=gfx_batch),  # noqa 
            #  Bottom two horizontals
            pyglet.sprite.Sprite(hs, x - v - 2, y - v, batch=gfx_batch),  # noqa 
            pyglet.sprite.Sprite(hs, x + v - v2 + 2, y - v, batch=gfx_batch),  # noqa 
            #  Top two verticals
            pyglet.sprite.Sprite(vs, x - v - 2, y + v, batch=gfx_batch),  # noqa 
            pyglet.sprite.Sprite(vs, x + v, y + v, batch=gfx_batch),  # noqa 
            #  Top two horizontals
            pyglet.sprite.Sprite(hs, x - v - 2, y + v + 5, batch=gfx_batch),  # noqa 
            pyglet.sprite.Sprite(hs, x + v - v2 + 2, y + v + 5, batch=gfx_batch),  # noqa 

        ]

    def target_closest_enemy(self, distance=float("inf")):
        try:
            min_dist = distance
            x1 = self.sprite.x
            y1 = self.sprite.y
            if len(self.puppet.enemies) == 0:
                return False
            for e in self.puppet.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    self.puppet.target = e
        except:
            self.puppet.target = None

    def check_target(self):
        self.marker = []
        if self.puppet.target:
            try:
                self.rotate(self.puppet.target.sprite.x, self.puppet.target.sprite.y)
                self.build_target(self.puppet.target)
                # self.puppet.ability.auto_attack()
            except:
                self.puppet.target = None
        else:
            self.rotate(self.sprite.x, self.sprite.y)

    def update(self):
        self.puppet.update_bars()
        self.target_closest_enemy()
        self.check_target()
        for p in self.master.loot.current_loot:
            if abs(self.puppet.sprite.x - p.sprite.x) < 10:
                if abs(self.puppet.sprite.y - p.sprite.y) < 10:
                    if collide(p.collision, self.master.player.collision):
                        self.master.loot.unpack_package(p)

lb_missile = {
        'gun_class': 'Missile',
        'level': 1,
        'damage_min': 8,
        'damage_max': 15,
        'travel': 700,
        'velocity': 100,
        'accuracy': 70,
        'rof': .5,
        'crit': 10,
        'crit_damage': 2,
        'armor_pierce': 5,
        'image': load_image('missile.png'), # noqa
        'gun_fire_sound': load_sound('laser.wav'), # noqa
        'on_hit_sound': load_sound('on_hit.wav'), # noqa
        'effects': [],
        'gem_slots': {
            '1': {
                'color': 'topaz',
                'current_gem': {'color': 'diamond', 'level': 4, 'stats': {'damage': 3, 'accuracy': 6, 'shield_regen': 2, 'shield_on_hit': 1, 'health_max_perc': 8}, 'rarity': 3} # noqa
            },
        },
    }

lb_autocannon = {
        'gun_class': 'Missile',
        'level': 1,
        'damage_min': 2,
        'damage_max': 4,
        'travel': 700,
        'velocity': 100,
        'accuracy': 85,
        'rof': 3,
        'crit': 10,
        'crit_damage': 3,
        'armor_pierce': 8,
        'image': load_image('autocannon.png'), # noqa
        'gun_fire_sound': load_sound('laser.wav'), # noqa
        'on_hit_sound': load_sound('on_hit.wav'), # noqa
        'effects': [],
        'gem_slots': {
            '1': {
                'color': 'topaz',
                'current_gem': {'color': 'diamond', 'level': 4, 'stats': {'damage': 3, 'accuracy': 6, 'shield_regen': 2, 'shield_on_hit': 1, 'health_max_perc': 8}, 'rarity': 3} # noqa
            },
        },
    }

player_armor = {
    'gem_slots': {
        '1': {
            'color': 'topaz',
            'current_gem': {'color': 'diamond', 'level': 4, 'stats': {'damage': 3, 'accuracy': 6, 'shield_regen': 2, 'shield_on_hit': 1, 'health_max_perc': 8}, 'rarity': 3} # noqa
            },
        },
    }


player_base = {
    'sprite': load_image('dreadnaught.png'),
    'coord': [window_width / 2, window_height / 2],
    'weapon_slot_one': lb_missile,
    'weapon_slot_two': lb_autocannon,
    'armor': player_armor,
    'ability': LongbowAbility,
    'ability_build': None,
    'color': 'blue',
    'friends': 'blue',
    'enemies': 'red',
    'blood_color': (30, 30, 30, 255),
    'controller': PlayerController,
    'stats': {
        'level': 1,
        'damage': 0,
        'damage_min': 0,
        'damage_max': 0,
        'damage_perc': 0,
        'attack_speed_perc': 0,
        'crit': 5,
        'crit_damage': 2,
        'accuracy': 0,
        'armor_pierce': 0,
        'shield_max': 10,
        'shield_max_perc': 0,
        'shield_regen': 1,
        'shield_on_hit': 0,
        'health_max': 500,
        'health_max_perc': 0,
        'health_regen': 0,
        'health_on_hit': 0,
        'armor': 1,
        'evade': 0,
        'speed': 3,
    },
}
