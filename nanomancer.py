from baseskills import * # noqa
import math
from functools import partial
from utility import * # noqa

class SpectreMelee(Melee):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(SpectreMelee, self).__init__(master, ability, skill, package, start_x, start_y)

    def check_package_accuracy(self):
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
                    self.range = 50
            else:
                self.sprite.rotation = (math.degrees(math.atan2(self.mouse_y - self.sprite.y, self.mouse_x - self.sprite.x)) * -1) + 90
                self.range = 50
        else:
            self.range = 50

    def display_outcome(self):
        play_sound(self.package['on_hit_sound'])
        x = self.sprite.x
        y = self.sprite.y
        if self.evade:
            self.master.spriteeffect.bullet_evade(x, y, 'evade') # noqa
        elif self.crit:
            self.master.spriteeffect.bullet_crit(x, y, self.damage) # noqa
            self.ability.core.add_chaos()
        elif self.hit:
            self.master.spriteeffect.bullet_hit(x, y, self.damage) # noqa
            self.ability.core.add_order()
        else:
            self.master.spriteeffect.bullet_miss(x, y, 'miss') # noqa   

class AnarchyShot(Gunshot):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(AnarchyShot, self).__init__(master, ability, skill, package, start_x, start_y)
        self.travelled = 1

    def check_package_accuracy(self):
        play_sound(self.package['on_hit_sound'])
        self.target = self.closest_enemy(self.start_x, self.start_y)
        if self.target:
            self.hit = True
            if self.hit and random.randint(0, 100) < self.package['crit']:
                self.crit = True
                self.package['damage_min'] = int(self.package['damage_min'] * self.package['crit_damage'])
                self.package['damage_max'] = int(self.package['damage_max'] * self.package['crit_damage'])

            if self.hit and random.randint(0, 100) < self.target.stats.evade:
                self.evade = True

            if self.hit:
                self.range = 0
            else:
                self.range = 0
        else:
            self.range = 0

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

class HomingShot(Gunshot):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(HomingShot, self).__init__(master, ability, skill, package, start_x, start_y)
        self.travelled = 1
        self.ret = [0, 0]
        self.ret_x = random.randint(-10, 10)
        self.ret_y = random.randint(-10, 10)
        self.tracking = 1

    def transmitting(self):
        if self.tracking:
            if self.hit:
                self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.sprite.x, self.sprite.y, 1)
                self.sprite.rotation = (math.degrees(math.atan2(self.target.sprite.y - self.sprite.y, self.target.sprite.x - self.sprite.x)) * -1) + 90
            else:
                self.ret = calc_vel_xy(self.mouse_x, self.mouse_y, self.sprite.x, self.sprite.y, 1)
                self.sprite.rotation = (math.degrees(math.atan2(self.mouse_y - self.sprite.y, self.mouse_x - self.sprite.x)) * -1) + 90
            self.update_ret()
            self.sprite.x += self.ret_x
            self.sprite.y += self.ret_y

        if math.hypot(self.target.sprite.x - self.sprite.x, self.target.sprite.y - self.sprite.y) < 10:
            self.end_transmission = True

        if not self.target:
            self.end_transmission = True

    def update_ret(self):
        self.ret_x += self.ret[0]
        if self.ret_x < -2:
            self.ret_x += .5
        elif self.ret_x > 1:
            self.ret_x -= .5
        self.ret_y += self.ret[1]
        if self.ret_y < -2:
            self.ret_y += .5
        elif self.ret_y > 2:
            self.ret_y -= .5

    def check_package_accuracy(self):
        self.target = self.closest_enemy(self.start_x, self.start_y)
        if not self.target:
            self.cleanup()
            return False

        self.hit = True
        if self.hit and random.randint(0, 100) < self.package['crit']:
            self.crit = True
            self.package['damage_min'] = int(self.package['damage_min'] * self.package['crit_damage'])
            self.package['damage_max'] = int(self.package['damage_max'] * self.package['crit_damage'])

        if self.hit and random.randint(0, 100) < self.target.stats.evade:
            self.evade = True

        if self.hit:
            self.range = 0
        else:
            self.range = 0

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

