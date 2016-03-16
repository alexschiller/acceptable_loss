from baseskills import * # noqa
import math
from functools import partial
from utility import * # noqa

class MissileCore(Core):
    def __init__(self, master, handler):
        super(MissileCore, self).__init__(master, handler)

    def update(self):
    	pass


class LBBarrage(Skill):
    def __init__(self, master, level, handler):
        super(LBBarrage, self).__init__(master, level, handler)
        self.img = load_image('autocannon.png')

    def fire(self):
        enemy_range = self.get_enemy_dist()
    	try:
            gun = self.handler.copy_gun()
            pmod = .5 + self.level * .05
            gun['damage_min'] = int(max(gun['damage_min'] * pmod, 1))
            gun['damage_max'] = int(max(gun['damage_max'] * pmod, 2))
            PlayerGunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
            self.handler.owner.stats.recoil += 13
            self.handler.delayed.append([5, partial(self.add_strike, gun)])
            self.handler.delayed.append([10, partial(self.add_strike, gun)])
            

            return True
        except:
            return False

    def add_strike(self, gun):
        if self.handler.owner.target:
        	PlayerGunshot(self.master, self.handler, self, dict.copy(gun), self.handler.owner.sprite.x, self.handler.owner.sprite.y)
        	self.handler.owner.stats.recoil += 13


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
