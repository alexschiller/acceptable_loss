
class Skill(object):
    def __init__(self, master, level):
        self.master = master

    def use(self):
        pass

class Build(object):
    def __init__(self, master, build):
        self.master = master
        self.build = {}

    def create_load_out(self):
        self.slot_mouse_one = self.build.get('slot_mouse_one', Skill(self.master, 1))
        self.slot_mouse_two = self.build.get('slot_mouse_two', Skill(self.master, 1))
        self.slot_one = self.build.get('slot_one', Skill(self.master, 1))
        self.slot_two = self.build.get('slot_two', Skill(self.master, 1))
        self.slot_three = self.build.get('slot_three', Skill(self.master, 1))
        self.slot_four = self.build.get('slot_four', Skill(self.master, 1))
        self.slot_five = self.build.get('slot_five', Skill(self.master, 1))
        self.slot_q = self.build.get('slot_q', Skill(self.master, 1))
        self.slot_e = self.build.get('slot_e', Skill(self.master, 1))

# Unfinished
class LBALTimedBreathing(Skill):
    def __init__(self, master, level):
        super(LBALTimedBreathing, self).__init__(master, level)

# Unfinished
class LBALFlakJacket(Skill):
    def __init__(self, master, level):
        super(LBALFlakJacket, self).__init__(master, level)

# Unfinished
class LBALTwentyMileMarch(Skill):
    def __init__(self, master, level):
        super(LBALTwentyMileMarch, self).__init__(master, level)

# Unfinished
class LBALLockAndLoad(Skill):
    def __init__(self, master, level):
        super(LBALLockAndLoad, self).__init__(master, level)

# Unfinished
class LBALFletcher(Skill):
    def __init__(self, master, level):
        super(LBALFletcher, self).__init__(master, level)

# Unfinished
class LBALSpotAndShot(Skill):
    def __init__(self, master, level):
        super(LBALSpotAndShot, self).__init__(master, level)

# Unfinished
class LBALIronRations(Skill):
    def __init__(self, master, level):
        super(LBALIronRations, self).__init__(master, level)

# Unfinished
class LBALStrafe(Skill):
    def __init__(self, master, level):
        super(LBALStrafe, self).__init__(master, level)

# Unfinished
class LBALCannibalize(Skill):
    def __init__(self, master, level):
        super(LBALCannibalize, self).__init__(master, level)

# Unfinished
class LBALBarrage(Skill):
    def __init__(self, master, level):
        super(LBALBarrage, self).__init__(master, level)

# Unfinished
class LBACTrigger(Skill):
    def __init__(self, master, level):
        super(LBACTrigger, self).__init__(master, level)

# Unfinished
class LBACSalted(Skill):
    def __init__(self, master, level):
        super(LBACSalted, self).__init__(master, level)

# Unfinished
class LBACMuzzleBrake(Skill):
    def __init__(self, master, level):
        super(LBACMuzzleBrake, self).__init__(master, level)

# Unfinished
class LBACPointBlank(Skill):
    def __init__(self, master, level):
        super(LBACPointBlank, self).__init__(master, level)

# Unfinished
class LBACIronDome(Skill):
    def __init__(self, master, level):
        super(LBACIronDome, self).__init__(master, level)

# Unfinished
class LBACHardCore(Skill):
    def __init__(self, master, level):
        super(LBACHardCore, self).__init__(master, level)

# Unfinished
class LBACTotalSystemShock(Skill):
    def __init__(self, master, level):
        super(LBACTotalSystemShock, self).__init__(master, level)

# Unfinished
class LBACBurst(Skill):
    def __init__(self, master, level):
        super(LBACBurst, self).__init__(master, level)

# Unfinished
class LBACTriggerDiscipline(Skill):
    def __init__(self, master, level):
        super(LBACTriggerDiscipline, self).__init__(master, level)

# Unfinished
class LBACSalvo(Skill):
    def __init__(self, master, level):
        super(LBACSalvo, self).__init__(master, level)

# Unfinished
class LBMSLaunch(Skill):
    def __init__(self, master, level):
        super(LBMSLaunch, self).__init__(master, level)

# Unfinished
class LBMSNeedle(Skill):
    def __init__(self, master, level):
        super(LBMSNeedle, self).__init__(master, level)

# Unfinished
class LBMSBangForYourBuck(Skill):
    def __init__(self, master, level):
        super(LBMSBangForYourBuck, self).__init__(master, level)

# Unfinished
class LBMSHoming(Skill):
    def __init__(self, master, level):
        super(LBMSHoming, self).__init__(master, level)

# Unfinished
class LBMSRocketPowered(Skill):
    def __init__(self, master, level):
        super(LBMSRocketPowered, self).__init__(master, level)

# Unfinished
class LBMSSmokyEyeSurprise(Skill):
    def __init__(self, master, level):
        super(LBMSSmokyEyeSurprise, self).__init__(master, level)

# Unfinished
class LBMSTheRLL(Skill):
    def __init__(self, master, level):
        super(LBMSTheRLL, self).__init__(master, level)

# Unfinished
class LBMSBlotOutTheSun(Skill):
    def __init__(self, master, level):
        super(LBMSBlotOutTheSun, self).__init__(master, level)

# Unfinished
class LBMSConked(Skill):
    def __init__(self, master, level):
        super(LBMSConked, self).__init__(master, level)

# Unfinished
class LBMSSwarm(Skill):
    def __init__(self, master, level):
        super(LBMSSwarm, self).__init__(master, level)

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
