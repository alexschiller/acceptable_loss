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
        self.plasma_max = 100

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

# Unfinished
class PSPDRepurpose(Skill):
    def __init__(self, master, level, handler):
        super(PSPDRepurpose, self).__init__(master, level, handler)
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
class PSPDFlakJacket(Skill):
    def __init__(self, master, level, handler):
        super(PSPDFlakJacket, self).__init__(master, level, handler)

# Unfinished
class PSPDTwentyMileMarch(Skill):
    def __init__(self, master, level, handler):
        super(PSPDTwentyMileMarch, self).__init__(master, level, handler)

# Unfinished
class PSPDLockAndLoad(Skill):
    def __init__(self, master, level, handler):
        super(PSPDLockAndLoad, self).__init__(master, level, handler)

# Unfinished
class PSPDFletcher(Skill):
    def __init__(self, master, level, handler):
        super(PSPDFletcher, self).__init__(master, level, handler)

# Unfinished
class PSPDSpotAndShot(Skill):
    def __init__(self, master, level, handler):
        super(PSPDSpotAndShot, self).__init__(master, level, handler)

# Unfinished
class PSPDIronRations(Skill):
    def __init__(self, master, level, handler):
        super(PSPDIronRations, self).__init__(master, level, handler)

# Unfinished
class PSPDStrafe(Skill):
    def __init__(self, master, level, handler):
        super(PSPDStrafe, self).__init__(master, level, handler)

# Unfinished
class PSPDCannibalize(Skill):
    def __init__(self, master, level, handler):
        super(PSPDCannibalize, self).__init__(master, level, handler)

# Unfinished
class PSPDBarrage(Skill):
    def __init__(self, master, level, handler):
        super(PSPDBarrage, self).__init__(master, level, handler)

# Unfinished
class PSMABang(Skill):
    def __init__(self, master, level, handler):
        super(PSMABang, self).__init__(master, level, handler)
    #     self.image = load_image('psma.png')
    #     self.damage_mod = 1 + .05 * self.level

    # def fire(self):
    #     if self.handler.core.bullets:
    #         self.handler.core.bullets -= 1
    #         gun = self.handler.copy_gun()
    #         gun['damage_min'] = int(gun['damage_min'] * self.damage_mod)
    #         gun['damage_max'] = int(gun['damage_max'] * self.damage_mod)
    #         # gun['velocity'] = 30
    #         gun['image'] = self.image

    #         PlayerGunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
    #         return True
    #     return False

# Unfinished
class PSMAShieldSplitter(Skill):
    def __init__(self, master, level, handler):
        super(PSMAShieldSplitter, self).__init__(master, level, handler)
        self.img = load_image('strike.png')
        self.sound = load_sound('slash.wav')

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                gun = self.handler.copy_gun()
                gun['image'] = self.img
                gun['gun_fire_sound'] = self.sound
                pmod = .5
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
class PSMALightSword(Skill):
    def __init__(self, master, level, handler):
        super(PSMALightSword, self).__init__(master, level, handler)
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
class PSMALightSpeed(Skill):
    def __init__(self, master, level, handler):
        super(PSMALightSpeed, self).__init__(master, level, handler)
        self.img = load_image('strike.png')
        self.sound = load_sound('slash.wav')

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                gun = self.handler.copy_gun()
                gun['image'] = self.img
                gun['gun_fire_sound'] = self.sound
                pmod = .2
                gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
                gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
                for i in range(random.randint(1, 10)):
                    self.handler.delayed.append([i, partial(LightningMelee, self.master, self.handler, self, gun, self.handler.owner.sprite.x, self.handler.owner.sprite.y)])
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
class PSMAIronDome(Skill):
    def __init__(self, master, level, handler):
        super(PSMAIronDome, self).__init__(master, level, handler)

# Unfinished
class PSMAHardCore(Skill):
    def __init__(self, master, level, handler):
        super(PSMAHardCore, self).__init__(master, level, handler)

# Unfinished
class PSMAPerseverate(Skill):
    def __init__(self, master, level, handler):
        super(PSMAPerseverate, self).__init__(master, level, handler)

# Unfinished
class PSMABurst(Skill):
    def __init__(self, master, level, handler):
        super(PSMABurst, self).__init__(master, level, handler)

# Unfinished
class PSMATriggerDiscipline(Skill):
    def __init__(self, master, level, handler):
        super(PSMATriggerDiscipline, self).__init__(master, level, handler)

# Unfinished
class PSMASalvo(Skill):
    def __init__(self, master, level, handler):
        super(PSMASalvo, self).__init__(master, level, handler)

# Unfinished
class PSPOBolt(Skill):
    def __init__(self, master, level, handler):
        super(PSPOBolt, self).__init__(master, level, handler)
        self.gun_fire_sound = load_sound('lightning_bolt.wav')

    def fire(self):
        dist = self.get_enemy_dist()
        if dist and dist <= (50 + 700 * self.handler.core.plasma / self.handler.core.plasma_max):
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

    def get_enemy_dist(self):
        if self.handler.owner.target:
            dist_x = self.handler.owner.sprite.x - self.handler.owner.target.sprite.x
            dist_y = self.handler.owner.sprite.y - self.handler.owner.target.sprite.y
            dist = math.hypot(dist_x, dist_y)
            return dist
        return False

