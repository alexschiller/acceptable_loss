from baseskills import * # noqa

class Build(object):
    def __init__(self, master, handler, skillset, build):
        self.master = master
        self.build = build
        self.handler = handler
        self.skillset = skillset
        self.create_load_out()

    def create_load_out(self):
        self.slot_mouse_two = self.skillset.get(self.build['slot_mouse_two'][0], Skill(self.master, 1, self.handler))(self.master, self.build['slot_mouse_two'][1], self.handler)
        self.slot_one = self.skillset.get(self.build['slot_one'][0], Skill(self.master, 1, self.handler))(self.master, self.build['slot_one'][1], self.handler)
        self.slot_two = self.skillset.get(self.build['slot_two'][0], Skill(self.master, 1, self.handler))(self.master, self.build['slot_two'][1], self.handler)
        self.slot_three = self.skillset.get(self.build['slot_three'][0], Skill(self.master, 1, self.handler))(self.master, self.build['slot_three'][1], self.handler)
        self.slot_four = self.skillset.get(self.build['slot_four'][0], Skill(self.master, 1, self.handler))(self.master, self.build['slot_four'][1], self.handler)
        self.slot_q = self.skillset.get(self.build['slot_q'][0], Skill(self.master, 1, self.handler))(self.master, self.build['slot_q'][1], self.handler)
        self.slot_e = self.skillset.get(self.build['slot_e'][0], Skill(self.master, 1, self.handler))(self.master, self.build['slot_e'][1], self.handler)
