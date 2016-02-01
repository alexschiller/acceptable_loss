from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa
from functools import partial # noqa
from longbow import * # noqa
from controller import Controller
import itertools


class Player(Character):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        # self.hp_shield_bar = pyglet.sprite.Sprite(load_image('hp_shield.png', anchor=False), window_width - 1050, 0, batch=gfx_batch),  # noqa
        # self.evade_acc_bar = pyglet.sprite.Sprite(load_image('evade_acc.png', anchor=False), window_width - 415, 0, batch=gfx_batch),  # noqa
        # self.accuracy_bar = pyglet.sprite.Sprite(load_image('evade_acc.png', anchor=False), window_width - 415, 30, batch=gfx_batch),  # noqa
        self.visor = pyglet.sprite.Sprite(load_image('visor.png', anchor=False), -1, window_height-171, batch=gfx_batch),  # noqa
        self.energy = 100
        self.inventory = []
        self.shield_bar = pyglet.sprite.Sprite(pyglet.image.create(271, 13, blue_sprite),
            10, window_height - 25, batch=BarBatch) # noqa
        self.health_bar = pyglet.sprite.Sprite(pyglet.image.create(271, 13, red_sprite),
            10, window_height - 40, batch=BarBatch) # noqa

        self.ae_bar = pyglet.sprite.Sprite(
            pyglet.image.create(50, 13, white_sprite),
            31, window_height - 168, batch=BarBatch)

        self.acc_bar = pyglet.sprite.Sprite(
            pyglet.image.create(3, 13, red_sprite),
            150, window_height - 168, batch=BarBatch)
        self.acc_mouse_mod = 0

        self.acc_mouse_bar_l = pyglet.sprite.Sprite(
            pyglet.image.create(20, 2, red_sprite),
            -50, -50, batch=BarBatch)

        self.acc_mouse_bar_r = pyglet.sprite.Sprite(
            pyglet.image.create(20, 2, red_sprite),
            -50, -50, batch=BarBatch)

        self.acc_mouse_bar_t = pyglet.sprite.Sprite(
            pyglet.image.create(2, 20, red_sprite),
            -50, -50, batch=BarBatch)

        self.acc_mouse_bar_b = pyglet.sprite.Sprite(
            pyglet.image.create(2, 20, red_sprite),
            -50, -50, batch=BarBatch)

    def target_distance(self):
        if self.target:
            dist = min(math.hypot(self.controller.sprite.x - self.target.sprite.x, self.controller.sprite.y - self.target.sprite.y), 300) # noqa
            self.acc_mouse_mod = 1 - (dist / 300.0)
            return self.acc_mouse_mod
        return 1

    def update_bars(self):
        if self.energy < 100:
            self.energy = 100
        self.shield_bar.x = 10 - (271 - (self.stats.shield / float(self.stats.shield_max) * 271)) # noqa
        self.health_bar.x = 10 - (271 - (self.stats.health / float(self.stats.health_max) * 271)) # noqa
        # self.acc_bar.x = 150 + min(int((self.stats.accuracy + self.stats.gun_two_data['accuracy']) * self.target_distance()), 100) # noqa
        acc_val = 100 - min(int((self.stats.accuracy + self.stats.gun_two_data['accuracy']) * self.target_distance()), 100) # noqa
        x = self.controller.sprite.x
        y = self.controller.sprite.y
        self.acc_mouse_bar_l.x = x + acc_val + 3
        self.acc_mouse_bar_r.x = x - acc_val - 20
        self.acc_mouse_bar_l.y = y
        self.acc_mouse_bar_r.y = y

        self.acc_mouse_bar_t.x = x
        self.acc_mouse_bar_b.x = x
        self.acc_mouse_bar_t.y = y + acc_val + 3
        self.acc_mouse_bar_b.y = y - acc_val - 20

        self.ae_bar.x = 31 + self.stats.evade_move / 10 * 50


class PlayerController(Controller):
    def __init__(self, *args, **kwargs):
        super(PlayerController, self).__init__(*args, **kwargs)
        self.master = master
        self.black_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 150))
        self.black_dot = pyglet.image.create(1, 1, self.black_sprite)
        self.sprite = pyglet.sprite.Sprite(self.black_dot, 0, 0, batch=gfx_batch)

        self.collision = SpriteCollision(self.sprite)
        self.timer = itertools.cycle(range(3))
        red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
        self.red_dot = pyglet.image.create(5, 5, red_sprite)
        self.marker = None
        self.timg = load_image('target.png')

    def slot_one_fire(self):
        self.puppet.ability.missile_launch()

    def slot_two_fire(self):
        # elf.puppet.ability.magnum_california_prayer_book()
        pass

    def on_hit(self):
        pass

    def update_target(self):
        for e in self.puppet.enemies:
            if collide(self.collision, e.collision):
                self.build_target(e)
                break

    def build_target(self, e):
        self.marker = pyglet.sprite.Sprite(self.timg, e.sprite.x - 10, e.sprite.y - 10, batch=gfx_batch)  # noqa 

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

    def move(self, mx, my):
        self.last_mx = mx
        self.last_my = my
        if mx and my:
            mx = mx / 1.41
            my = my / 1.41
        self.puppet.stats.update_move(mx, my)
        self.puppet.sprite.x += (self.puppet.stats.speed * mx)
        self.puppet.sprite.y += (self.puppet.stats.speed * my)

    def check_target(self):
        # self.marker = []
        if self.puppet.target:
            try:
                # self.rotate(self.puppet.target.sprite.x, self.puppet.target.sprite.y)
                self.build_target(self.puppet.target)
                # self.puppet.ability.auto_attack()
            except:
                self.puppet.target = None
        else:
            # pass
            self.rotate(self.sprite.x, self.sprite.y)

    def update(self):
        if self.timer.next() == 1:
            self.puppet.update_bars()
            self.target_closest_enemy()
        for p in self.master.loot.current_loot:
            if abs(self.puppet.sprite.x - p.sprite.x) < 10:
                if abs(self.puppet.sprite.y - p.sprite.y) < 10:
                    if collide(p.collision, self.master.player.collision):
                        self.master.loot.unpack_package(p)
        self.check_target()

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
        'velocity': 80,
        'accuracy': 85,
        'rof': 10,
        'crit': 10,
        'crit_damage': 3,
        'armor_pierce': 8,
        'image': load_image('magnum.png'), # noqa
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
