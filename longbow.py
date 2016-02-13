from baseskills import * # noqa

# Unfinished
class LBALTimedBreathing(Skill):
    def __init__(self, master, level, handler):
        super(LBALTimedBreathing, self).__init__(master, level, handler)

# Unfinished
class LBALFlakJacket(Skill):
    def __init__(self, master, level, handler):
        super(LBALFlakJacket, self).__init__(master, level, handler)

# Unfinished
class LBALTwentyMileMarch(Skill):
    def __init__(self, master, level, handler):
        super(LBALTwentyMileMarch, self).__init__(master, level, handler)

# Unfinished
class LBALLockAndLoad(Skill):
    def __init__(self, master, level, handler):
        super(LBALLockAndLoad, self).__init__(master, level, handler)

# Unfinished
class LBALFletcher(Skill):
    def __init__(self, master, level, handler):
        super(LBALFletcher, self).__init__(master, level, handler)

# Unfinished
class LBALSpotAndShot(Skill):
    def __init__(self, master, level, handler):
        super(LBALSpotAndShot, self).__init__(master, level, handler)

# Unfinished
class LBALIronRations(Skill):
    def __init__(self, master, level, handler):
        super(LBALIronRations, self).__init__(master, level, handler)

# Unfinished
class LBALStrafe(Skill):
    def __init__(self, master, level, handler):
        super(LBALStrafe, self).__init__(master, level, handler)

# Unfinished
class LBALCannibalize(Skill):
    def __init__(self, master, level, handler):
        super(LBALCannibalize, self).__init__(master, level, handler)

# Unfinished
class LBALBarrage(Skill):
    def __init__(self, master, level, handler):
        super(LBALBarrage, self).__init__(master, level, handler)

# Unfinished
class LBACTrigger(Skill):
    def __init__(self, master, level, handler):
        super(LBACTrigger, self).__init__(master, level, handler)

    def fire(self):
        bullet_base = self.handler.build_bullet(
            self.handler.owner.stats.gun_two_data,
            self.handler.owner.sprite.x,
            self.handler.owner.sprite.y,
            self.handler.owner.target.sprite.x,
            self.handler.owner.target.sprite.y,
            500,
            self.handler.owner.target,
        )
        # play_sound(self.owner.stats.gun_two_data['gun_fire_sound'])
        self.handler.thrown.append(Thrown(self.master, self.handler, bullet_base))

        # time = int(60.0 / bullet_base['rof'])
        # self.trigger_aa_cooldown(time)

# Unfinished
class LBACSalted(Skill):
    def __init__(self, master, level, handler):
        super(LBACSalted, self).__init__(master, level, handler)

# Unfinished
class LBACMuzzleBrake(Skill):
    def __init__(self, master, level, handler):
        super(LBACMuzzleBrake, self).__init__(master, level, handler)

# Unfinished
class LBACPointBlank(Skill):
    def __init__(self, master, level, handler):
        super(LBACPointBlank, self).__init__(master, level, handler)

# Unfinished
class LBACIronDome(Skill):
    def __init__(self, master, level, handler):
        super(LBACIronDome, self).__init__(master, level, handler)

# Unfinished
class LBACHardCore(Skill):
    def __init__(self, master, level, handler):
        super(LBACHardCore, self).__init__(master, level, handler)

# Unfinished
class LBACTotalSystemShock(Skill):
    def __init__(self, master, level, handler):
        super(LBACTotalSystemShock, self).__init__(master, level, handler)

# Unfinished
class LBACBurst(Skill):
    def __init__(self, master, level, handler):
        super(LBACBurst, self).__init__(master, level, handler)

# Unfinished
class LBACTriggerDiscipline(Skill):
    def __init__(self, master, level, handler):
        super(LBACTriggerDiscipline, self).__init__(master, level, handler)

# Unfinished
class LBACSalvo(Skill):
    def __init__(self, master, level, handler):
        super(LBACSalvo, self).__init__(master, level, handler)

# Unfinished
class LBMSLaunch(Skill):
    def __init__(self, master, level, handler):
        super(LBMSLaunch, self).__init__(master, level, handler)

# Unfinished
class LBMSNeedle(Skill):
    def __init__(self, master, level, handler):
        super(LBMSNeedle, self).__init__(master, level, handler)

# Unfinished
class LBMSBangForYourBuck(Skill):
    def __init__(self, master, level, handler):
        super(LBMSBangForYourBuck, self).__init__(master, level, handler)

# Unfinished
class LBMSHoming(Skill):
    def __init__(self, master, level, handler):
        super(LBMSHoming, self).__init__(master, level, handler)

# Unfinished
class LBMSRocketPowered(Skill):
    def __init__(self, master, level, handler):
        super(LBMSRocketPowered, self).__init__(master, level, handler)

# Unfinished
class LBMSSmokyEyeSurprise(Skill):
    def __init__(self, master, level, handler):
        super(LBMSSmokyEyeSurprise, self).__init__(master, level, handler)

# Unfinished
class LBMSTheRLL(Skill):
    def __init__(self, master, level, handler):
        super(LBMSTheRLL, self).__init__(master, level, handler)

# Unfinished
class LBMSBlotOutTheSun(Skill):
    def __init__(self, master, level, handler):
        super(LBMSBlotOutTheSun, self).__init__(master, level, handler)

# Unfinished
class LBMSConked(Skill):
    def __init__(self, master, level, handler):
        super(LBMSConked, self).__init__(master, level, handler)

# Unfinished
class LBMSSwarm(Skill):
    def __init__(self, master, level, handler):
        super(LBMSSwarm, self).__init__(master, level, handler)

longbow_skillset = {
    '1': LBALTimedBreathing,
    '2': LBALFlakJacket,
    '3': LBALTwentyMileMarch,
    '4': LBALLockAndLoad,
    '5': LBALFletcher,
    '6': LBALSpotAndShot,
    '7': LBALIronRations,
    '8': LBALStrafe,
    '9': LBALCannibalize,
    '10': LBALBarrage,
    '11': LBACTrigger,
    '12': LBACSalted,
    '13': LBACMuzzleBrake,
    '14': LBACPointBlank,
    '15': LBACIronDome,
    '16': LBACHardCore,
    '17': LBACTotalSystemShock,
    '18': LBACBurst,
    '19': LBACTriggerDiscipline,
    '20': LBACSalvo,
    '21': LBMSLaunch,
    '22': LBMSNeedle,
    '23': LBMSBangForYourBuck,
    '24': LBMSHoming,
    '25': LBMSRocketPowered,
    '26': LBMSSmokyEyeSurprise,
    '27': LBMSTheRLL,
    '28': LBMSBlotOutTheSun,
    '29': LBMSConked,
    '30': LBMSSwarm,
}

sample_longbow_build = {
    'slot_mouse_two': ['11', 1],
    'slot_one': ['22', 1],
    'slot_two': ['20', 1],
    'slot_three': ['11', 2],
    'slot_four': ['1', 3],
    'slot_q': ['25', 1],
    'slot_e': ['15', 1],
    'passive_one': ['4', 1],
    'passive_two': ['16', 1],
    'passive_three': ['13', 1],
}
