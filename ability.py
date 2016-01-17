from functools import partial

class Ability(object):
    def __init__(self, master, owner, gun_one, gun_two):
        self.gun_one = gun_one
        self.gun_two = gun_two

        self.delayed = []
        self.global_cooldown = False

    def global_cooldown_reset(self):  # this is a super tacky way to do this for sure...
        self.global_cooldown = False

    def trigger_global_cooldown(self):
        self.global_cooldown = True
        self.delayed.append([30, partial(self.global_cooldown_reset)])

    def update_delayed(self):
        for p in self.delayed:
            p[0] -= 1
            if p[0] == 0:
                try:
                    p[1]()
                except:
                    'failed delayed action'
                self.delayed.remove(p)

    def update(self):
        self.update_delayed()
