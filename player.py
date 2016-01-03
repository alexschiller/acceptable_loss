from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
import math
import itertools
from gun import * # noqa

player_base = {
    'sprite': load_image('dreadnaught.png'),
    'coord': [50, 50],
    'kbr': 50,
    'health': 100,
    'speed': 1,
}

class Player(Character):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        self.build_character(kwargs['base'])

        # Player specific defaults
        self.max_energy = 100
        self.energy = 100

        self.max_shield = 100
        self.shield = 100

    def closest_object(self):
        closest = None
        min_dist = float('inf')
        x1 = self.sprite.x
        y1 = self.sprite.y
        for o in self.master.objects:
            dist = math.sqrt((o.sprite.x - x1) ** 2 + (o.sprite.y - y1) ** 2)
            if dist < min_dist:
                closest = o
                min_dist = dist
        return closest

    def check_object_collision(self, o):
        if collide(self.collision, o.collision):
            ret = calc_vel_xy(self.sprite.x, self.sprite.y,
            o.sprite.x, o.sprite.y, 3)
            self.sprite.x += ret[0]
            self.sprite.y += ret[1]

    def update(self):
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        if self.energy < 100:
            self.energy += 1
        self.shield_bar = pyglet.sprite.Sprite(
            pyglet.image.create(200 * self.shield / self.max_shield, 10, green_sprite),
            20, window_height - 20, batch=BarBatch)

        self.health_bar = pyglet.sprite.Sprite(
            pyglet.image.create(200 * self.health / self.max_health, 10, red_sprite),
            20, window_height - 40, batch=BarBatch)

        self.energy_bar = pyglet.sprite.Sprite(
            pyglet.image.create(200 * self.energy / self.max_energy, 10, blue_sprite),
            20, window_height - 60, batch=BarBatch)

    def on_hit(self, bullet):
        self.health -= bullet.damage
        self.spriteeffect.blood(bullet.sprite.x, bullet.sprite.y, 3, 5)
        impact = bullet.knockback / self.kbr
        self.sprite.x += bullet.vel_x * impact
        self.sprite.y += bullet.vel_y * impact

    def next_gun(self):
        self.gun = self.guns[next(self.cycle_guns)]

    def load_guns(self, guns):
        self.guns = guns
        self.cycle_guns = itertools.cycle(range(len(self.guns)))
        self.gun = self.guns[0]
