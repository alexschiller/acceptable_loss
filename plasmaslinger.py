from baseskills import * # noqa
import math
from functools import partial
from utility import * # noqa

class LightningMelee(Melee):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(LightningMelee, self).__init__(master, ability, skill, package, start_x, start_y)
        self.travelled = 0

    def check_package_accuracy(self):
        play_sound(self.package['gun_fire_sound'])
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
                self.sprite.rotation = (math.degrees(math.atan2(self.target.sprite.y - self.sprite.y, self.target.sprite.x - self.sprite.x)) * -1) + 90
                ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.ability.owner.sprite.x, self.ability.owner.sprite.y, 50)
                self.sprite.x += ret[0]
                self.sprite.y += ret[1]
                self.range = 20
            else:
                self.sprite.rotation = (math.degrees(math.atan2(self.mouse_y - self.sprite.y, self.mouse_x - self.sprite.x)) * -1) + 90
                self.range = 20
        else:
            self.range = 20

    def transmitting(self):
        if self.hit:
            self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.ability.owner.sprite.x, self.ability.owner.sprite.y, self.package['velocity'])
        else:
            self.travelled = self.range
            self.end_transmission = True
            # return False

        # self.package['velocity'] += 1
        self.sprite.x -= self.ret[0]
        self.sprite.y -= self.ret[1]

        self.travelled += math.hypot(self.ret[0], self.ret[1])

        if self.travelled >= self.range:
            self.end_transmission = True

class Orb(object):
    def __init__(self, master, handler): # noqa
        self.master = master
        self.handler = handler
        self.sprite = pyglet.sprite.Sprite(load_image('orb.png'), self.handler.owner.sprite.x + 20, self.handler.owner.sprite.y + 20, batch=BarBatch)
        self.timer = 1
        self.ret = [0, 0]
        self.ret_x = 0
        self.ret_y = 0

    def update(self, plasma):
        self.sprite.scale = (plasma + 50) / 150
        self.timer -= 1
        if not self.timer:
            self.ret = calc_vel_xy(self.handler.owner.sprite.x, self.handler.owner.sprite.y, self.sprite.x, self.sprite.y, 2)
            self.update_ret()
            self.timer = random.randint(3, 5)
        self.sprite.x += self.ret_x
        self.sprite.y += self.ret_y

    def update_ret(self):
        self.ret_x += self.ret[0]
        if self.ret_x < -5:
            self.ret_x += 1
        elif self.ret_x > 5:
            self.ret_x -= 1
        self.ret_y += self.ret[1]
        if self.ret_y < -5:
            self.ret_y += 1
        elif self.ret_y > 5:
            self.ret_y -= 1

class PlasmaCore(Core):
    def __init__(self, master, handler):
        super(PlasmaCore, self).__init__(master, handler)
        self.spinner = pyglet.sprite.Sprite(load_image('light_box.png'), self.handler.owner.sprite.x + 20, self.handler.owner.sprite.y + 20, batch=BarBatch)
        self.bullets = 6
        self.max_bullets = 6
        self.reload_timer = 120
        self.reload_timer_max = 120
        self.lightning = []
        self.lightning_counter = 0
        self.white_dot = pyglet.image.create(2, 2, white_sprite)
        self.plasma = 100
        self.plasma_max = 100.0

    def create_dot(self, x, y):
        self.lightning.append(pyglet.sprite.Sprite(self.white_dot, x, y, batch=BarBatch))

    def create_lightning(self, start_x, start_y, dist=15, target=None):
        marker = [start_x, start_y]
        if not target:
            target = [marker[0] + random.randint(-100, 100), marker[1] + random.randint(-100, 100)]
        for i in range(int(dist * .3)):
            # counter += 1
            ret = calc_vel_xy(target[0], target[1], marker[0], marker[1], 5)
            marker[0] += ret[0] + random.randint(-1, 1)
            marker[1] += ret[1] + random.randint(-1, 1)
            self.create_dot(marker[0], marker[1])

    def update(self):
        if self.plasma <= 0:
            self.plasma = 1
        if self.plasma > self.plasma_max:
            self.plasma = self.plasma_max
        self.spinner.rotation += (22 * self.plasma / self.plasma_max + 3)
        self.spinner.x = self.handler.owner.sprite.x
        self.spinner.y = self.handler.owner.sprite.y
        if len(self.lightning):
            self.lightning_counter -= 1
            if not self.lightning_counter:
                self.lightning = []


class LDBreaker(Skill):
    def __init__(self, master, level, handler):
        super(LDBreaker, self).__init__(master, level, handler)
        self.img = load_image('strike.png')
        self.sound = load_sound('slash.wav')
        self.shield_sound = load_sound('shield_up.wav')

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                if self.level >= 4:
                    self.four()
                    if self.level >= 7:
                        self.seven()
                        if self.level >= 10:
                            self.ten()

                gun = self.handler.copy_gun()
                gun['image'] = self.img
                gun['gun_fire_sound'] = self.sound
                pmod = .5 + self.level * .05
                gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
                gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
                self.handler.core.plasma += 20
                LightningMelee(self.master, self.handler, self, gun, self.handler.owner.sprite.x, self.handler.owner.sprite.y)
                return True
            else:
                self.dash()
                return False
        except:
            return False

    def four(self):
        if random.randint(0, 100) >= 90:
            play_sound(self.shield_sound)
            self.handler.owner.stats.add_shield(self.handler.owner.stats.shield_max / 10.0)

    def seven(self):
        self.handler.core.plasma += 10

    def ten(self):
        if random.randint(0, 100) >= 90:
            play_sound(self.shield_sound)
            self.handler.owner.stats.add_shield(self.handler.owner.stats.shield_max)