# Unfinished
class PSPOAnvilCrawler(Skill):
    def __init__(self, master, level, handler):
        super(PSPOAnvilCrawler, self).__init__(master, level, handler)
        self.gun_fire_sound = load_sound('lightning_bolt.wav')

    def fire(self):
        hits = 0
        for e in self.handler.owner.enemies:
            if hits >= 3:
                break
            self.handler.owner.target = e
            dist = self.get_enemy_dist()
            if dist <= (self.handler.core.plasma / self.handler.core.plasma_max * 200) + 50:
                hits += 1
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
                gun['gun_fire_sound'] = self.gun_fire_sound
                pmod = self.handler.core.plasma / self.handler.core.plasma_max * .5
                gun['gun_fire_sound'] = self.gun_fire_sound
                gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
                gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
                Gunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y)

        if hits > 0:
            self.handler.core.plasma = 0
            return True
        return False

    def get_enemy_dist(self):
        if self.handler.owner.target:
            dist_x = self.handler.owner.sprite.x - self.handler.owner.target.sprite.x
            dist_y = self.handler.owner.sprite.y - self.handler.owner.target.sprite.y
            dist = math.hypot(dist_x, dist_y)
            return dist
        return False


# Unfinished
class PSPOBangForYourBuck(Skill):
    def __init__(self, master, level, handler):
        super(PSPOBangForYourBuck, self).__init__(master, level, handler)

# Unfinished
class PSPOSpark(Skill):
    def __init__(self, master, level, handler):
        super(PSPOSpark, self).__init__(master, level, handler)
        self.gun_fire_sound = load_sound('lightning_bolt.wav')

    def fire(self):
        if self.handler.core.plasma >= 50:
            dist = self.get_enemy_dist()
            if dist:
                if dist <= 100:

                    self.handler.core.plasma -= 50
                    gun = self.handler.copy_gun()
                    gun['accuracy'] += 100
                    gun['damage_min'] = int(max(gun['damage_min'] * .1, 1))
                    gun['damage_max'] = int(max(gun['damage_max'] * .1, 2))
                    gun['gun_fire_sound'] = self.gun_fire_sound
                    self.add_strike(gun, dist)
                    self.handler.delayed.append([10, partial(self.add_strike, gun, dist)])
                    self.handler.delayed.append([20, partial(self.add_strike, gun, dist)])
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
class PSPOZipZap(Skill):
    def __init__(self, master, level, handler):
        super(PSPOZipZap, self).__init__(master, level, handler)
        self.img = load_image('strike.png')
        self.sound = load_sound('slash.wav')

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50 and enemy_range and not self.handler.global_cooldown:
                gun = self.handler.copy_gun()
                gun['image'] = self.img
                gun['gun_fire_sound'] = self.sound
                # pmod = 1
                # gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
                # gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
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

    def get_enemy_dist(self):
        if self.handler.owner.target:
            dist_x = self.handler.owner.sprite.x - self.handler.owner.target.sprite.x
            dist_y = self.handler.owner.sprite.y - self.handler.owner.target.sprite.y
            dist = math.hypot(dist_x, dist_y)
            return dist
        return False

# Unfinished
class PSPOPlasmaBall(Skill):
    def __init__(self, master, level, handler):
        super(PSPOPlasmaBall, self).__init__(master, level, handler)
        self.image = load_image('plasma_ball.png')
        self.damage_mod = 1 + .05 * self.level

    def fire(self):
        if self.handler.core.plasma >= 20:
            self.handler.core.plasma -= 20
            gun = self.handler.copy_gun()
            gun['damage_min'] = int(gun['damage_min'] * self.damage_mod)
            gun['damage_max'] = int(gun['damage_max'] * self.damage_mod)
            # gun['velocity'] = 30
            gun['image'] = self.image

            PlayerGunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
            return True
        return False

# Unfinished
class PSPOTracer(Skill):
    def __init__(self, master, level, handler):
        super(PSPOTracer, self).__init__(master, level, handler)

# Unfinished
class PSPOBlotOutTheSun(Skill):
    def __init__(self, master, level, handler):
        super(PSPOBlotOutTheSun, self).__init__(master, level, handler)

# Unfinished
class PSPOConked(Skill):
    def __init__(self, master, level, handler):
        super(PSPOConked, self).__init__(master, level, handler)

# Unfinished
class PSPOBallLightning(Skill):
    def __init__(self, master, level, handler):
        super(PSPOBallLightning, self).__init__(master, level, handler)


plasmaslinger_skillset = {
    'core': PlasmaCore,
    '1': PSPDRepurpose,
    '2': PSPDFlakJacket,
    '3': PSPDTwentyMileMarch,
    '4': PSPDLockAndLoad,
    '5': PSPDFletcher,
    '6': PSPDSpotAndShot,
    '7': PSPDIronRations,
    '8': PSPDStrafe,
    '9': PSPDCannibalize,
    '10': PSPDBarrage,
    '11': PSMABang,
    '12': PSMAShieldSplitter,
    '13': PSMALightSword,
    '14': PSMALightSpeed,
    '15': PSMAIronDome,
    '16': PSMAHardCore,
    '17': PSMAPerseverate,
    '18': PSMABurst,
    '19': PSMATriggerDiscipline,
    '20': PSMASalvo,
    '21': PSPOBolt,
    '22': PSPOAnvilCrawler,
    '23': PSPOBangForYourBuck,
    '24': PSPOSpark,
    '25': PSPOZipZap,
    '26': PSPOPlasmaBall,
    '27': PSPOTracer,
    '28': PSPOBlotOutTheSun,
    '29': PSPOConked,
    '30': PSPOBallLightning,
}
