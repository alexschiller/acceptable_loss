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

    def dash(self):
        ret = calc_vel_xy(self.handler.owner.sprite.x, self.handler.owner.sprite.y,
        self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y, 45)
        self.handler.owner.controller.move_to(self.handler.owner.target.sprite.x + ret[0],
            self.handler.owner.target.sprite.y + ret[1], 1)

    def get_enemy_dist(self):
        if self.handler.owner.target:
            dist_x = self.handler.owner.sprite.x - self.handler.owner.target.sprite.x
            dist_y = self.handler.owner.sprite.y - self.handler.owner.target.sprite.y
            dist = math.hypot(dist_x, dist_y)
            return dist
        return False

class Transmission(object):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        self.master = master
        self.ability = ability
        self.skill = skill
        self.package = package
        self.ability.transmissions.append(self)
        self.end_transmission = False
        self.mouse_x = 0
        self.mouse_y = 0
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
        self.check_end_transmission()
        self.transmitting()

    def transmitting(self):
        pass

    def check_end_transmission(self):
        if self.end_transmission:
            self.pass_package()

    def pass_package(self):
        self.ability.packages.append(self)
        self.ability.transmissions.remove(self)

    def check_package_accuracy(self):
        self.target = self.ability.owner.target
        if self.target:
            self.hit = random.randint(0, 100) < self.package['accuracy']
            if self.hit and random.randint(0, 100) < self.package['crit']:
                self.crit = True
                self.package['damage_min'] = int(self.package['damage_min'] * self.package['crit_damage'])
                self.package['damage_max'] = int(self.package['damage_max'] * self.package['crit_damage'])

            if self.hit and random.randint(0, 100) < self.target.stats.evade:
                self.evade = True

            if self.hit:
                self.range = math.hypot(self.sprite.x - self.target.sprite.x, self.sprite.y - self.target.sprite.y)
            else:
                self.range = math.hypot(self.sprite.x - self.target.sprite.x + random.randint(-5, 5), self.sprite.y - self.target.sprite.y + random.randint(-5, 5))
        else:
            self.range = math.hypot(self.sprite.x - self.sprite.x + random.randint(-20, 20), self.sprite.y - self.sprite.y + random.randint(-20, 20))

    def unpack(self):
        if self.target and self.hit:
            if self.package['damage_min'] < self.package['damage_max']:
                self.damage = random.randint(self.package['damage_min'], self.package['damage_max'])
            else:
                self.damage = random.randint(self.package['damage_min'], self.package['damage_min'] + 1)
            self.target.on_hit(self)
        self.display_outcome()
        self.backtransmit(not(self.hit), self.evade, self.hit, self.crit, self.kill)
        try:
            self.cleanup()
        except Exception, e:
            print e

    def display_outcome(self):
        play_sound(self.package['on_hit_sound'])
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
        try:
            self.sprite.delete()
        except:
            pass
        try:
            self.ability.transmissions.remove(self)
        except:
            pass
        try:
            self.ability.packages.remove(self)
        except:
            pass
        try:
            del self
        except:
            pass

class Gunshot(Transmission):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(Gunshot, self).__init__(master, ability, skill, package, start_x, start_y)
        self.travelled = 1
        try:
            play_sound(self.package['gun_fire_sound'])
        except:
            pass

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

