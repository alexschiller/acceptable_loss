from importer import * # noqa
import pyglet # noqa
import random # noqa
import json # noqa
from collide import * # noqa
from character import * # noqa
from enemy import * # noqa


window_height = 800
window_width = 1400


class Portal(object):
    def __init__(self, x, y, width, height, batch, master):
        h_choice = random.randint(0, height)
        w_choice = random.randint(0, width)
        self.sprite = pyglet.sprite.Sprite(
            load_image('portal.png'),
            x + w_choice, y + h_choice, batch=batch
        )
        self.collision = SpriteCollision(self.sprite)
        self.manager = master

    def on_colide(self):
        master.reset()

    def move(self, dx, dy):
        self.sprite.x += dx
        self.sprite.y += dy

    def update(self):
        self.sprite.rotation += 3
        if self.sprite.rotation > 359:
            self.sprite.rotation = self.sprite.rotation - 360


class Room(object):
    def __init__(self):
        pass


class Dungeon(object):
    def __init__(self):
        pass
