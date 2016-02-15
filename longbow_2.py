from pyglet.gl import *  # noqa
from collide import *  # noqa
from utility import *  # noqa
from character import *  # noqa

import pyglet
from gun import *  # noqa
from functools import partial # noqa
from ability import *  # noqa
# import random


class AoeThrown(Thrown):
    def __init__(self, *args, **kwargs):
        super(AoeThrown, self).__init__(*args, **kwargs)

    def aoe(self):
        self.hit = True
        b_x = self.sprite.x
        b_y = self.sprite.y
        self.master.spriteeffect.explosion(b_x, b_y)
        for e in self.owner.owner.enemies:
            if abs(math.hypot(b_x - e.sprite.x, b_y - e.sprite.y)) < 100:
                e.on_hit(self)
                self.display_outcome()

    def delete_thrown(self):
        self.display_outcome()
        self.aoe()
        play_sound(self.owner.sound_explosion)
        self.sprite.delete()
        self.owner.thrown.remove(self)

class LongbowAbility(Ability):
    def __init__(self, *args, **kwargs):
        super(LongbowAbility, self).__init__(*args, **kwargs)
        self.bul = 30
        self.mis = 10
        self.bul_max = 30
        self.mis_max = 10

        self.g1b = 10
        self.g1b_max = 10
        self.g1b_reload = 0
        self.gun_one_bullets = []
        self.g1b_len = self.g1b_max * 4
        self.g1b_bar = pyglet.sprite.Sprite(
            pyglet.image.create(self.g1b_len, 13, orange_sprite),
            11, window_height - 139, batch=BarBatch)
        for i in range(self.g1b):
            self.gun_one_bullets.append(pyglet.sprite.Sprite(load_image('s_bullet.png', anchor=False), 11 + i * 4, window_height - 140, batch=gfx_batch))  # noqa)

        self.g2b = 50
        self.g2b_max = 50
        self.g2b_reload = 0
        self.gun_two_bullets = []
        self.g2b_len = self.g2b_max * 4
        self.g2b_bar = pyglet.sprite.Sprite(
            pyglet.image.create(self.g2b_len, 13, orange_sprite),
            11, window_height - 152, batch=BarBatch)
        for i in range(self.g2b):
            self.gun_two_bullets.append(pyglet.sprite.Sprite(load_image('s_bullet.png', anchor=False), 11 + i * 4, window_height - 153, batch=gfx_batch))  # noqa)

        self.opp_bar = pyglet.sprite.Sprite(
            pyglet.image.create(15, 90, orange_sprite),
            window_width - 472, 5, batch=BarBatch)

        self.vul_bar = pyglet.sprite.Sprite(
            pyglet.image.create(20, 90, red_sprite),
            window_width - 440, 5, batch=BarBatch)

        self.sound_explosion = load_sound('explosion.wav')
        self.sound_missile = load_sound('missile.wav')

        self.vat = pyglet.sprite.Sprite(load_image('autoloader.png', anchor=False), window_width-472, 0, batch=gfx_batch),  # noqa

    def update_ammo(self):
        if self.bul < self.bul_max:
            self.bul += .01
        if self.mis < self.mis_max:
            self.mis += .005

        if not self.g1b:
            self.g1b_reload = 1
        if self.g1b_reload:
            self.g1b += .1
            if self.g1b >= self.g1b_max:
                self.g1b = self.g1b_max
                self.g1b_reload = 0

        if not self.g2b:
            self.g2b_reload = 1
        if self.g2b_reload:
            self.g2b += .1
            if self.g2b >= self.g2b_max:
                self.g2b = self.g2b_max
                self.g2b_reload = 0

    # def can_aa_shoot(self):
    #     if not self.aa_cooldown:
    #         x = self.owner.controller.target_closest_enemy()
    #         print x
    #         if x:
    #             dist_x = self.owner.sprite.x - self.owner.target.sprite.x
    #             dist_y = self.owner.sprite.y - self.owner.target.sprite.y
    #             dist = math.hypot(dist_x, dist_y)
    #             if dist < self.owner.stats.gun_two_data['travel']:
    #                 return dist
    #     return False

    def auto_attack(self):
        enemy_range = self.can_aa_shoot()
        if enemy_range:
            bullet_base = self.build_bullet(
                self.owner.stats.generate_gun(self.owner.stats.gun_two),
                self.owner.sprite.x,
                self.owner.sprite.y,
                self.owner.target.sprite.x,
                self.owner.target.sprite.y,
                enemy_range,
                self.owner.target,
            )
            if not self.g1b_reload:
                play_sound(self.owner.stats.gun_two_data['gun_fire_sound'])
                bullet_base['accuracy'] *= self.owner.acc_mouse_mod
                self.thrown.append(Thrown(master, self, bullet_base))
                self.g1b -= 1
                time = int(60.0 / bullet_base['rof'])
                self.trigger_aa_cooldown(time)
                if random.choice([0, 0, 0, 1]):
                    self.mini_missile_launch()

    def update(self):
        # self.update_delayed()
        self.update_ammo()

        for t in self.thrown:
            t.update()

        self.g1b_bar.x = 11 - (self.g1b_len - (self.g1b / float(self.g1b_max) * self.g1b_len)) # noqa
        self.g2b_bar.x = 11 - (self.g2b_len - (self.g2b / float(self.g2b_max) * self.g2b_len)) # noqa

        self.opp_bar.y = 5 - (90 - (self.bul / float(self.bul_max) * 90)) # noqa
        self.vul_bar.y = 5 - (90 - (self.mis / float(self.mis_max) * 90)) # noqa

    def action_checks(self, bul, mis):
        if self.owner.target:
            if not self.global_cooldown:
                if self.bul >= bul and self.mis >= mis:
                    return True
        return False

    def enemy_in_range(self, enemy, gun):
            dist_x = self.owner.sprite.x - enemy.sprite.x
            dist_y = self.owner.sprite.y - enemy.sprite.y
            dist = math.hypot(dist_x, dist_y)
            # if dist < gun['travel']:
            return dist

    def add_bullet(self, bullet_base):
        self.thrown.append(Thrown(master, self, bullet_base))

    def mini_missile_launch(self):
            enemy_range = self.can_ability_shoot(self.owner.stats.gun_one_data)
            if enemy_range:
                play_sound(self.sound_missile)
                bullet_base = self.build_bullet(
                    self.owner.stats.gun_one_data,
                    self.owner.sprite.x,
                    self.owner.sprite.y,
                    self.owner.target.sprite.x,
                    self.owner.target.sprite.y,
                    enemy_range,
                    self.owner.target,)
                bullet_base['velocity'] = 15
                bullet_base['image'] = load_image('small_missile.png')
                # bullet_base['damage_min'] = bullet_base['damage_min'] / 2.0
                # bullet_base['damage_max'] = bullet_base['damage_max'] / 2.0
                bullet_base['enemy_range'] -= 50
                self.thrown.append(AoeThrown(master, self, bullet_base))

    def missile_launch(self):
        if self.action_checks(0, 1):
            enemy_range = self.can_ability_shoot(self.owner.stats.gun_one_data)
            if enemy_range:
                play_sound(self.sound_missile)
                bullet_base = self.build_bullet(
                    self.owner.stats.gun_one_data,
                    self.owner.sprite.x,
                    self.owner.sprite.y,
                    self.owner.target.sprite.x,
                    self.owner.target.sprite.y,
                    enemy_range,
                    self.owner.target,)
                bullet_base['velocity'] = 25
                bullet_base['enemy_range'] -= 50
                self.thrown.append(AoeThrown(master, self, bullet_base))
                self.trigger_global_cooldown()
                self.mis -= 1