class NanoShot(HomingShot):
    def __init__(self, master, ability, skill, package, start_x, start_y):
        super(HomingShot, self).__init__(master, ability, skill, package, start_x, start_y)
        self.travelled = 1
        self.ret = [0, 0]
        self.ret_x = random.randint(-10, 10)
        self.ret_y = random.randint(-10, 10)
        self.tracking = 1

    def transmitting(self):
        if self.tracking:
            if self.hit:
                self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.sprite.x, self.sprite.y, 1)
                self.sprite.rotation = (math.degrees(math.atan2(self.target.sprite.y - self.sprite.y, self.target.sprite.x - self.sprite.x)) * -1) + 90
            else:
                self.ret = calc_vel_xy(self.mouse_x, self.mouse_y, self.sprite.x, self.sprite.y, 1)
                self.sprite.rotation = (math.degrees(math.atan2(self.mouse_y - self.sprite.y, self.mouse_x - self.sprite.x)) * -1) + 90
            self.update_ret()
            self.sprite.x += self.ret_x
            self.sprite.y += self.ret_y

        if math.hypot(self.target.sprite.x - self.sprite.x, self.target.sprite.y - self.sprite.y) < 10:
            self.end_transmission = True

        if not self.target:
            self.end_transmission = True

    def update_ret(self):
        self.ret_x += self.ret[0]
        if self.ret_x < -2:
            self.ret_x += .5
        elif self.ret_x > 1:
            self.ret_x -= .5
        self.ret_y += self.ret[1]
        if self.ret_y < -2:
            self.ret_y += .5
        elif self.ret_y > 2:
            self.ret_y -= .5

    def check_package_accuracy(self):
        self.target = self.closest_enemy(self.start_x, self.start_y)
        if not self.target:
            self.cleanup()
            return False

        self.hit = True
        if self.hit and random.randint(0, 100) < self.package['crit']:
            self.crit = True
            self.package['damage_min'] = int(self.package['damage_min'] * self.package['crit_damage'])
            self.package['damage_max'] = int(self.package['damage_max'] * self.package['crit_damage'])

        if self.hit and random.randint(0, 100) < self.target.stats.evade:
            self.evade = True

        if self.hit:
            self.range = 0
        else:
            self.range = 0

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


class Chaos(object):
    def __init__(self, master, handler, start_x, start_y): # noqa
        self.master = master
        self.handler = handler
        img = load_image('chaos.png')
        self.sprite = pyglet.sprite.Sprite(img,
        start_x, start_y, batch=EffectsBatch)
        self.timer = 1
        self.shoot_timer = 60
        self.shoot = 0
        self.ret = [0, 0]
        self.ret_x = 0
        self.ret_y = 0
        self.controller = None
        self.target = None

    def delete_self(self):
        self.master.spriteeffect.teleport(self.sprite.x, self.sprite.y)
        self.sprite.delete()
        self.handler.ability.core.chaos_in_action.remove(self)

    def update(self):
        if not self.controller:
            self.timer -= 1
            if not self.timer:
                self.ret = calc_vel_xy(self.handler.sprite.x, self.handler.sprite.y, self.sprite.x, self.sprite.y, 5)
                self.update_ret()
                self.timer = random.randint(3, 5)
            self.sprite.x += self.ret_x
            self.sprite.y += self.ret_y
        else:
            self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.sprite.x, self.sprite.y, 10)
            self.sprite.x += self.ret[0]
            self.sprite.y += self.ret[1]
            if math.hypot(self.target.sprite.x - self.sprite.x, self.target.sprite.y - self.sprite.y) < 10:
                try:
                    self.controller.activate(self)
                except Exception, e:
                    print e
                self.delete_self()

    def tracer_update(self):
        try:
            self.timer -= 1
            self.shoot_timer -= 1
            if self.target.dead:
                self.target = self.controller.closest_enemy(self)
            if not self.controller:
                if not self.timer:
                    self.ret = calc_vel_xy(self.handler.sprite.x, self.handler.sprite.y, self.sprite.x, self.sprite.y, 5)
                    self.update_ret()
                    self.timer = random.randint(3, 5)
                self.sprite.x += self.ret_x
                self.sprite.y += self.ret_y
            else:
                if not self.timer:
                    self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.sprite.x, self.sprite.y, 5)
                    self.update_ret()
                    self.timer = random.randint(3, 5)
                self.sprite.x += self.ret_x
                self.sprite.y += self.ret_y
            if not self.shoot_timer:
                self.shoot_timer = 60
                self.shoot += 1
                self.controller.activate(self)
                if self.shoot > 10:
                    self.delete_self()
        except:
            self.delete_self()

    def update_ret(self):
        self.ret_x += self.ret[0]
        if self.ret_x < -10:
            self.ret_x += 1
        elif self.ret_x > 10:
            self.ret_x -= 1
        self.ret_y += self.ret[1]
        if self.ret_y < -10:
            self.ret_y += 1
        elif self.ret_y > 10:
            self.ret_y -= 1


