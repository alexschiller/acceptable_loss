import math # noqa
import random # noqa
from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet # noqa
from collide import * # noqa
from build import Build

class Ability(object):
    def __init__(self, master, owner, skillset, build, gun_one, gun_two):
        self.master = master
        self.owner = owner
        self.delayed = []
        self.global_cooldown = False
        self.global_cooldown_time = 30
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
        if not self.global_cooldown and not self.slot_mouse_two.cooldown:
            if self.slot_mouse_two.fire():
                self.trigger_global_cooldown()

    def slot_one_fire(self):
        if not self.global_cooldown and not self.slot_one.cooldown:
            if self.slot_one.fire():
                self.trigger_global_cooldown()

    def slot_two_fire(self):
        if not self.global_cooldown and not self.slot_two.cooldown:
            if self.slot_two.fire():
                self.trigger_global_cooldown()

    def slot_three_fire(self):
        if not self.global_cooldown and not self.slot_three.cooldown:
            if self.slot_three.fire():
                self.trigger_global_cooldown()

    def slot_four_fire(self):
        if not self.global_cooldown and not self.slot_four.cooldown:
            if self.slot_four.fire():
                self.trigger_global_cooldown()

    def slot_q_fire(self):
        if not self.global_cooldown and not self.slot_q.cooldown:
            if self.slot_q.fire():
                self.trigger_global_cooldown()

    def slot_e_fire(self):
        if not self.global_cooldown and not self.slot_e.cooldown:
            if self.slot_e.fire():
                self.trigger_global_cooldown()

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

    def trigger_global_cooldown(self):
        self.global_cooldown += self.global_cooldown_time

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
        if self.global_cooldown:
            self.global_cooldown -= 1
        self.slot_mouse_two.update()
        self.slot_one.update()
        self.slot_two.update()
        self.slot_three.update()
        self.slot_four.update()
        self.slot_q.update()
        self.slot_e.update()
        for t in self.thrown:
            t.update()

        self.update_delayed()
