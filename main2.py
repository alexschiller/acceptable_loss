import pyglet  # noqa
from pyglet.gl import *  # noqa
from collections import OrderedDict  # noqa
from time import time  # noqa
from os.path import abspath  # noqa
from pyglet.window import key # noqa
import cProfile # noqa
import pstats # noqa
import StringIO # noqa
from energy import * # noqa
from time import time, sleep # noqa
from importer import * # noqa
from states import * # noqa

from button import Manager, Button,TextBox, DraggableButton, foo # noqa
from menu import * # noqa
from hotbar import * # noqa
from inventory import * # noqa


class GameAssets(object):
    def __init__(self):
        self.hb = HotBarManager(hotbar_sprite, master)
        self.bm = BuildingManager(building_menu) # noqa
        self.bum = MenuManager(1200, 0, menu_back) # noqa
        self.bum.set_build_manager(buildmanager)
        self.im = Inventory(master) # noqa
        self.hb.setup()


class Game(pyglet.window.Window):
    def __init__(self, height, width):
        super(Game, self).__init__(width, height, caption='Acceptable Loss')
        self.pr = cProfile.Profile()
        self.pr.enable()
        self.assets = GameAssets
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.state_manager = StateManager(self.assets)
        self.alive = True
        self.framerate = 0, time()
        self.count = 0

    def render(self, *args):
        self.clear()
        self.state_manager.current.update(0)

        for batch in self.state_manager.current.batches:
            batch.draw()

        if time() - self.framerate[1] > 1:
            # print('fps:', self.framerate[0])
            self.framerate = 0, time()
        else:
            # Not an optimal way to do it, but it will work.
            self.framerate = self.framerate[0] + 1, self.framerate[1]

        self.flip()

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = False

    # def on_key_press(self, symbol, modkey):
    #     self.state_manager.current.on_key_press(symbol, modkey)

    # def on_key_release(self, symbol, modkey):
    #     self.state_manager.current.on_key_release(symbol, modkey)

    def on_mouse_release(self, x, y, button, modifiers):
        self.state_manager.current.on_mouse_release(x, y, button, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.state_manager.current.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        mouse_position = [x, y] # noqa
        self.state_manager.current.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        mouse_position = [x, y] # noqa
        self.state_manager.current.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def run(self):
        while self.alive:
            event = self.dispatch_events()
            if event:
                print(event)
            self.render()

game = Game(window_height, window_width)
game.push_handlers(key_handler)

if __name__ == '__main__':
    pyglet.clock.set_fps_limit(10)

    game.run()