class Order(object):
    def __init__(self, master, handler, start_x, start_y): # noqa
        self.master = master
        self.handler = handler
        img = load_image('order.png')
        self.sprite = pyglet.sprite.Sprite(img,
        start_x, start_y, batch=EffectsBatch)
        self.timer = 1
        self.shoot_timer = 60
        self.shoot = 0
        self.ret = [0, 0]
        self.ret_x = 0
        self.ret_y = 0
        self.controller = None
        self.target = None

    def delete_self(self):
        self.master.spriteeffect.teleport(self.sprite.x, self.sprite.y)
        self.sprite.delete()
        self.handler.ability.core.order_in_action.remove(self)

    def update(self):
        if not self.controller:
            self.timer -= 1
            if not self.timer:
                self.ret = calc_vel_xy(self.handler.sprite.x, self.handler.sprite.y, self.sprite.x, self.sprite.y, 5)
                self.update_ret()
                self.timer = random.randint(3, 5)
            self.sprite.x += self.ret_x
            self.sprite.y += self.ret_y
        else:
            self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.sprite.x, self.sprite.y, 10)
            self.sprite.x += self.ret[0]
            self.sprite.y += self.ret[1]
            if math.hypot(self.target.sprite.x - self.sprite.x, self.target.sprite.y - self.sprite.y) < 10:
                try:
                    self.controller.activate(self)
                except Exception, e:
                    print e
                self.delete_self()

    def tracer_update(self):
        try:
            self.timer -= 1
            self.shoot_timer -= 1
            if self.target.dead:
                self.target = self.controller.closest_enemy(self)
            if not self.controller:
                if not self.timer:
                    self.ret = calc_vel_xy(self.handler.sprite.x, self.handler.sprite.y, self.sprite.x, self.sprite.y, 5)
                    self.update_ret()
                    self.timer = random.randint(3, 5)
                self.sprite.x += self.ret_x
                self.sprite.y += self.ret_y
            else:
                if not self.timer:
                    self.ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y, self.sprite.x, self.sprite.y, 5)
                    self.update_ret()
                    self.timer = random.randint(3, 5)
                self.sprite.x += self.ret_x
                self.sprite.y += self.ret_y
            if not self.shoot_timer:
                self.shoot_timer = 60
                self.shoot += 1
                self.controller.activate(self)
                if self.shoot > 10:
                    self.delete_self()
        except:
            self.delete_self()

    def update_ret(self):
        self.ret_x += self.ret[0]
        if self.ret_x < -10:
            self.ret_x += 1
        elif self.ret_x > 10:
            self.ret_x -= 1
        self.ret_y += self.ret[1]
        if self.ret_y < -10:
            self.ret_y += 1
        elif self.ret_y > 10:
            self.ret_y -= 1

class SpectreCore(Core):
    def __init__(self, master, handler):
        super(SpectreCore, self).__init__(master, handler)
        self.chaos = []
        self.chaos_in_action = []
        self.order = []
        self.order_in_action = []

    def add_chaos(self):
        if len(self.chaos) + len(self.order) < 5:
            self.chaos.append(Chaos(self.master, self.handler.owner, self.handler.owner.sprite.x, self.handler.owner.sprite.y))

    def add_order(self):
        if len(self.chaos) + len(self.order) < 5:
            self.order.append(Order(self.master, self.handler.owner, self.handler.owner.sprite.x, self.handler.owner.sprite.y))

    def update(self):
        for c in self.chaos:
            c.update()
        for c in self.chaos_in_action:
            c.update()
        for o in self.order:
            o.update()
        for o in self.order_in_action:
            o.update()

# Unfinished
class SPOVTimedBreathing(Skill):
    def __init__(self, master, level, handler):
        super(SPOVTimedBreathing, self).__init__(master, level, handler)

# Unfinished
class SPOVFlakJacket(Skill):
    def __init__(self, master, level, handler):
        super(SPOVFlakJacket, self).__init__(master, level, handler)

