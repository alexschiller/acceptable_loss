import pyglet
from utility import LabelBatch
from collide import * # noqa


class Clickable(object):
    def __init__(self, upsprite, x, y, callback=None, batch=None):
        self.func = callback
        self.upsprite = upsprite
        self.trigger = 0
        self.sprite = pyglet.sprite.Sprite(
            upsprite,
            x, y, batch=batch
        )

    def on_mouse_motion(self, x, y, dx, dy):
        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height):
            print 'whats up kitty cat'
        else:
            self.trigger = 0

    def move(self, x, y):
        self.sprite.x, self.label.x = x, x
        self.sprite.y, self.label.y = y, y

    def on_mouse_press(self, x, y, mode):
        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height):
            if mode == 1 and self.trigger == 1:
                self.trigger = 0
                try:
                    self.func()
                except:
                    pass
            if mode == 0:
                self.trigger = 1


class Placeable(Clickable):
    def __init__(self, upsprite, x, y, callback=None, batch=None):
        super(Placeable, self).__init__(
            upsprite, x, y,
            callback, batch
        )
        self.collision = SpriteCollision(self.sprite)

    def on_collide(self, button):
        ret = calc_vel_xy(
            self.sprite.x, self.sprite.y,
            button.sprite.x, button.sprite.y, 10
        )
        self.sprite.x += ret[0]
        self.sprite.y += ret[1]

    def on_mouse_press(self, x, y, mode):
        if (
            self.sprite.x < x and
            x < self.sprite.x + self.sprite.width and
            self.sprite.y < y and
            y < self.sprite.y + self.sprite.height
        ):
            if mode == 1 and self.trigger == 1:
                self.trigger = 0
                self.sprite.image = self.hoversprite

                self.func()
            if mode == 0:
                self.sprite.image = self.downsprite
                self.trigger = 1

    def on_mouse_motion(self, x, y, dx, dy):
        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and self.trigger == 1 and
                y < self.sprite.y + self.sprite.height):
            self.sprite.x += dx
            self.sprite.y += dy
            self.label.x += dx
            self.label.y += dy
            # for buttons in DragButtons:
            #     if collide(self.collision, buttons.collision) and buttons is not self:
            #         print "OK"
            #         self.on_collide(buttons)
        else:
            self.trigger = 0
            self.sprite.image = self.upsprite
