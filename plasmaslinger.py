from player import * # noqa
import random

class Plasmaslinger(Player):
    def __init__(self, *args, **kwargs):
        super(Plasmaslinger, self).__init__(*args, **kwargs)
        self.plasma = 100
        self.max_plasma = 100
        self.slot_one_time = None
        self.vat = pyglet.sprite.Sprite(load_image('plasma_vat.png', anchor=False), window_width-472, 0, batch=gfx_batch),  # noqa
        self.hp_shield_bar = pyglet.sprite.Sprite(load_image('hp_shield.png', anchor=False), window_width - 1050, 0, batch=gfx_batch),  # noqa
        self.evade_acc_bar = pyglet.sprite.Sprite(load_image('evade_acc.png', anchor=False), window_width - 415, 0, batch=gfx_batch),  # noqa
        self.gun_one = Gun(master, base=pm_magnum)
        self.gun_two = Gun(master, base=pm_carbine)

        self.guns = [self.gun_one, self.gun_two]
        self.gun = self.guns[1]
        self.master.register_guns([self.gun_one, self.gun_two])
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
                p[1]()
                self.delayed.remove(p)

    def slot_one_fire(self):
        self.magnum_double_tap()

    def slot_two_fire(self):
        self.magnum_california_prayer_book()

    def update_plasma(self):
        if self.plasma < self.max_plasma:
            self.plasma += .3 * self.plasma / self.max_plasma + .05
            # self.plasma += .03
        else:
            self.plasma = self.max_plasma

    def update(self):
        self.update_delayed()

        try:
            self.check_object_collision(self.closest_object())
        except:
            pass
        self.update_plasma()
        if self.energy < 100:
            self.energy += 1

        if self.shield < self.max_shield:
            self.shield += .016
        ph = int(max(115 * self.plasma / 100, 1))
        sw = int(max(115 * self.shield / self.max_shield, 1))
        hw = int(max(115 * self.health / self.max_health, 1))
        ae = (window_width - 410) + self.evade / 10 * 70

        self.shield_bar = pyglet.sprite.Sprite(
            pyglet.image.create(sw, 15, blue_sprite),
            window_width - 1045, 30, batch=BarBatch)

        self.health_bar = pyglet.sprite.Sprite(
            pyglet.image.create(hw, 15, red_sprite),
            window_width - 1045, 5, batch=BarBatch)

        self.plasma_bar = pyglet.sprite.Sprite(
            pyglet.image.create(15, ph, green_sprite),
            window_width - 443, 5, batch=BarBatch)

        self.ae_bar = pyglet.sprite.Sprite(
            pyglet.image.create(70, 20, white_sprite),
            ae, 5, batch=BarBatch)

    def action_checks(self, plasma):
        if self.target:
            if not self.global_cooldown:
                if self.plasma >= plasma:
                    return True
        return False

    def magnum_double_tap(self):
        if self.action_checks(20):
            if self.gun_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True): # noqa  
                self.delayed.append(
                    [2,
                        partial(self.gun_one.fire, self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True) # noqa
                    ]) # noqa
                self.trigger_global_cooldown()
                self.plasma -= 20

    def magnum_action_shot(self):
        if self.action_checks(11):
            self.acc += self.evade
            if self.gun_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True): # noqa  
                self.trigger_global_cooldown()
                self.plasma -= 20
            self.acc -= self.evade

    def magnum_california_prayer_book(self):
        if self.action_checks(20):
            if self.gun_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True): # noqa  
                self.trigger_global_cooldown()
                lottery = random.choice([[1, 'W'], [20, 'L']])
                self.master.spriteeffect.message(self.sprite.x, self.sprite.y, lottery[1]) # noqa
                self.plasma -= lottery[0]
