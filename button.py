import pyglet
from utility import LabelBatch


def foo():
    print "hello"


class Manager(object):
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def update(self, x, y, mode):
        for button in self.buttons:
            button.on_mouse_press(x, y, mode)

    def update_image(self, x, y, dx, dy):
        for button in self.buttons:
            button.on_mouse_motion(x, y, dx, dy)


class Button(object):
    def __init__(self, upsprite, hoversprite, downsprite, x, y, callback=None, batch=None, label=None):
        self.func = callback
        self.upsprite = upsprite
        self.downsprite = downsprite
        self.hoversprite = hoversprite
        self.trigger = 0
        self.sprite = pyglet.sprite.Sprite(
            upsprite,
            x, y, batch=batch
        )
        if label is not None:
            self.label = pyglet.text.Label(
                label,
                font_name='Times New Roman',
                font_size=32,
                x=self.sprite.x + self.sprite.width / 2,
                y=self.sprite.y + self.sprite.height / 2,
                anchor_x='center',
                anchor_y='center',
                batch=LabelBatch
            )

    def on_press(self):
        pass

    def on_mouse_motion(self, x, y):
        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height):
            self.sprite.image = self.hoversprite
        else:
            self.trigger = 0
            self.sprite.image = self.upsprite

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
                self.sprite.image = self.hoversprite

                self.func()
            if mode == 0:
                self.sprite.image = self.downsprite
                self.trigger = 1


class DraggableButton(Button):
    def __init__(self, upsprite, hoversprite, downsprite, x, y, callback=None, batch=None, label=None):
        super(DraggableButton, self).__init__(
            upsprite, hoversprite, downsprite, x, y,
            callback, batch, label
        )

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
        else:
            self.trigger = 0
            self.sprite.image = self.upsprite


class TextBox(Button):
    def __init__(self, upsprite, hoversprite, downsprite, x, y, callback=None, batch=None, label=None):
        super(TextBox, self).__init__(
            upsprite, hoversprite, downsprite, x, y,
            callback, batch, ' '
        )

    def delete(self):
        self.label.text = self.label.text[:-1]

    def add_text(self, key):
        self.label.text = self.label.text + chr(key)

    def on_mouse_press(self, x, y, mode):
        if (
            self.sprite.x < x and
            x < self.sprite.x + self.sprite.width and
            self.sprite.y < y and
            y < self.sprite.y + self.sprite.height
        ):
            if mode == 1 and self.trigger == 1:
                self.trigger = 0
                self.sprite.image = self.downsprite

                self.func()
            if mode == 0:
                self.sprite.image = self.downsprite
                self.trigger = 1
