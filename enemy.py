from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
# import pyglet
import random

# import itertools
from gun import * # noqa

def gen_soldier_base():
    base = {
        'sprite': load_image('soldier.png'),
        'coord': random.choice([[-50, random.randint(0, window_height)], [random.randint(0, window_width), -50]]),  # noqa
        'kbr': 10,
        'health': 10,
        'speed': 1,
        'guns': [Gun(master, base=missile)],
    }
    return base

class Enemy(Character):
    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)

        self.build_character(kwargs['base'])

        self.ai_time = random.randint(0, 60)

        self.touch_damage = 0

        # enter effect
        self.spriteeffect.teleport(self.sprite.x, self.sprite.y, 5, 5)

    def on_death(self):
        # For some reason the auto append new enemy is borked
        # self.enemy.append(Enemy(self.master, base=gen_soldier_base()))
        # self.spriteeffect.blood(self.sprite.x, self.sprite.y, 30, 50)
        try:
            self.sprite.delete()
            self.enemies.remove(self)
        except:
            pass

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 10)
        self.sprite.x -= ret[0] * 2
        self.sprite.y -= ret[1] * 2
        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]

    def update_target(self):
        self.target = self.master.player

    def update(self):
        if self.health_bar:
            self.update_health_bar()
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        if collide(self.collision, self.player.collision):
            self.on_collide()

        self.required_updates()

class Soldier(Enemy):
    def __init__(self, *args, **kwargs):
        super(Soldier, self).__init__(*args, **kwargs)

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 10)
        self.sprite.x -= ret[0] * 2
        self.sprite.y -= ret[1] * 2
        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]
        self.health -= 10  # squish
