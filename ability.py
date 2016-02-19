# from functools import partial
import math # noqa
import random # noqa
from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet # noqa
# import itertools
from functools import partial
from collide import * # noqa
from build import Build
# from copy import copy

class Ability(object):
    def __init__(self, master, owner, skillset, build, gun_one, gun_two):
        self.master = master
        self.owner = owner
        self.delayed = []
        self.global_cooldown = False
        self.thrown = []
        self.build = Build(self.master, self, skillset, build)
        self.slot_mouse_two = self.build.slot_mouse_two
        self.slot_one = self.build.slot_one
        self.slot_two = self.build.slot_two
        self.slot_three = self.build.slot_three
        self.slot_four = self.build.slot_four
        self.slot_q = self.build.slot_q
        self.slot_e = self.build.slot_e
        # self.core = self.skillset['core']()

    def slot_mouse_two_fire(self):
        self.slot_mouse_two.fire()

    def slot_one_fire(self):
        self.slot_one.fire()

    def slot_two_fire(self):
        self.slot_two.fire()

    def slot_three_fire(self):
        self.slot_three.fire()

    def slot_four_fire(self):
        self.slot_four.fire()

    def slot_q_fire(self):
        self.slot_q.fire()

    def slot_e_fire(self):
        self.slot_e.fire()

    def build_bullet(self, gun, start_x, start_y, target_x, target_y, enemy_range, enemy, image=None): # noqa
        calc_gun = gun
        calc_gun['start_x'] = start_x
        calc_gun['start_y'] = start_y
        calc_gun['target_x'] = target_x
        calc_gun['target_y'] = target_y
        calc_gun['enemy_range'] = enemy_range
        calc_gun['enemy'] = enemy
        calc_gun['image'] = image or gun['image']
        return dict.copy(gun)

    def global_cooldown_reset(self):  # this is a super tacky way to do this for sure...
        self.global_cooldown = False

    def trigger_global_cooldown(self):
        self.global_cooldown = True
        self.delayed.append([30, partial(self.global_cooldown_reset)])

    def update_delayed(self):
        for p in self.delayed:
            p[0] -= 1
            if p[0] == 0:
                try:
                    p[1]()
                except:
                    'failed delayed action'
                self.delayed.remove(p)

    def update(self):
        for t in self.thrown:
            t.update()

        self.update_delayed()
