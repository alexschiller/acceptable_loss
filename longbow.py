from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa
from functools import partial # noqa
from ability import * # noqa
# import random

class BolaEffect(object):
    def __init__(self, master, owner, start_x, start_y, target_x, target_y): # noqa
        self.sprite = pyglet.sprite.Sprite(load_image('bola.png'), start_x, start_y, batch=gfx_batch) # noqa
        self.travel = 200 + random.randint(-50, 50)
        self.master = master
        self.owner = owner
        self.target_x = target_x
        self.target_y = target_y
        self.start_x = start_x
        self.start_y = start_y
        ret = calc_vel_xy(target_x, target_y,
            start_x, start_y, random.randint(7, 10))

        self.vel_x = ret[0] + random.randint(-2, 2)
        self.vel_y = ret[1] + random.randint(-2, 2)

        self.travelled = 0

    def remove_bola(self):
        self.master.spriteeffect.bola_explosion(self.sprite.x, self.sprite.y)
        try:
            self.sprite.delete()
            self.owner.thrown.remove(self)
        except:
            pass

    def get_target(self):
        try:
            min_dist = 300  # must be within 300 of the bola
            x1 = self.sprite.x
            y1 = self.sprite.y
            self.target = None
            for e in self.owner.owner.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    self.target = e
            return min_dist
        except:
            self.target = None

    def shoot(self):
        enemy_range = self.get_target()
        if self.target:
            bullet_base = self.owner.build_bullet(
                self.owner.gun_one,
                self.sprite.x,
                self.sprite.y,
                self.target.sprite.x,
                self.target.sprite.y,
                enemy_range,
                self.target,)
            bullet_base['damage']
            bullet_base['image'] = self.owner.plasma_shot
            self.owner.thrown.append(Thrown(self.master, self.owner, bullet_base))
        self.remove_bola()

    def update(self):
        self.sprite.rotation += 5
        try:
            self.sprite.x += self.vel_x
            self.sprite.y += self.vel_y
            self.travelled += math.hypot(self.vel_x, self.vel_y)
            if self.travelled > self.travel:
                self.shoot()
        except:
            pass

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
                self.enemy.on_hit(self)
                self.display_outcome()

    def delete_thrown(self):
        self.display_outcome()
        self.aoe()
        self.sprite.delete()
        self.owner.thrown.remove(self)

class LongbowAbility(Ability):
    def __init__(self, *args, **kwargs):
        super(LongbowAbility, self).__init__(*args, **kwargs)
        self.bul = 30
        self.mis = 10
        self.bul_max = 30
        self.mis_max = 10

        self.vat = pyglet.sprite.Sprite(load_image('autoloader.png', anchor=False), window_width-472, 0, batch=gfx_batch),  # noqa

    def update_ammo(self):
        if self.bul < self.bul_max:
            self.bul += .01
        if self.mis < self.mis_max:
            self.mis += .005

    def update(self):
        self.update_delayed()
        self.update_ammo()

        for t in self.thrown:
            t.update()

        oh = int(max(90 * self.bul / self.bul_max, 1))
        self.opp_bar = pyglet.sprite.Sprite(
            pyglet.image.create(15, oh, orange_sprite),
            window_width - 472, 5, batch=BarBatch)

        vh = int(max(90 * round(self.mis / self.mis_max, 1), 1))
        self.vul_bar = pyglet.sprite.Sprite(
            pyglet.image.create(20, vh, red_sprite),
            window_width - 440, 5, batch=BarBatch)

    def action_checks(self, bul, mis):
        if self.owner.target:
            if not self.global_cooldown:
                if self.bul >= bul and self.mis >= mis:
                    return True
        return False

    # def update_plasma(self):
    #     if self.plasma < self.max_plasma:
    #         self.plasma += .3 * self.plasma / self.max_plasma + .05
    #     else:
    #         self.plasma = self.max_plasma

    def enemy_in_range(self, enemy, gun):
            dist_x = self.owner.sprite.x - enemy.sprite.x
            dist_y = self.owner.sprite.y - enemy.sprite.y
            dist = math.hypot(dist_x, dist_y)
            if dist < gun['travel']:
                return dist
            return False

    def add_bullet(self, bullet_base):
        self.thrown.append(Thrown(master, self, bullet_base))

    def missile_launch(self):
        if self.action_checks(0, 1):
            enemy_range = self.can_ability_shoot(self.gun_one)
            if enemy_range:
                bullet_base = self.build_bullet(
                    self.gun_one,
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

    def missile_everyone(self):
        if self.action_checks(0, 1):
            enemy_range = self.can_ability_shoot(self.gun_one)
            if enemy_range:
                bullet_base = self.build_bullet(
                    self.gun_one,
                    self.owner.sprite.x,
                    self.owner.sprite.y,
                    self.owner.target.sprite.x,
                    self.owner.target.sprite.y,
                    enemy_range,
                    self.owner.target,)
                bullet_base['velocity'] = 25
                self.thrown.append(AoeThrown(master, self, bullet_base))
                self.trigger_global_cooldown()
                self.mis -= 1
