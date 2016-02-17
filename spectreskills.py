from baseskills import * # noqa
import math
from functools import partial
from utility import load_image

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
class SPSNTrigger(Skill):
    def __init__(self, master, level, handler):
        super(SPSNTrigger, self).__init__(master, level, handler)
        self.damage_mod = .5 + self.level * .05

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

            bullet_base['damage_min'] = int(self.damage_mod * bullet_base['damage_min'])
            bullet_base['damage_max'] = int(self.damage_mod * bullet_base['damage_max'])
            # play_sound(self.owner.stats.gun_one_data['gun_fire_sound'])
            self.handler.thrown.append(Thrown(self.master, self.handler, bullet_base))
            self.handler.owner.stats.recoil += self.handler.owner.stats.gun_one_data['recoil']
            self.handler.trigger_global_cooldown()

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
        self.armor_pierce_mod = 1 + self.level * .05
        self.img = load_image('salted.png')

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

            bullet_base['armor_pierce'] = int(self.armor_pierce_mod * (bullet_base['armor_pierce'] + self.level))
            bullet_base['image'] = self.img
            # play_sound(self.owner.stats.gun_one_data['gun_fire_sound'])
            self.handler.thrown.append(Thrown(self.master, self.handler, bullet_base))
            self.handler.owner.stats.recoil += self.handler.owner.stats.gun_one_data['recoil']
            self.handler.trigger_global_cooldown()

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
class SPSNPointBlank(Skill):
    def __init__(self, master, level, handler):
        super(SPSNPointBlank, self).__init__(master, level, handler)

# Unfinished
class SPSNIronDome(Skill):
    def __init__(self, master, level, handler):
        super(SPSNIronDome, self).__init__(master, level, handler)

# Unfinished
class SPSNHardCore(Skill):
    def __init__(self, master, level, handler):
        super(SPSNHardCore, self).__init__(master, level, handler)

# Unfinished
class SPSNTotalSystemShock(Skill):
    def __init__(self, master, level, handler):
        super(SPSNTotalSystemShock, self).__init__(master, level, handler)

# Unfinished
class SPSNBurst(Skill):
    def __init__(self, master, level, handler):
        super(SPSNBurst, self).__init__(master, level, handler)
        self.damage_mod = .5 + self.level * .05

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
            bullet_base['damage_min'] = int(self.damage_mod * bullet_base['damage_min'])
            bullet_base['damage_max'] = int(self.damage_mod * bullet_base['damage_max'])

            # play_sound(self.owner.stats.gun_one_data['gun_fire_sound'])
            self.handler.delayed.append([5, partial(self.handler.thrown.append, Thrown(self.master, self.handler, bullet_base))])
            self.handler.delayed.append([10, partial(self.handler.thrown.append, Thrown(self.master, self.handler, bullet_base))])
            self.handler.owner.stats.recoil += (self.handler.owner.stats.gun_one_data['recoil'] * 3)
            self.handler.trigger_global_cooldown()

    def get_enemy_dist(self):
        if self.handler.owner.target:
            dist_x = self.handler.owner.sprite.x - self.handler.owner.target.sprite.x
            dist_y = self.handler.owner.sprite.y - self.handler.owner.target.sprite.y
            dist = math.hypot(dist_x, dist_y)
            return dist
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

    def fire(self):
        enemy_range = self.get_enemy_dist()
        try:
            if enemy_range <= 50:
                if not self.handler.global_cooldown:
                    bullet_base = self.handler.build_bullet(
                        self.handler.owner.stats.gun_two_data,
                        self.handler.owner.sprite.x,
                        self.handler.owner.sprite.y,
                        self.handler.owner.target.sprite.x,
                        self.handler.owner.target.sprite.y,
                        enemy_range,
                        self.handler.owner.target,
                    )
                    # play_sound(self.owner.stats.gun_two_data['gun_fire_sound'])
                    self.handler.thrown.append(Melee(self.master, self.handler, bullet_base))
                    self.handler.owner.stats.recoil += self.handler.owner.stats.gun_two_data['recoil']
                    self.handler.trigger_global_cooldown()
            else:
                ret = calc_vel_xy(self.handler.owner.sprite.x, self.handler.owner.sprite.y,
                    self.handler.owner.target.sprite.x, self.handler.owner.target.sprite.y, 45)
                self.handler.owner.controller.move_to(self.handler.owner.target.sprite.x + ret[0],
                    self.handler.owner.target.sprite.y + ret[1], 1)
        except:
            pass

    def get_enemy_dist(self):
        if self.handler.owner.target:
            dist_x = self.handler.owner.sprite.x - self.handler.owner.target.sprite.x
            dist_y = self.handler.owner.sprite.y - self.handler.owner.target.sprite.y
            dist = math.hypot(dist_x, dist_y)
            return dist
        return False

