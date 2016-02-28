from baseskills import * # noqa
# import math
# from functools import partial
from utility import * # noqa

class PlasmaCore(Core):
    def __init__(self, master, handler):
        super(PlasmaCore, self).__init__(master, handler)

    def update(self):
        pass
        # self.add_nano()
        # for n in self.nano:
        #     n.update()
        # for n in self.nano_in_action:
        #     n.update()

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
class PSMASlash(Skill):
    def __init__(self, master, level, handler):
        super(PSMASlash, self).__init__(master, level, handler)

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
class PSPOSlash(Skill):
    def __init__(self, master, level, handler):
        super(PSPOSlash, self).__init__(master, level, handler)

# Unfinished
class PSPOTrips(Skill):
    def __init__(self, master, level, handler):
        super(PSPOTrips, self).__init__(master, level, handler)


# Unfinished
class PSPOBangForYourBuck(Skill):
    def __init__(self, master, level, handler):
        super(PSPOBangForYourBuck, self).__init__(master, level, handler)

# Unfinished
class PSPOAnarchy(Skill):
    def __init__(self, master, level, handler):
        super(PSPOAnarchy, self).__init__(master, level, handler)

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
    '11': PSMASlash,
    '12': PSMABolted,
    '13': PSMAMuzzleBrake,
    '14': PSMACoupled,
    '15': PSMAIronDome,
    '16': PSMAHardCore,
    '17': PSMAPerseverate,
    '18': PSMABurst,
    '19': PSMATriggerDiscipline,
    '20': PSMASalvo,
    '21': PSPOSlash,
    '22': PSPOTrips,
    '23': PSPOBangForYourBuck,
    '24': PSPOAnarchy,
    '25': PSPORocketPowered,
    '26': PSPOSmokyEyeSurprise,
    '27': PSPOTracer,
    '28': PSPOBlotOutTheSun,
    '29': PSPOConked,
    '30': PSPOMayhem,
}

sample_plasmaslinger_build = {
    'slot_mouse_two': ['21', 1],
    'slot_one': ['18', 1],
    'slot_two': ['12', 1],
    'slot_three': ['12', 2],
    'slot_four': ['12', 3],
    'slot_q': ['1', 1],
    'slot_e': ['1', 1],
    'passive_one': ['1', 1],
    'passive_two': ['1', 1],
    'passive_three': ['1', 1],
}
