from functools import partial
import math # noqa
import random
from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet
# import itertools
from collide import * # noqa

class Thrown(object):
    def __init__(self, master, ability, base):  # noqa
        # Base stats
        self.master = master
        self.owner = ability
        self.base = base
        self.damage_min = self.base['damage_min']
        self.damage_max = self.base['damage_max']
        self.velocity = self.base['velocity']
        self.accuracy = self.base['accuracy']
        self.crit_chance = self.base['crit']
        self.crit_damage = self.base['crit_damage']
        self.enemy_range = self.base['enemy_range']
        self.start_x = self.base['start_x']
        self.start_y = self.base['start_y']
        self.target_x = self.base['target_x']
        self.target_y = self.base['target_y']
        self.enemy = self.base['enemy']
        img = self.base['image']
        self.travelled = 0

        # Calculate shit here
        self.crit = False
        self.evade = False
        self.hit = random.randint(0, 100) < self.accuracy

        if self.hit and random.randint(0, 100) < self.crit_chance:
            self.crit = True
            self.damage_min = self.damage_min * self.crit_damage
            self.damage_max = self.damage_max * self.crit_damage

        self.damage = random.randint(self.damage_min, self.damage_max)

        if self.hit and random.randint(0, 100) < self.enemy.stats.evade:
            self.evade = True

        self.sprite = pyglet.sprite.Sprite(img,
            self.start_x, self.start_y, batch=BulletBatch)

        dist_x = self.target_x - float(self.start_x)
        dist_y = self.target_y - float(self.start_y)

        self.sprite.rotation = (math.degrees(math.atan2(dist_y, dist_x)) * -1) + 90
        self.sprite.scale = 1

        ret = calc_vel_xy(self.target_x, self.target_y,
            self.start_x, self.start_y, self.velocity)

        if self.hit:
            self.vel_x = ret[0]
            self.vel_y = ret[1]
        else:
            self.vel_x = ret[0] + random.choice([-1, 1])
            self.vel_y = ret[1] + random.choice([-1, 1])

    def delete_thrown(self):
        self.display_outcome()
        self.sprite.delete()
        self.owner.thrown.remove(self)

    def display_outcome(self):
        x = self.sprite.x
        y = self.sprite.y
        if self.evade:
            self.master.spriteeffect.bullet_evade(x, y, 'evade') # noqa
        elif self.crit:
            self.master.spriteeffect.bullet_crit(x, y, self.damage) # noqa
        elif self.hit:
            self.master.spriteeffect.bullet_hit(x, y, self.damage) # noqa
        else:
            self.master.spriteeffect.bullet_miss(x, y, 'miss') # noqa

    def update(self):
        self.sprite.x += self.vel_x
        self.sprite.y += self.vel_y
        self.travelled += math.hypot(self.vel_x, self.vel_y)
        if self.travelled > self.enemy_range:
            if self.hit and not self.evade:
                # try:
                self.enemy.on_hit(self)
                # except:
                    # pass
            self.delete_thrown()

class Ability(object):
    def __init__(self, master, owner, gun_one, gun_two):
        self.master = master
        self.owner = owner
        # self.delayed = []
        # self.global_cooldown = False
        # self.aa_cooldown = False
        self.thrown = []

    def slot_mouse_one_fire(self):
        self.puppet.ability.slot_mouse_one_fire()

    def slot_mouse_two_fire(self):
        self.puppet.ability.slot_mouse_two_fire()

    def slot_one_fire(self):
        self.puppet.ability.slot_one_fire()

    def slot_two_fire(self):
        self.puppet.ability.slot_two_fire()

    def slot_three_fire(self):
        self.puppet.ability.slot_three_fire()

    def slot_four_fire(self):
        self.puppet.ability.slot_four_fire()

    def slot_q_fire(self):
        self.puppet.ability.slot_q_fire()

    def slot_e_fire(self):
        self.puppet.ability.slot_e_fire()

    # def build_bullet(self, gun, start_x, start_y, target_x, target_y, enemy_range, enemy, image=None): # noqa
    #     calc_gun = gun
    #     calc_gun['start_x'] = start_x
    #     calc_gun['start_y'] = start_y
    #     calc_gun['target_x'] = target_x
    #     calc_gun['target_y'] = target_y
    #     calc_gun['enemy_range'] = enemy_range
    #     calc_gun['enemy'] = enemy
    #     calc_gun['image'] = image or gun['image']
    #     return gun

    # def aa_cooldown_reset(self):
    #     self.aa_cooldown = False

    # def trigger_aa_cooldown(self, time):
    #     self.aa_cooldown = True
    #     self.delayed.append([time, partial(self.aa_cooldown_reset)])

    # def global_cooldown_reset(self):  # this is a super tacky way to do this for sure...
    #     self.global_cooldown = False

    # def trigger_global_cooldown(self):
    #     self.global_cooldown = True
    #     self.delayed.append([30, partial(self.global_cooldown_reset)])

    # def update_delayed(self):
    #     for p in self.delayed:
    #         p[0] -= 1
    #         if p[0] == 0:
    #             try:
    #                 p[1]()
    #             except:
    #                 'failed delayed action'
    #             self.delayed.remove(p)

    def update(self):
        for t in self.thrown:
            t.update()

        # self.update_delayed()

    # def can_aa_shoot(self):
    #     if not self.aa_cooldown:
    #         if self.owner.target:
    #             dist_x = self.owner.sprite.x - self.owner.target.sprite.x
    #             dist_y = self.owner.sprite.y - self.owner.target.sprite.y
    #             dist = math.hypot(dist_x, dist_y)
    #             # if dist < self.owner.stats.gun_two_data['travel']:
    #             return dist
    #     return False

    # def can_ability_shoot(self, gun):
    #     if not self.global_cooldown:
    #         if self.owner.target:
    #             dist_x = self.owner.sprite.x - self.owner.target.sprite.x
    #             dist_y = self.owner.sprite.y - self.owner.target.sprite.y
    #             dist = math.hypot(dist_x, dist_y)
    #             # if dist < gun['travel']:
    #             return dist
    #     return False

    # def auto_attack(self):
    #     enemy_range = self.can_aa_shoot()
    #     if enemy_range:
    #         bullet_base = self.build_bullet(
    #             self.owner.stats.gun_two_data,
    #             self.owner.sprite.x,
    #             self.owner.sprite.y,
    #             self.owner.target.sprite.x,
    #             self.owner.target.sprite.y,
    #             enemy_range,
    #             self.owner.target,
    #         )
    #         play_sound(self.owner.stats.gun_two_data['gun_fire_sound'])
    #         self.thrown.append(Thrown(master, self, bullet_base))
    #         time = int(60.0 / bullet_base['rof'])
    #         self.trigger_aa_cooldown(time)