# Unfinished
class LDCurrent(Skill):
    def __init__(self, master, level, handler):
        super(LDCurrent, self).__init__(master, level, handler)
        self.img = load_image('lightsword.png')
        self.sound = load_sound('slash.wav')

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                gun = self.handler.copy_gun()
                gun['image'] = self.img
                gun['gun_fire_sound'] = self.sound
                pmod = .5
                gun['armor_pierce'] += 10
                gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
                gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
                self.handler.core.plasma += 5
                LightningMelee(self.master, self.handler, self, gun, self.handler.owner.sprite.x, self.handler.owner.sprite.y)
                return True
            else:
                self.dash()
                return False
        except:
            return False

# Unfinished
class LDZap(Skill):
    def __init__(self, master, level, handler):
        super(LDZap, self).__init__(master, level, handler)
        self.gun_fire_sound = load_sound('lightning_bolt.wav')

    def fire(self):
        dist = self.get_enemy_dist()
        if dist and dist <= 600:
            self.handler.core.lightning_counter = 3
            self.handler.core.create_lightning(
                self.handler.owner.sprite.x,
                self.handler.owner.sprite.y,
                dist,
                [self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y]
            )

            # self.handler.core.bullets -= 1
            gun = self.handler.copy_gun()
            gun['accuracy'] += 100
            pmod = self.handler.core.plasma / self.handler.core.plasma_max * 3
            gun['gun_fire_sound'] = self.gun_fire_sound
            gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
            gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
            Gunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y)
            self.handler.core.plasma = 0
            return True
        return False

# Unfinished
class LDSpark(Skill):
    def __init__(self, master, level, handler):
        super(LDSpark, self).__init__(master, level, handler)
        self.gun_fire_sound = load_sound('lightning_bolt.wav')

    def fire(self):
        dist = self.get_enemy_dist()
        if dist:
            if dist <= 150:
                gun = self.handler.copy_gun()
                gun['accuracy'] += 100
                gun['gun_fire_sound'] = self.gun_fire_sound
                pmod = self.handler.core.plasma / self.handler.core.plasma_max
                gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
                gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
                self.add_strike(gun, dist)
                self.handler.delayed.append([10, partial(self.add_strike, gun, dist)])
                self.handler.delayed.append([20, partial(self.add_strike, gun, dist)])
                self.handler.core.plasma = 0
                return True
            else:
                self.dash()
        return False

    def add_strike(self, gun, dist):
        if self.handler.owner.target:
            self.handler.core.lightning_counter = 3
            self.handler.core.create_lightning(
                self.handler.owner.sprite.x,
                self.handler.owner.sprite.y,
                dist,
                [self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y]
            )
            Gunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y)

# Unfinished
class LDChainLightning(Skill):
    def __init__(self, master, level, handler):
        super(LDChainLightning, self).__init__(master, level, handler)

# Unfinished
class LDBallLightning(Skill):
    def __init__(self, master, level, handler):
        super(LDBallLightning, self).__init__(master, level, handler)

# Unfinished
class LDRepurpose(Skill):
    def __init__(self, master, level, handler):
        super(LDRepurpose, self).__init__(master, level, handler)
        self.sound = load_sound('repurpose.wav')

    def fire(self):
        if self.handler.owner.stats.shield and self.handler.core.plasma != self.handler.core.plasma_max:
            play_sound(self.sound)
            self.master.spriteeffect.teleport(self.handler.owner.sprite.x, self.handler.owner.sprite.y)
            self.handler.core.plasma += 50 * (self.handler.owner.stats.shield / self.handler.owner.stats.shield_max)
            self.handler.owner.stats.update_health(self.handler.owner.stats.shield)
            return True
        return False

# Unfinished
class LDEmpower(Skill):
    def __init__(self, master, level, handler):
        super(LDEmpower, self).__init__(master, level, handler)

# Unfinished
class LDZipZap(Skill):
    def __init__(self, master, level, handler):
        super(LDZipZap, self).__init__(master, level, handler)
        self.img = load_image('strike.png')
        self.sound = load_sound('slash.wav')

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                gun = self.handler.copy_gun()
                gun['image'] = self.img
                gun['gun_fire_sound'] = self.sound
                LightningMelee(self.master, self.handler, self, gun, self.handler.owner.sprite.x, self.handler.owner.sprite.y)
                return True
            else:
                self.dash()
                return False
        except:
            return False

    def dash(self):
        self.handler.owner.stats.temp_stat_change(2, 'speed', 10)
        self.handler.owner.stats.update_health(self.handler.owner.stats.shield)
        ret = calc_vel_xy(self.handler.owner.sprite.x, self.handler.owner.sprite.y,
        self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y, 45)
        self.handler.owner.controller.move_to(self.handler.owner.target.sprite.x + ret[0],
            self.handler.owner.target.sprite.y + ret[1], 1)

# Unfinished
class LDEnergize(Skill):
    def __init__(self, master, level, handler):
        super(LDEnergize, self).__init__(master, level, handler)

# Unfinished
class LDRedirect(Skill):
    def __init__(self, master, level, handler):
        super(LDRedirect, self).__init__(master, level, handler)

# Unfinished
class LDRepulse(Skill):
    def __init__(self, master, level, handler):
        super(LDRepulse, self).__init__(master, level, handler)

plasmaslinger_skillset = {
    'core': PlasmaCore,
    '1': LDBreaker,
    '2': LDCurrent,
    '3': LDZap,
    '4': LDSpark,
    '5': LDChainLightning,
    '6': LDBallLightning,
    '7': LDRepurpose,
    '8': LDEmpower,
    '9': LDZipZap,
    '10': LDEnergize,
    '11': LDRedirect,
    '12': LDRepulse,
}
