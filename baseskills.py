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

    def miss(self):
        pass

    def evade(self):
        pass

    def hit(self):
        pass

    def crit(self):
        pass

    def kill(self):
        pass

class BasicTrigger(Skill):
    def __init__(self, master, level, handler):
        super(BasicTrigger, self).__init__(master, level, handler)

class Transmission(object):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        self.master = master
        self.ability = ability
        self.skill = skill
        self.package = package
        self.ability.transmissions.append(self)
        self.end_transmission = False
        self.mouse_x = self.master.player_controller.sprite.x
        self.mouse_y = self.master.player_controller.sprite.y
        self.start_x = start_x
        self.start_y = start_y
        self.ret = [10, 10]
        self.x = None
        self.y = None
        self.hit = False
        self.crit = False
        self.evade = False
        self.kill = False
        self.sprite = pyglet.sprite.Sprite(self.package['image'], self.start_x, self.start_y, batch=BulletBatch)
        self.check_package_accuracy()

    def transmit(self):
        self.transmitting()
        self.check_end_transmission()

    def transmitting(self):
        pass

    def check_end_transmission(self):
        if self.end_transmission:
            self.pass_package()

    def pass_package(self):
        self.ability.packages.append(self)
        self.ability.transmissions.remove(self)

    def check_package_accuracy(self):
        self.evade = 0
        self.hit = 1
        self.crit = 0

    def unpack(self):
        pass

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

    def backtransmit(self, miss, evade, hit, crit, kill):
        if miss:
            self.skill.miss()
            for o in self.ability.outcomes['miss']:
                o.fire()

        if evade:
            self.skill.evade()
            for o in self.ability.outcomes['evade']:
                o.fire()

        if hit:
            self.skill.hit()
            for o in self.ability.outcomes['hit']:
                o.fire()

        if crit:
            self.skill.crit()
            for o in self.ability.outcomes['crit']:
                o.fire()

        if kill:
            self.skill.kill()
            for o in self.ability.outcomes['kill']:
                o.fire()

    def cleanup(self):
        self.sprite.delete()
        self.ability.packages.remove(self)
        del self

class PlayerGunshot(Transmission):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(PlayerGunshot, self).__init__(master, ability, skill, package, start_x, start_y)
        self.travelled = 0

    def transmitting(self):
        if self.hit:
            self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.sprite.x, self.sprite.y, self.package['velocity'])
            self.sprite.rotation = (math.degrees(math.atan2(self.target.sprite.y - self.sprite.y, self.target.sprite.x - self.sprite.x)) * -1) + 90
        else:
            self.ret = calc_vel_xy(self.mouse_x, self.mouse_y, self.sprite.x, self.sprite.y, self.package['velocity'])
            self.sprite.rotation = (math.degrees(math.atan2(self.mouse_y - self.sprite.y, self.mouse_x - self.sprite.x)) * -1) + 90
        self.sprite.x += self.ret[0]
        self.sprite.y += self.ret[1]
        self.travelled += math.hypot(self.ret[0], self.ret[1])
        if self.travelled >= self.range:
            self.end_transmission = True

    def check_package_accuracy(self):
        self.target = self.ability.owner.target
        if self.target:
            self.hit = random.randint(0, 100) < self.package['accuracy'] * self.ability.owner.acc_mouse_mod
            if self.hit and random.randint(0, 100) < self.package['crit']:
                self.crit = True
                self.package['damage_min'] = self.package['damage_min'] * self.package['crit_damage']
                self.package['damage_max'] = self.package['damage_max'] * self.package['crit_damage']

            if self.hit and random.randint(0, 100) < self.target.stats.evade:
                self.evade = True

            if self.hit:
                self.range = math.hypot(self.sprite.x - self.target.sprite.x, self.sprite.y - self.target.sprite.y)
            else:
                self.range = math.hypot(self.sprite.x - self.mouse_x, self.sprite.y - self.mouse_y)
        else:
            self.range = math.hypot(self.sprite.x - self.mouse_x, self.sprite.y - self.mouse_y)

    def unpack(self):
        if self.target and self.hit:
            self.damage = random.randint(self.package['damage_min'], self.package['damage_max'])
            self.target.on_hit(self)
        self.display_outcome()
        self.backtransmit(not(self.hit), self.evade, self.hit, self.crit, self.kill)
        try:
            self.cleanup()
        except Exception, e:
            print e

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

class NoAccMelee(object):
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
