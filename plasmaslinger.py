from baseskills import * # noqa
# import math
from functools import partial
from utility import * # noqa

class PlasmaCore(Core):
    def __init__(self, master, handler):
        super(PlasmaCore, self).__init__(master, handler)
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
        counter = 0
        if not target:
            target = [marker[0] + random.randint(-100, 100), marker[1] + random.randint(-100, 100)]
        while counter < dist:
            counter += 1
            ret = calc_vel_xy(target[0], target[1], marker[0], marker[1], 3)
            marker[0] += ret[0] + random.randint(-2, 2)
            marker[1] += ret[1] + random.randint(-2, 2)
            self.create_dot(marker[0], marker[1])
            # if counter == dist / 2:
            #     if random.choice([0, 0, 0, 1]):
            #         if dist > 10:
            #             self.create_lightning(marker[0],
            #                 marker[1],
            #                 dist=dist / 2,
            #             )

    def update(self):
        if self.plasma < self.plasma_max:
            self.plasma += .5
        if len(self.lightning):
            self.lightning_counter -= 1
            if not self.lightning_counter:
                self.lightning = []
        else:
            if random.randint(0, 100) >= 100 - self.plasma / 10:
                self.lightning_counter = 3
                self.create_lightning(self.handler.owner.sprite.x, self.handler.owner.sprite.y)

        if not self.bullets:
            self.reload_timer -= 1
            if not self.reload_timer:
                self.bullets += self.max_bullets
                self.reload_timer += self.reload_timer_max

# Unfinished
class PSPDTimedBreathing(Skill):
    def __init__(self, master, level, handler):
        super(PSPDTimedBreathing, self).__init__(master, level, handler)

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
        self.image = load_image('psma.png')
        self.damage_mod = 1 + .05 * self.level

    def fire(self):
        if self.handler.core.bullets:
            self.handler.core.bullets -= 1
            gun = self.handler.copy_gun()
            gun['damage_min'] = int(gun['damage_min'] * self.damage_mod)
            gun['damage_max'] = int(gun['damage_max'] * self.damage_mod)
            # gun['velocity'] = 30
            gun['image'] = self.image

            PlayerGunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
            return True
        return False

# Unfinished
class PSMABolted(Skill):
    def __init__(self, master, level, handler):
        super(PSMABolted, self).__init__(master, level, handler)

# Unfinished
class PSMAMuzzleBrake(Skill):
    def __init__(self, master, level, handler):
        super(PSMAMuzzleBrake, self).__init__(master, level, handler)

# Unfinished
class PSMACoupled(Skill):
    def __init__(self, master, level, handler):
        super(PSMACoupled, self).__init__(master, level, handler)

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
        if self.handler.core.plasma >= 50:
            dist = self.get_enemy_dist()
            if dist:
                self.handler.core.plasma -= 50
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
                Gunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y)
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
        if self.handler.core.plasma >= 100:
            self.handler.core.plasma -= 100
            for e in self.handler.owner.enemies:
                if hits == 3:
                    return True
                self.handler.owner.target = e
                dist = self.get_enemy_dist()
                if dist <= 200:
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
                    Gunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y)

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
class PSPORocketPowered(Skill):
    def __init__(self, master, level, handler):
        super(PSPORocketPowered, self).__init__(master, level, handler)

# Unfinished
class PSPOSmokyEyeSurprise(Skill):
    def __init__(self, master, level, handler):
        super(PSPOSmokyEyeSurprise, self).__init__(master, level, handler)

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
class PSPOMayhem(Skill):
    def __init__(self, master, level, handler):
        super(PSPOMayhem, self).__init__(master, level, handler)

plasmaslinger_skillset = {
    'core': PlasmaCore,
    '1': PSPDTimedBreathing,
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
    '12': PSMABolted,
    '13': PSMAMuzzleBrake,
    '14': PSMACoupled,
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
    '25': PSPORocketPowered,
    '26': PSPOSmokyEyeSurprise,
    '27': PSPOTracer,
    '28': PSPOBlotOutTheSun,
    '29': PSPOConked,
    '30': PSPOMayhem,
}