class Melee(Transmission):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(Melee, self).__init__(master, ability, skill, package, start_x, start_y)
        self.travelled = 0
        self.stab = 1

    def transmitting(self):

        if self.hit:
            self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.sprite.x, self.sprite.y, self.package['velocity'])
        else:
            self.ret = calc_vel_xy(self.mouse_x, self.mouse_y, self.sprite.x, self.sprite.y, self.package['velocity'])

        if self.stab:
            self.sprite.x += self.ret[0]
            self.sprite.y += self.ret[1]
            self.package['velocity'] -= 1
        else:
            self.package['velocity'] += 1
            self.sprite.x -= self.ret[0]
            self.sprite.y -= self.ret[1]

        self.travelled += math.hypot(self.ret[0], self.ret[1])

        if self.travelled >= self.range / 2:
            self.stab = 0

        if self.travelled >= self.range:
            self.end_transmission = True

    def check_package_accuracy(self):
        self.target = self.ability.owner.target
        if self.target:
            self.hit = random.randint(0, 100) < self.package['accuracy']
            if self.hit and random.randint(0, 100) < self.package['crit']:
                self.crit = True
                self.package['damage_min'] = int(self.package['damage_min'] * self.package['crit_damage'])
                self.package['damage_max'] = int(self.package['damage_max'] * self.package['crit_damage'])

            if self.hit and random.randint(0, 100) < self.target.stats.evade:
                self.evade = True

            if self.hit:
                    self.sprite.rotation = (math.degrees(math.atan2(self.target.sprite.y - self.sprite.y, self.target.sprite.x - self.sprite.x)) * -1) + 90
                    self.range = 100
            else:
                self.sprite.rotation = (math.degrees(math.atan2(self.mouse_y - self.sprite.y, self.mouse_x - self.sprite.x)) * -1) + 90
                self.range = 100
        else:
            self.range = 100

class PlayerGunshot(Gunshot):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(PlayerGunshot, self).__init__(master, ability, skill, package, start_x, start_y)

    def check_package_accuracy(self):
        self.mouse_x = self.master.player_controller.sprite.x
        self.mouse_y = self.master.player_controller.sprite.y
        self.target = self.ability.owner.target
        if self.target:
            self.hit = random.randint(0, 100) < self.package['accuracy'] * self.ability.owner.acc_mouse_mod
            if self.hit and random.randint(0, 100) < self.package['crit']:
                self.crit = True
                self.package['damage_min'] = int(self.package['damage_min'] * self.package['crit_damage'])
                self.package['damage_max'] = int(self.package['damage_max'] * self.package['crit_damage'])

            if self.hit and random.randint(0, 100) < self.target.stats.evade:
                self.evade = True

            if self.hit:
                self.range = math.hypot(self.sprite.x - self.target.sprite.x, self.sprite.y - self.target.sprite.y)
            else:
                self.range = math.hypot(self.sprite.x - self.mouse_x, self.sprite.y - self.mouse_y)
        else:
            self.range = math.hypot(self.sprite.x - self.mouse_x, self.sprite.y - self.mouse_y)

class NoTargetGunshot(Gunshot):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(NoTargetGunshot, self).__init__(master, ability, skill, package, start_x, start_y)

    def check_package_accuracy(self):
        self.target = self.closest_enemy(self.start_x, self.start_y)
        if not self.target:
            self.cleanup()
            return False

        self.hit = random.randint(0, 100) < self.package['accuracy']
        if self.hit and random.randint(0, 100) < self.package['crit']:
            self.crit = True
            self.package['damage_min'] = int(self.package['damage_min'] * self.package['crit_damage'])
            self.package['damage_max'] = int(self.package['damage_max'] * self.package['crit_damage'])

        if self.hit and random.randint(0, 100) < self.target.stats.evade:
            self.evade = True

        if self.hit:
            self.range = math.hypot(self.sprite.x - self.target.sprite.x, self.sprite.y - self.target.sprite.y)
        else:
            self.range = math.hypot(self.sprite.x - self.target.sprite.x + random.randint(-5, 5), self.sprite.y - self.target.sprite.y + random.randint(-5, 5))

    def closest_enemy(self, x, y):
        target = None
        try:
            min_dist = 1000
            x1 = x
            y1 = y
            if len(self.ability.owner.enemies) == 0:
                return False
            for e in self.ability.owner.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    target = e
            return target
        except:
            return False

class BasicTrigger(Skill):
    def __init__(self, master, level, handler):
        super(BasicTrigger, self).__init__(master, level, handler)

    def fire(self):
        if not self.handler.global_cooldown:
            Gunshot(self.master, self.handler, self, self.handler.copy_gun(), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
            return True
        return False

    def get_enemy_dist(self):
        if self.handler.owner.target:
            dist_x = self.handler.owner.sprite.x - self.handler.owner.target.sprite.x
            dist_y = self.handler.owner.sprite.y - self.handler.owner.target.sprite.y
            dist = math.hypot(dist_x, dist_y)
            return dist
        return False
