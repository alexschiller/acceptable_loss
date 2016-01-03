from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
# import pyglet
import random
import math
# import itertools
from gun import * # noqa

def gen_soldier_base():
    base = {
        'sprite': load_image('soldier.png'),
        'coord': [random.randint(0, window_width), random.randint(0, window_height)],
        'kbr': 50,
        'health': 10,
        'speed': 1,
        'gun': Gun(master, hits='friends', base=missile),
    }
    return base

class Enemy(Character):
    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)

        self.build_character(kwargs['base'])

        self.gun = kwargs['base']['gun']
        self.master.guns.append(self.gun)
        self.touch_damage = 0

        # enter effect
        self.spriteeffect.teleport(self.sprite.x, self.sprite.y, 5, 5)

    def on_death(self):
        # For some reason the auto append new enemy is borked
        # self.enemy.append(Enemy(self.master, base=gen_soldier_base()))
        self.spriteeffect.blood(self.sprite.x, self.sprite.y, 30, 50)
        try:
            self.sprite.delete()
            self.enemy.remove(self)
        except:
            pass

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 10)
        self.sprite.x -= ret[0] * 2
        self.sprite.y -= ret[1] * 2
        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]
        self.health -= 10

    def update(self):
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        x_dist = self.player.sprite.x - float(self.sprite.x)
        y_dist = self.player.sprite.y - float(self.sprite.y)
        self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
            self.sprite.x, self.sprite.y, self.speed)
        self.speed = .5
        self.sprite.x += ret[0]
        self.sprite.y += ret[1]
        if random.randint(0, 300) > 270:
            self.shoot(self.player.sprite.x, self.player.sprite.y)
        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()
