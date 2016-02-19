import math # noqa
import random
from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet
# import itertools
from collide import * # noqa

class Core(object):
    def __init__(self, master, handler):
        self.master = master
        self.handler = handler

    def update(self):
        pass

class Skill(object):
    def __init__(self, master, level, handler):
        self.master = master
        self.handler = handler
        self.level = level
        self._cooldown = 30

    def fire(self):
        pass

    @property
    def cooldown(self):
        return self._cooldown

    def update(self):
        if self._cooldown:
            self._cooldown -= 1

class BasicTrigger(Skill):
    def __init__(self, master, level, handler):
        super(BasicTrigger, self).__init__(master, level, handler)

    def fire(self):
        enemy_range = self.get_enemy_dist()
        if enemy_range and not self.handler.global_cooldown:
            bullet_base = self.handler.build_bullet(
                self.handler.owner.stats.gun_one_data,
                self.handler.owner.sprite.x,
                self.handler.owner.sprite.y,
                self.handler.owner.target.sprite.x,
                self.handler.owner.target.sprite.y,
                enemy_range,
                self.handler.owner.target,
            )

            # play_sound(self.owner.stats.gun_one_data['gun_fire_sound'])
            self.handler.thrown.append(Thrown(self.master, self.handler, bullet_base))
            self.handler.owner.stats.recoil += self.handler.owner.stats.gun_one_data['recoil']
            self._cooldown = 120
            return True
        return False

    def get_enemy_dist(self):
        if self.handler.owner.target:
            dist_x = self.handler.owner.sprite.x - self.handler.owner.target.sprite.x
            dist_y = self.handler.owner.sprite.y - self.handler.owner.target.sprite.y
            dist = math.hypot(dist_x, dist_y)
            return dist
        return False


class Thrown(object):
    def __init__(self, master, ability, base):  # noqa
        # Base stats
        self.master = master
        self.owner = ability
        self.base = base
        self.damage_min = self.base['damage_min']
        self.damage_max = self.base['damage_max']
        self.velocity = self.base['velocity']
        self.accuracy = self.base['accuracy'] * self.owner.owner.acc_mouse_mod
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
            self.vel_x = ret[0] + random.randint(-2, 2)
            self.vel_y = ret[1] + random.randint(-2, 2)

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
                self.enemy.on_hit(self)
            self.delete_thrown()


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
        # play_sound(self.owner.sound_explosion)
        self.sprite.delete()
        self.owner.thrown.remove(self)


class Melee(object):
    def __init__(self, master, ability, base):  # noqa
        # Base stats
        self.master = master
        self.owner = ability
        self.base = base
        self.damage_min = self.base['damage_min']
        self.damage_max = self.base['damage_max']
        self.velocity = self.base['velocity']
        self.accuracy = self.base['accuracy'] * self.owner.owner.acc_mouse_mod
        self.crit_chance = self.base['crit']
        self.crit_damage = self.base['crit_damage']
        self.enemy_range = self.base['enemy_range']
        self.target_x = self.base['target_x'] - 50
        self.target_y = self.base['target_y'] - 50
        self.enemy = self.base['enemy']
        img = self.base['image']
        self.travelled = 0
        self.vel_x = 100
        self.vel_y = 100
        self.draw_time = 4
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
            self.target_x, self.target_y, batch=BulletBatch)

        # self.sprite.rotation = random.randint(0, 365)
        self.sprite.scale = 1

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
        self.draw_time -= 1
        self.sprite.x += 20
        self.sprite.y += 20
        self.sprite.rotation += 5
        # self.sprite.scale += .2
        if not self.draw_time:
            if self.hit and not self.evade:
                self.enemy.on_hit(self)
            self.delete_thrown()