# Unfinished
class SPBLNeedle(Skill):
    def __init__(self, master, level, handler):
        super(SPBLNeedle, self).__init__(master, level, handler)

# Unfinished
class SPBLBangForYourBuck(Skill):
    def __init__(self, master, level, handler):
        super(SPBLBangForYourBuck, self).__init__(master, level, handler)

# Unfinished
class SPBLHoming(Skill):
    def __init__(self, master, level, handler):
        super(SPBLHoming, self).__init__(master, level, handler)

# Unfinished
class SPBLRocketPowered(Skill):
    def __init__(self, master, level, handler):
        super(SPBLRocketPowered, self).__init__(master, level, handler)

    def fire(self):
        if self.handler.owner.controller.move_target:
            mt = self.handler.owner.controller.move_target
            self.handler.owner.stats.temp_stat_change(60, 'speed', 2)
            self.handler.owner.stats.temp_stat_change(60, 'evade', 10)
            self.master.spriteeffect.rocket_shoes(self.handler.owner.sprite.x, self.handler.owner.sprite.y, mt[0], mt[1])

# Unfinished
class SPBLSmokyEyeSurprise(Skill):
    def __init__(self, master, level, handler):
        super(SPBLSmokyEyeSurprise, self).__init__(master, level, handler)

# Unfinished
class SPBLTheRLL(Skill):
    def __init__(self, master, level, handler):
        super(SPBLTheRLL, self).__init__(master, level, handler)

# Unfinished
class SPBLBlotOutTheSun(Skill):
    def __init__(self, master, level, handler):
        super(SPBLBlotOutTheSun, self).__init__(master, level, handler)

# Unfinished
class SPBLConked(Skill):
    def __init__(self, master, level, handler):
        super(SPBLConked, self).__init__(master, level, handler)

# Unfinished
class SPBLSwarm(Skill):
    def __init__(self, master, level, handler):
        super(SPBLSwarm, self).__init__(master, level, handler)

spectre_skillset = {
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
    '11': SPSNTrigger,
    '12': SPSNSalted,
    '13': SPSNMuzzleBrake,
    '14': SPSNPointBlank,
    '15': SPSNIronDome,
    '16': SPSNHardCore,
    '17': SPSNTotalSystemShock,
    '18': SPSNBurst,
    '19': SPSNTriggerDiscipline,
    '20': SPSNSalvo,
    '21': SPBLSlash,
    '22': SPBLNeedle,
    '23': SPBLBangForYourBuck,
    '24': SPBLHoming,
    '25': SPBLRocketPowered,
    '26': SPBLSmokyEyeSurprise,
    '27': SPBLTheRLL,
    '28': SPBLBlotOutTheSun,
    '29': SPBLConked,
    '30': SPBLSwarm,
}

sample_spectre_build = {
    'slot_mouse_two': ['21', 1],
    'slot_one': ['11', 1],
    'slot_two': ['12', 1],
    'slot_three': ['11', 2],
    'slot_four': ['1', 3],
    'slot_q': ['25', 1],
    'slot_e': ['15', 1],
    'passive_one': ['4', 1],
    'passive_two': ['16', 1],
    'passive_three': ['13', 1],
}
