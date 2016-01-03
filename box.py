from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet
from gun import * # noqa


class Box(object):
    def __init__(self, master):
        self.sprite = pyglet.sprite.Sprite(load_image('box.png'),
            random.randint(50, 1350), random.randint(50, 750), batch=gfx_batch)
        self.collision = SpriteCollision(self.sprite)
        self.health = 1000
        self.max_health = 1000.0
