from build import Skill

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
