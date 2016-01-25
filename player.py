from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa
from functools import partial # noqa


class Player(Character):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.hp_shield_bar = pyglet.sprite.Sprite(load_image('hp_shield.png', anchor=False), window_width - 1050, 0, batch=gfx_batch),  # noqa
        self.evade_acc_bar = pyglet.sprite.Sprite(load_image('evade_acc.png', anchor=False), window_width - 415, 0, batch=gfx_batch),  # noqa
        self.energy = 100
        self.inventory = []

    def update_bars(self):
        if self.energy < 100:
            self.energy = 100
        sw = int(max(115 * self.stats.shield / self.stats.shield_max, 1))
        hw = int(max(115 * self.stats.health / self.stats.health_max, 1))
        ae = (window_width - 410) + self.stats.evade_move / 10 * 70

        self.shield_bar = pyglet.sprite.Sprite(
            pyglet.image.create(sw, 15, blue_sprite),
            window_width - 1045, 30, batch=BarBatch)

        self.health_bar = pyglet.sprite.Sprite(
            pyglet.image.create(hw, 15, red_sprite),
            window_width - 1045, 5, batch=BarBatch)

        self.ae_bar = pyglet.sprite.Sprite(
            pyglet.image.create(70, 20, white_sprite),
            ae, 5, batch=BarBatch)
