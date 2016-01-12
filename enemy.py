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
        self.move_target = (self.player.sprite.x, self.player.sprite.y)

        # enter effect
        self.spriteeffect.teleport(self.sprite.x, self.sprite.y, 5, 5)

    def on_death(self):
        # For some reason the auto append new enemy is borked
        # self.enemy.append(Enemy(self.master, base=gen_soldier_base()))
        self.spriteeffect.blood(self.sprite.x, self.sprite.y, 30, 50)
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

    def shoot(self, target_x, target_y, target):
        self.gun.fire(self.sprite.x, self.sprite.y, target_x, target_y, target) # noqa           

    def update_ai(self):
        self.move_target = (self.player.sprite.x, self.player.sprite.y)

    def timer_ai(self):
        self.ai_time += 1
        if self.ai_time == 30:
            self.ai_time = 0
            self.update_ai()

    def update(self):
        self.timer_ai()
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        x_dist = self.player.sprite.x - float(self.sprite.x)
        y_dist = self.player.sprite.y - float(self.sprite.y)
        self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

        ret = calc_vel_xy(self.move_target[0], self.move_target[1],
            self.sprite.x, self.sprite.y, self.speed)
        self.sprite.x += ret[0]
        self.sprite.y += ret[1]
        if math.hypot(abs(self.sprite.x - self.master.player.sprite.x), abs(self.sprite.y - self.master.player.sprite.y)) < self.gun.travel: # noqa
            self.shoot(self.player.sprite.x, self.player.sprite.y, self.player)
        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()


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
