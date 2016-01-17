from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa
from functools import partial # noqa
from ability import * # noqa
# import random

class BolaEffect(object):
    def __init__(self, master, owner, start_x, start_y, target_x, target_y): # noqa
        self.sprite = pyglet.sprite.Sprite(load_image('bola.png'), start_x, start_y, batch=gfx_batch) # noqa
        self.travel = 200 + random.randint(-50, 50)
        self.master = master
        self.owner = owner
        self.target_x = target_x
        self.target_y = target_y
        self.start_x = start_x
        self.start_y = start_y
        ret = calc_vel_xy(target_x, target_y,
            start_x, start_y, random.randint(7, 10))

        self.vel_x = ret[0] + random.randint(-2, 2)
        self.vel_y = ret[1] + random.randint(-2, 2)

        self.travelled = 0

    def remove_bola(self):
        self.master.spriteeffect.bola_explosion(self.sprite.x, self.sprite.y)
        try:
            self.sprite.delete()
            self.owner.queue.remove(self)
        except:
            pass

    def get_target(self):
        try:
            min_dist = 300  # must be within 300 of the bola
            x1 = self.sprite.x
            y1 = self.sprite.y
            self.target = None
            for e in self.master.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    self.target = e
        except:
            self.target = None

    def shoot(self):
        self.get_target()
        if self.target:
            self.owner.gun_one.fire(self.sprite.x,
                self.sprite.y,
                self.target.sprite.x,
                self.target.sprite.y,
                self.owner.owner, self.target,
            True)
        self.remove_bola()

    def update(self):
        self.sprite.rotation += 5
        try:
            self.sprite.x += self.vel_x
            self.sprite.y += self.vel_y
            self.travelled += math.hypot(self.vel_x, self.vel_y)
            if self.travelled > self.travel:
                self.shoot()
        except:
            pass

class PlasmaslingerAbility(Ability):
    def __init__(self, *args, **kwargs):
        super(PlasmaslingerAbility, self).__init__(*args, **kwargs)
        self.plasma = 100
        self.max_plasma = 100
        self.vat = pyglet.sprite.Sprite(load_image('plasma_vat.png', anchor=False), window_width-472, 0, batch=gfx_batch),  # noqa
        self.queue = []

    def update(self):
        self.update_plasma()
        self.update_delayed()
        for q in self.queue:
            q.update()

        ph = int(max(115 * self.plasma / 100, 1))
        self.plasma_bar = pyglet.sprite.Sprite(
            pyglet.image.create(15, ph, green_sprite),
            window_width - 443, 5, batch=BarBatch)

    def action_checks(self, plasma):
        if self.owner.target:
            if not self.global_cooldown:
                if self.plasma >= plasma:
                    return True
        return False

    def update_plasma(self):
        if self.plasma < self.max_plasma:
            self.plasma += .3 * self.plasma / self.max_plasma + .05
        else:
            self.plasma = self.max_plasma

    def magnum_double_tap(self):
        if self.action_checks(10):
            if self.gun_one.fire(self.owner.sprite.x,
                self.owner.sprite.y,
                self.owner.target.sprite.x,
                self.owner.target.sprite.y,
                self.owner, self.owner.target,
            True):
                self.delayed.append(
                    [2,
                        partial(self.gun_one.fire,
                        self.owner.sprite.x,
                        self.owner.sprite.y,
                        self.owner.target.sprite.x,
                        self.owner.target.sprite.y,
                        self.owner,
                        self.owner.target, True)
                    ]) # noqa
                self.trigger_global_cooldown()
                self.plasma -= 10

    def magnum_five_beans_in_the_wheel(self):
        if self.action_checks(30):
            for i in range(5):
                self.queue.append(
                    BolaEffect(self.master, self, self.owner.sprite.x,
                    self.owner.sprite.y, self.owner.target.sprite.x,
                    self.owner.target.sprite.y,)
                )
            self.trigger_global_cooldown()
            self.plasma -= 30

    # def magnum_action_shot(self):
    #     if self.action_checks(11):
    #         self.acc += self.evade
    #         if self.gun_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True): # noqa  
    #             self.trigger_global_cooldown()
    #             self.plasma -= 20
    #         self.acc -= self.evade

    def magnum_california_prayer_book(self):
        if self.action_checks(30):
            keep_going = 1
            keep_count = 0
            while keep_going:
                if random.choice([1, 1, 1, 0]):
                    self.queue.append(
                        BolaEffect(self.master, self, self.owner.sprite.x,
                            self.owner.sprite.y, self.owner.target.sprite.x,
                            self.owner.target.sprite.y,)
                    )
                    keep_count += 1
                else:
                    keep_going = 0
            self.master.spriteeffect.message(self.owner.sprite.x, self.owner.sprite.y, 'shot: ' + str(keep_count), time=90) # noqa                    
            self.trigger_global_cooldown()
            self.plasma -= 30

            # if self.gun_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target, True): # noqa  
            #     self.trigger_global_cooldown()
            #     keep_going = 1
            #     keep_count = 0
            #     while keep_going:
            #         if random.choice([1, 1, 1, 0]):
            #             keep_count += 1
            #             self.delayed.append(
            #                 [4 * keep_count,
            #                 partial(self.gun_one.fire, self.sprite.x,
            #                 self.sprite.y, self.target.sprite.x,
            #                 self.target.sprite.y, self, self.target, True)]
            #             )
            #         else:
            #             keep_going = 0

                # self.master.spriteeffect.message(self.sprite.x, self.sprite.y, 'shot: ' + str(keep_count), time=90) # noqa
