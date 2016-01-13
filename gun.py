from pyglet.gl import * # noqa
from collide import * # noqa
import random
from utility import * # noqa
import pyglet
import math
# import itertools
from collide import * # noqa

class Bullet(object):
    def __init__(self, base, start_x, start_y, target_x, target_y, enemy_range, enemy):  # noqa
        # Base stats
        self.base = base
        self.damage = self.base['damage']
        self.travel = self.base['travel']
        self.velocity = self.base['velocity']
        self.accuracy = self.base['accuracy']
        self.knockback = self.base['knockback']
        self.crit_chance = self.base['crit_chance']
        self.crit_multiplier = self.base['crit_multiplier']
        self.enemy_range = enemy_range
        self.enemy = enemy
        self.travelled = 0

        # Calculate shit here
        self.crit = False
        self.hit = random.randint(0, 100) < self.accuracy

        if self.hit and random.randint(0, 100) < self.crit_chance:
            self.crit = True
            self.damage = self.damage * self.crit_multiplier

        self.sprite = pyglet.sprite.Sprite(base['image'],
            start_x, start_y, batch=BulletBatch)

        dist_x = target_x - float(start_x)
        dist_y = target_y - float(start_y)

        self.sprite.rotation = (math.degrees(math.atan2(dist_y, dist_x)) * -1) + 90
        self.sprite.scale = 1

        ret = calc_vel_xy(target_x, target_y,
            start_x, start_y, self.velocity)

        if self.hit:
            self.vel_x = ret[0]
            self.vel_y = ret[1]
        else:
            self.vel_x = ret[0] + random.choice([-1, 1])
            self.vel_y = ret[1] + random.choice([-1, 1])

    def update(self):
        self.sprite.x += self.vel_x
        self.sprite.y += self.vel_y
        self.travelled += math.hypot(self.vel_x, self.vel_y)


class Gun(object):
    def __init__(self, master, base): # noqa
        self.base = base
        self.rof = 60 / self.base['rof']
        self.rofl = 0
        self.bullets = []
        self.master = master
        self.travel = self.base['travel']

        self.gun_fire_sound = self.base['gun_fire_sound']
        self.on_hit_sound = self.base['on_hit_sound']

    def fire(self, start_x, start_y, target_x, target_y, enemy):
        dist_x = start_x - target_x
        dist_y = start_y - target_y
        enemy_range = math.hypot(dist_x, dist_y)

        if self.can_fire(enemy_range):
            play_sound(self.gun_fire_sound)
            self.bullets.append(Bullet(self.base, start_x, start_y, target_x, target_y, enemy_range, enemy)) # noqa
            return True

    def can_fire(self, enemy_range):
        if enemy_range <= self.travel:
            if self.rofl == self.rof:
                self.rofl -= self.rof
                return True
        return False

    def delete_bullet(self, bullet):
        try:
            self.display_bullet_outcome(bullet, bullet.sprite.x, bullet.sprite.y)
            bullet.sprite.delete()
            self.bullets.remove(bullet)
        except:
            pass

    def display_bullet_outcome(self, bullet, x, y):
        if bullet.crit:
            self.master.spriteeffect.bullet_crit(x, y, bullet.damage) # noqa
        elif bullet.hit:
            self.master.spriteeffect.bullet_hit(x, y, bullet.damage) # noqa
        else:
            self.master.spriteeffect.bullet_miss(x, y, 'miss') # noqa

    def update_rof(self):
        if self.rofl < self.rof:
            self.rofl += 1

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.travelled > bullet.enemy_range:
                if bullet.hit:
                    try:
                        bullet.enemy.on_hit(bullet)
                    except:
                        pass
                self.delete_bullet(bullet)

    def update(self):
        self.update_rof()
        self.update_bullets()

class AOEGun(Gun):
    def __init__(self, *args, **kwargs):
        super(AOEGun, self).__init__(*args, **kwargs)

    def delete_bullet(self, bullet):

        self.display_bullet_outcome(bullet, bullet.sprite.x, bullet.sprite.y)
        self.explode(bullet)

    def explode(self, bullet):
        if not bullet.hit:
            bullet.hit = True

        b_x = bullet.sprite.x
        b_y = bullet.sprite.y
        self.master.spriteeffect.explosion(b_x, b_y)

        for e in self.master.enemies:
            if abs(math.hypot(b_x - e.sprite.x, b_y - e.sprite.y)) < 100:
                self.display_bullet_outcome(bullet, e.sprite.x, e.sprite.y)

                e.on_aoe_hit(bullet.damage)
        try:
            bullet.sprite.delete()
            self.bullets.remove(bullet)
        except:
            pass

# Sample guns
red_laser = {
    'damage': 1,
    'travel': 300,
    'velocity': 25,
    'accuracy': 85,
    'rof': 10,
    'knockback': 1,
    'crit_chance': 5,
    'crit_multiplier': 2,
    'image': load_image('red_laser.png'),
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
    'effects': [],
}

sniper = {
    'damage': 5,
    'travel': 800,
    'velocity': 100,
    'accuracy': 95,
    'rof': 1,
    'knockback': 50,
    'crit_chance': 50,
    'crit_multiplier': 6,
    'image': load_image('snipe.png'),
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
    'effects': [],
}


missile = {
    'damage': 2,
    'travel': 400,
    'velocity': 25,
    'accuracy': 95,
    'rof': 1,
    'knockback': 1,
    'crit_chance': 5,
    'crit_multiplier': 2,
    'image': load_image('missile.png'),
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
    'effects': [],
}

rocket = {
    'damage': 3,
    'travel': 400,
    'velocity': 25,
    'accuracy': 0,
    'rof': 1,
    'knockback': 1,
    'crit_chance': 5,
    'crit_multiplier': 2,
    'image': load_image('missile.png'),
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
    'effects': [],
}
