from ability import * # noqa
# import random

class PlasmaslingerAbility(Ability):
    def __init__(self, *args, **kwargs):
        super(PlasmaslingerAbility, self).__init__(*args, **kwargs)
        self.plasma = 100
        self.max_plasma = 100
        self.vat = pyglet.sprite.Sprite(load_image('plasma_vat.png', anchor=False), window_width-472, 0, batch=gfx_batch),  # noqa

    def action_checks(self, plasma):
        if self.target:
            if not self.global_cooldown:
                if self.plasma >= plasma:
                    return True
        return False

    def update_plasma(self):
        if self.plasma < self.max_plasma:
            self.plasma += .3 * self.plasma / self.max_plasma + .05
            # self.plasma += .03
        else:
            self.plasma = self.max_plasma

    def update(self):
        self.update_plasma()
        ph = int(max(115 * self.plasma / 100, 1))
        self.plasma_bar = pyglet.sprite.Sprite(
            pyglet.image.create(15, ph, green_sprite),
            window_width - 443, 5, batch=BarBatch)

    # def magnum_double_tap(self):
    #     if self.action_checks(10):
    #         if self.gun_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True): # noqa  
    #             self.delayed.append(
    #                 [2,
    #                     partial(self.gun_one.fire, self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True) # noqa
    #                 ]) # noqa
    #             self.trigger_global_cooldown()
    #             self.plasma -= 10

    # def magnum_action_shot(self):
    #     if self.action_checks(11):
    #         self.acc += self.evade
    #         if self.gun_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True): # noqa  
    #             self.trigger_global_cooldown()
    #             self.plasma -= 20
    #         self.acc -= self.evade

    # def magnum_california_prayer_book(self):
    #     if self.action_checks(30):
    #         if self.gun_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True): # noqa  
    #             self.trigger_global_cooldown()
    #             keep_going = 1
    #             keep_count = 0
    #             while keep_going:
    #                 if random.choice([1, 1, 1, 0]):
    #                     keep_count += 1
    #                     self.delayed.append(
    #                         [4 * keep_count,
    #                         partial(self.gun_one.fire, self.sprite.x,
    #                         self.sprite.y, self.target.sprite.x,
    #                         self.target.sprite.y, self, self.target, True)]
    #                     )
    #                 else:
    #                     keep_going = 0

    #             self.master.spriteeffect.message(self.sprite.x, self.sprite.y, 'shot: ' + str(keep_count), time=90) # noqa
    #             self.plasma -= 30
