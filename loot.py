from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
import math
from gun import * # noqa

class Content(object):
    def __init__(self, loot): # noqa
        self.loot = loot
        self.wait = 60
        self.vel_x = 0
        self.vel_y = 0
        self.travel = 1
        self.travelled = 0

    def draw(self, x, y):
        effect_color = pyglet.image.SolidColorImagePattern(color=(0, 255, 0, 255))
        effect_shape = pyglet.image.create(10, 10, effect_color)
        self.sprite = pyglet.sprite.Sprite(effect_shape, x, y, batch=EffectsBatch) # noqa

    def update(self):
        if self.wait > 0:
            self.wait -= 1
        elif self.travelled == 0:
            ret = calc_vel_xy(window_width, 0,
                self.sprite.x, self.sprite.y, 30)
            self.vel_x = ret[0]
            self.vel_y = ret[1]
            self.travel = math.hypot(abs(self.sprite.x - window_width),
                abs(self.sprite.y))

        self.sprite.x += self.vel_x
        self.sprite.y += self.vel_y
        self.travelled += math.hypot(self.vel_x, self.vel_y)

class Package(object):
    def __init__(self, x, y, contents): # noqa
        self.x = x
        self.y = y
        self.contents = contents
        effect_color = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 255))
        effect_shape = pyglet.image.create(10, 10, effect_color)

        self.sprite = pyglet.sprite.Sprite(effect_shape, x, y, batch=EffectsBatch)
        self.collision = SpriteCollision(self.sprite)

class Loot(object):
    def __init__(self, master):
        self.current_loot = []
        self.moving_loot = []
        self.master = master
        self.resource_fun = {
            'foo': self.add_foo,
            'pow': self.add_pow,
            'eng': self.add_eng,
            'sci': self.add_sci,
            'mon': self.add_mon,
        }

    def add_foo(self, amount):
        return Content(amount)

    def add_pow(self, amount):
        return Content(amount)

    def add_eng(self, amount):
        return Content(amount)

    def add_sci(self, amount):
        return Content(amount)

    def add_mon(self, amount):
        return Content(amount)

    def pack_package(self, loot, x, y):
        contents = []
        for r in loot['resources'].keys():
            contents.append(self.resource_fun[r](loot['resources'][r]))

        self.current_loot.append(Package(x, y, contents))

    def unpack_package(self, package):
        for n, c in enumerate(package.contents):
            c.draw(package.sprite.x, package.sprite.y + 20 * n)
            self.moving_loot.append(c)
        self.delete_package(package)

    def delete_package(self, package):
        package.sprite.delete()
        self.current_loot.remove(package)

    def give_loot(self, content):
        pass

    def delete_content(self, content):
        self.give_loot(content)
        try:
            content.sprite.delete()
            self.moving_loot.remove(content)
        except:
            pass

    def update(self):
        for p in self.current_loot:
            if collide(p.collision, self.master.player.collision):
                self.unpack_package(p)
        for c in self.moving_loot:
            c.update()
            if c.travelled >= c.travel:
                self.delete_content(c)