# Unfinished
class SPOVTwentyMileMarch(Skill):
    def __init__(self, master, level, handler):
        super(SPOVTwentyMileMarch, self).__init__(master, level, handler)

# Unfinished
class SPOVLockAndLoad(Skill):
    def __init__(self, master, level, handler):
        super(SPOVLockAndLoad, self).__init__(master, level, handler)

# Unfinished
class SPOVFletcher(Skill):
    def __init__(self, master, level, handler):
        super(SPOVFletcher, self).__init__(master, level, handler)

# Unfinished
class SPOVSpotAndShot(Skill):
    def __init__(self, master, level, handler):
        super(SPOVSpotAndShot, self).__init__(master, level, handler)

# Unfinished
class SPOVIronRations(Skill):
    def __init__(self, master, level, handler):
        super(SPOVIronRations, self).__init__(master, level, handler)

# Unfinished
class SPOVStrafe(Skill):
    def __init__(self, master, level, handler):
        super(SPOVStrafe, self).__init__(master, level, handler)

# Unfinished
class SPOVCannibalize(Skill):
    def __init__(self, master, level, handler):
        super(SPOVCannibalize, self).__init__(master, level, handler)

# Unfinished
class SPOVBarrage(Skill):
    def __init__(self, master, level, handler):
        super(SPOVBarrage, self).__init__(master, level, handler)

