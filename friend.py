from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
# import pyglet
import random
import math
# import itertools
from gun import * # noqa

def gen_friend_base():
    base = {
        'sprite': load_image('tmech.png'),
        'coord': [random.randint(0, window_width), random.randint(0, window_height)],
        'kbr': 10,
        'health': 10,
        'speed': 1,
        'guns': [Gun(master, hits='enemies', base=shotgun)],
    }
    return base

def gen_cannon_base():
    base = {
        'sprite': load_image('can.png'),
        'coord': [window_width / 2 + 50, window_height / 2 + 50],
        'kbr': 10,
        'health': 10,
        'speed': 1,
        'guns': [Gun(master, hits='enemies', base=sniper)],
    }
    return base

def gen_carpet_base(mouse):
    base = {
        'sprite': load_image('jet.png'),
        'coord': random.choice([[-50, random.randint(0, window_height)], [random.randint(0, window_width), -50]]), # noqa
        'kbr': 10,
        'health': 1800,
        'speed': 10,
        'guns': [Gun(master, hits='enemies', base=bomb)],
        'mouse': mouse,
    }
    return base

class Friend(Character):
    def __init__(self, *args, **kwargs):
        super(Friend, self).__init__(*args, **kwargs)

        self.build_character(kwargs['base'])

        self.touch_damage = 0

        # enter effect
        self.spriteeffect.teleport(self.sprite.x, self.sprite.y, 5, 5)

    def on_death(self):
        self.spriteeffect.blood(self.sprite.x, self.sprite.y, 30, 50)
        try:
            self.sprite.delete()
            self.master.friends.remove(self)
        except:
            pass

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 10)
        self.sprite.x -= ret[0] * 2
        self.sprite.y -= ret[1] * 2
        # self.player.sprite.x += ret[0]
        # self.player.sprite.y += ret[1]

    def select_target(self):
        try:
            min_dist = float("inf")
            coord = (0, 0)
            x1 = self.sprite.x
            y1 = self.sprite.y
            for e in self.master.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    coord = (e.sprite.x, e.sprite.y)
            return coord
        except:
            print "snail fail"
            return [self.sprite.x + random.randint(-5, 5), self.sprite.x + random.randint(-5, 5)] # noqa

    def update(self):
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass
        x_dist = self.player.sprite.x - float(self.sprite.x)
        y_dist = self.player.sprite.y - float(self.sprite.y)
        if abs(y_dist) + abs(x_dist) > 50:
            self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

            ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
                self.sprite.x, self.sprite.y, self.speed)
            self.sprite.x += ret[0]
            self.sprite.y += ret[1]
        if random.randint(0, 100) > 50:
            loc = self.select_target()
            self.shoot(loc[0], loc[1])
        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()


class Carpet(Friend):
    def __init__(self, *args, **kwargs):
        super(Carpet, self).__init__(*args, **kwargs)
        self.ret = calc_vel_xy(kwargs['base']['mouse'][0], kwargs['base']['mouse'][1],
            self.sprite.x, self.sprite.y, self.speed)

        x_dist = kwargs['base']['mouse'][0] - float(self.sprite.x)
        y_dist = kwargs['base']['mouse'][1] - float(self.sprite.y)
        self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

    def check_object_collision(self, o):
        pass

    def update(self):
        self.health -= self.speed
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass
        self.sprite.x += self.ret[0]
        self.sprite.y += self.ret[1]

        loc = self.select_target()
        self.shoot(loc[0], loc[1])

        if self.health <= 0:
            self.on_death()

class Cannon(Friend):
    def __init__(self, *args, **kwargs):
        super(Cannon, self).__init__(*args, **kwargs)

    def move(self):
        pass

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 10)

        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]

    def update(self):
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        if random.randint(0, 100) > 50:
            loc = self.select_target()
            x_dist = loc[0] - float(self.sprite.x)
            y_dist = loc[1] - float(self.sprite.y)
            self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90
            self.shoot(loc[0], loc[1])

        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()
