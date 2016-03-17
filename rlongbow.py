from baseskills import * # noqa
import math
from functools import partial
from utility import * # noqa

class Nano(object):
    def __init__(self, master, handler, start_x, start_y): # noqa
        self.master = master
        self.handler = handler
        img = load_image('smiss.png')
        self.sprite = pyglet.sprite.Sprite(img,
        start_x, start_y, batch=EffectsBatch)
        self.timer = 1
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
        if random.choice([0, 0, 0, 0, 0, 1]):
            self.sprite.scale += .2
        if self.sprite.scale > 1:
            self.sprite.scale -= .1
        if not self.controller:
            self.timer -= 1
            if not self.timer:
                self.ret = calc_vel_xy(self.handler.sprite.x, self.handler.sprite.y, self.sprite.x, self.sprite.y, 3)
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

class MissileCore(Core):
    def __init__(self, master, handler):
        super(MissileCore, self).__init__(master, handler)
        self.nano = []
        self.nano_in_action = []

    def add_nano(self):
        if len(self.nano) < 5:
            self.nano.append(Nano(self.master, self.handler.owner, self.handler.owner.sprite.x, self.handler.owner.sprite.y))

    def update(self):
        self.add_nano()
        for n in self.nano:
            n.update()
        for n in self.nano_in_action:
            n.update()


class LBBarrage(Skill):
    def __init__(self, master, level, handler):
        super(LBBarrage, self).__init__(master, level, handler)
        self.img = load_image('autocannon.png')

    def fire(self):
        enemy_range = self.get_enemy_dist()
    	try:
            gun = self.handler.copy_gun()
            pmod = .1 + self.level * .05
            gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
            gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
            play_sound(gun['gun_fire_sound'])
            gun['gun_fire_sound'] = None
            for m in self.handler.core.nano:
            	self.handler.delayed.append([random.randint(1,10), partial(self.add_strike, gun, m)])
            	# PlayerGunshot(self.master, self.handler, self, dict.copy(gun), m.sprite.x, m.sprite.y)
            # self.handler.owner.stats.recoil += 13
            self.handler.delayed.append([5, partial(self.add_strike, gun)])
            # self.handler.delayed.append([10, partial(self.add_strike, gun)])
            

            return True
        except:
            return False

    def add_strike(self, gun, m):
        if self.handler.owner.target:
        	PlayerGunshot(self.master, self.handler, self, dict.copy(gun), m.sprite.x, m.sprite.y)
        	# self.handler.owner.stats.recoil += 13


# Unfinished
class LBCurrent(Skill):
    def __init__(self, master, level, handler):
        super(LBCurrent, self).__init__(master, level, handler)

# Unfinished
class LBZap(Skill):
    def __init__(self, master, level, handler):
        super(LBZap, self).__init__(master, level, handler)

# Unfinished
class LBElectrocute(Skill):
    def __init__(self, master, level, handler):
        super(LBElectrocute, self).__init__(master, level, handler)

# Unfinished
class LBChainLightning(Skill):
    def __init__(self, master, level, handler):
        super(LBChainLightning, self).__init__(master, level, handler)

# Unfinished
class LBBallLightning(Skill):
    def __init__(self, master, level, handler):
        super(LBBallLightning, self).__init__(master, level, handler)

# Unfinished
class LBRepurpose(Skill):
    def __init__(self, master, level, handler):
        super(LBRepurpose, self).__init__(master, level, handler)

# Unfinished
class LBEmpower(Skill):
    def __init__(self, master, level, handler):
        super(LBEmpower, self).__init__(master, level, handler)

# Unfinished
class LBZipZap(Skill):
    def __init__(self, master, level, handler):
        super(LBZipZap, self).__init__(master, level, handler)

# Unfinished
class LBEnergize(Skill):
    def __init__(self, master, level, handler):
        super(LBEnergize, self).__init__(master, level, handler)

# Unfinished
class LBRedirect(Skill):
    def __init__(self, master, level, handler):
        super(LBRedirect, self).__init__(master, level, handler)

# Unfinished
class LBRepulse(Skill):
    def __init__(self, master, level, handler):
        super(LBRepulse, self).__init__(master, level, handler)

longbow_skillset = {
    'core': MissileCore,
    '1': LBBarrage,
    '2': LBCurrent,
    '3': LBZap,
    '4': LBElectrocute,
    '5': LBChainLightning,
    '6': LBBallLightning,
    '7': LBRepurpose,
    '8': LBEmpower,
    '9': LBZipZap,
    '10': LBEnergize,
    '11': LBRedirect,
    '12': LBRepulse,
}