# Unfinished
class SPSNSlash(Skill):
    def __init__(self, master, level, handler):
        super(SPSNSlash, self).__init__(master, level, handler)

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                SpectreMelee(self.master, self.handler, self, self.handler.copy_gun(), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
                # self.handler.owner.stats.recoil += self.handler.owner.stats.gun_data['recoil']
                return True
            else:
                self.dash()
                return False
        except:
            return False

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

# Unfinished
class SPSNSalted(Skill):
    def __init__(self, master, level, handler):
        super(SPSNSalted, self).__init__(master, level, handler)

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                SpectreMelee(self.master, self.handler, self, self.handler.copy_gun(), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
                self.handler.owner.stats.recoil += self.handler.owner.stats.gun_data['recoil']
                return True
            else:
                self.dash()
                return False
        except:
            return False

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

# Unfinished
class SPSNMuzzleBrake(Skill):
    def __init__(self, master, level, handler):
        super(SPSNMuzzleBrake, self).__init__(master, level, handler)

# Unfinished
class SPSNCoupled(Skill):
    def __init__(self, master, level, handler):
        super(SPSNCoupled, self).__init__(master, level, handler)
        self.dash_sound = load_sound("dash.wav")

    def fire(self):
        enemy_range = self.get_enemy_dist()
        if len(self.handler.core.order):
            try:
                if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                    x = self.handler.core.order.pop()
                    self.handler.core.order_in_action.append(x)
                    x.delete_self()
                    gun = self.handler.copy_gun()
                    gun['damage_min'] = 1
                    gun['damage_max'] *= 4
                    SpectreMelee(self.master, self.handler, self, gun, self.handler.owner.sprite.x, self.handler.owner.sprite.y)
                    # self.handler.owner.stats.recoil += self.handler.owner.stats.gun_data['recoil']
                    return True
                else:
                    self.dash()
                    return False
            except:
                return False

    def dash(self):
        if not self.handler.owner.stats.speed > self.handler.owner.stats._speed:
            play_sound(self.dash_sound)
        self.handler.owner.stats.temp_stat_change(2, 'speed', 10)
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


# Unfinished
class SPSNIronDome(Skill):
    def __init__(self, master, level, handler):
        super(SPSNIronDome, self).__init__(master, level, handler)

# Unfinished
class SPSNHardCore(Skill):
    def __init__(self, master, level, handler):
        super(SPSNHardCore, self).__init__(master, level, handler)

# Unfinished
class SPSNPerseverate(Skill):
    def __init__(self, master, level, handler):
        super(SPSNPerseverate, self).__init__(master, level, handler)
        self.image = load_image('crystal.png')
        # self.on_hit = load_sound('anarchy_on_hit.wav')

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                gun = self.handler.copy_gun()
                gun['image'] = self.image
                gun['damage_min'] = int(max(gun['damage_min'] * .1, 1))
                gun['damage_max'] = int(max(gun['damage_max'] * .1, 2))
                SpectreMelee(self.master, self.handler, self, gun, self.handler.owner.sprite.x, self.handler.owner.sprite.y)
                self.handler.delayed.append([5, partial(SpectreMelee, self.master, self.handler, self, gun, self.handler.owner.sprite.x, self.handler.owner.sprite.y)])
                self.handler.delayed.append([10, partial(SpectreMelee, self.master, self.handler, self, gun, self.handler.owner.sprite.x, self.handler.owner.sprite.y)])
                # self.handler.owner.stats.recoil += self.handler.owner.stats.gun_data['recoil']
                return True
            else:
                self.dash()
                return False
        except:
            return False

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


# Unfinished
class SPSNBurst(Skill):
    def __init__(self, master, level, handler):
        super(SPSNBurst, self).__init__(master, level, handler)

    def fire(self):
        gun = self.handler.copy_gun()
        # gun['image'] = self.image
        gun['damage_min'] = int(max(gun['damage_min'] * .1, 1))
        gun['damage_max'] = int(max(gun['damage_max'] * .1, 2))
        # gun['velocity'] = 20
        HomingShot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
        HomingShot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
        HomingShot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
        HomingShot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
        HomingShot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
        return True

    def closest_enemy(self, chaos):
        target = None
        try:
            min_dist = float("inf")
            x1 = chaos.sprite.x
            y1 = chaos.sprite.y
            if len(self.handler.owner.enemies) == 0:
                return False
            for e in self.handler.owner.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    target = e
            return target
        except:
            return False

# Unfinished
class SPSNTriggerDiscipline(Skill):
    def __init__(self, master, level, handler):
        super(SPSNTriggerDiscipline, self).__init__(master, level, handler)

# Unfinished
class SPSNSalvo(Skill):
    def __init__(self, master, level, handler):
        super(SPSNSalvo, self).__init__(master, level, handler)

# Unfinished
class SPBLSlash(Skill):
    def __init__(self, master, level, handler):
        super(SPBLSlash, self).__init__(master, level, handler)

# Unfinished
class SPBLTrips(Skill):
    def __init__(self, master, level, handler):
        super(SPBLTrips, self).__init__(master, level, handler)


# Unfinished
class SPBLBangForYourBuck(Skill):
    def __init__(self, master, level, handler):
        super(SPBLBangForYourBuck, self).__init__(master, level, handler)

# Unfinished
class SPBLAnarchy(Skill):
    def __init__(self, master, level, handler):
        super(SPBLAnarchy, self).__init__(master, level, handler)
        self.image = load_image('snipe.png')
        self.sound = load_sound('anarchy.wav')
        self.on_hit = load_sound('anarchy_on_hit.wav')

    def fire(self):
        if len(self.handler.core.chaos):
            for c in self.handler.core.chaos:
                c.controller = self
                c.target = self.closest_enemy(c)
                if not c.target:
                    try:
                        c.delete_self()
                        self.handler.core.add_chaos()
                    except:
                        break
                play_sound(self.sound)
                self.handler.core.chaos_in_action.append(c)
                self.handler.core.chaos.remove(c)
            return True
        return False

    def activate(self, chaos):
        gun = self.handler.copy_gun()
        gun['image'] = self.image
        gun['accuracy'] += 100
        gun['on_hit_sound'] = self.on_hit
        AnarchyShot(self.master, self.handler, self, gun, chaos.sprite.x, chaos.sprite.y)

    def closest_enemy(self, chaos):
        target = None
        try:
            min_dist = 2000
            x1 = chaos.sprite.x
            y1 = chaos.sprite.y
            if len(self.handler.owner.enemies) == 0:
                return False
            for e in self.handler.owner.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    target = e
            return target
        except:
            return False
# Unfinished
class SPBLRocketPowered(Skill):
    def __init__(self, master, level, handler):
        super(SPBLRocketPowered, self).__init__(master, level, handler)

# Unfinished
class SPBLSmokyEyeSurprise(Skill):
    def __init__(self, master, level, handler):
        super(SPBLSmokyEyeSurprise, self).__init__(master, level, handler)

# Unfinished
class SPBLTracer(Skill):
    def __init__(self, master, level, handler):
        super(SPBLTracer, self).__init__(master, level, handler)
        self.image = load_image('red_laser.png')

    def fire(self):
        if len(self.handler.core.chaos):
            c = self.handler.core.chaos.pop()
            c.controller = self
            c.target = self.closest_enemy(c)
            if not c.target:
                try:
                    self.handler.core.add_chaos()
                    c.delete_self()
                except:
                    return True
                return True
            c.update = c.tracer_update
            self.handler.core.chaos_in_action.append(c)
            return True
        else:
            return False

    def activate(self, chaos):
        gun = self.handler.copy_gun()
        gun['image'] = self.image
        gun['damage_min'] = int(max(gun['damage_min'] * .1, 1))
        gun['damage_max'] = int(max(gun['damage_max'] * .1, 2))
        gun['velocity'] = 20
        NoTargetGunshot(self.master, self.handler, self, dict.copy(gun), chaos.sprite.x, chaos.sprite.y)

    def closest_enemy(self, chaos):
        target = None
        try:
            min_dist = float("inf")
            x1 = chaos.sprite.x
            y1 = chaos.sprite.y
            if len(self.handler.owner.enemies) == 0:
                return False
            for e in self.handler.owner.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    target = e
            return target
        except:
            return False

# Unfinished
class SPBLBlotOutTheSun(Skill):
    def __init__(self, master, level, handler):
        super(SPBLBlotOutTheSun, self).__init__(master, level, handler)

# Unfinished
class SPBLConked(Skill):
    def __init__(self, master, level, handler):
        super(SPBLConked, self).__init__(master, level, handler)

# Unfinished
class SPBLMayhem(Skill):
    def __init__(self, master, level, handler):
        super(SPBLMayhem, self).__init__(master, level, handler)
        self.image = load_image('crystal.png')
        self.on_hit = load_sound('crystal_break.wav')

    def fire(self):
        try:
            if len(self.handler.core.chaos):
                print self.handler.core.chaos
                for c in self.handler.core.chaos:
                    c.controller = self
                    self.handler.core.chaos_in_action.append(c)
                    self.activate(c)
                    c.delete_self()
                self.handler.core.chaos = []
                return True
            return False
        except Exception, e:
            print e
            self.handler.core.chaos = []

    def activate(self, chaos):
        gun = self.handler.copy_gun()
        gun['on_hit_sound'] = self.on_hit
        gun['image'] = self.image
        gun['damage_min'] = int(max(gun['damage_min'] * .1, 1))
        gun['damage_max'] = int(max(gun['damage_max'] * .1, 2))
        for i in range(3):
            HomingShot(self.master, self.handler, self, dict.copy(gun), chaos.sprite.x, chaos.sprite.y)

nanomancer_skillset = {
    'core': SpectreCore,
    '1': SPOVTimedBreathing,
    '2': SPOVFlakJacket,
    '3': SPOVTwentyMileMarch,
    '4': SPOVLockAndLoad,
    '5': SPOVFletcher,
    '6': SPOVSpotAndShot,
    '7': SPOVIronRations,
    '8': SPOVStrafe,
    '9': SPOVCannibalize,
    '10': SPOVBarrage,
    '11': SPSNSlash,
    '12': SPSNSalted,
    '13': SPSNMuzzleBrake,
    '14': SPSNCoupled,
    '15': SPSNIronDome,
    '16': SPSNHardCore,
    '17': SPSNPerseverate,
    '18': SPSNBurst,
    '19': SPSNTriggerDiscipline,
    '20': SPSNSalvo,
    '21': SPBLSlash,
    '22': SPBLTrips,
    '23': SPBLBangForYourBuck,
    '24': SPBLAnarchy,
    '25': SPBLRocketPowered,
    '26': SPBLSmokyEyeSurprise,
    '27': SPBLTracer,
    '28': SPBLBlotOutTheSun,
    '29': SPBLConked,
    '30': SPBLMayhem,
}

sample_nanomancer_build = {
    'slot_mouse_two': ['18', 1],
    'slot_one': ['14', 1],
    'slot_two': ['24', 1],
    'slot_three': ['30', 2],
    'slot_four': ['27', 3],
    'slot_q': ['1', 1],
    'slot_e': ['1', 1],
    'passive_one': ['1', 1],
    'passive_two': ['1', 1],
    'passive_three': ['1', 1],
}

# sample_spectre_build = {
#     'slot_mouse_two': ['21', 1],
#     'slot_one': ['22', 1],
#     'slot_two': ['24', 1],
#     'slot_three': ['11', 2],
#     'slot_four': ['1', 3],
#     'slot_q': ['25', 1],
#     'slot_e': ['15', 1],
#     'passive_one': ['4', 1],
#     'passive_two': ['16', 1],
#     'passive_three': ['13', 1],
# }
