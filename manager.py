import pyglet  # noqa
from pyglet.gl import *  # noqa
from collections import OrderedDict  # noqa
from time import time  # noqa
from os.path import abspath  # noqa

import cProfile # noqa
import pstats # noqa
import StringIO # noqa

window_height = 800
window_width = 1400

class StateHandler(object):
    def __init__(self):
        self.main_menu_state = MainMenu()
        self.game_state = MainMenu()

class StateObject(object):
    def __init__(self):
        self.batches = OrderedDict([])
        self.stop = 0

    def on_key_press(self, symbol, modkey):
        pass

    def on_key_release(self, symbol, modkey):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def update(self):
        pass

class MainMenuState(StateObject):
    def __init__(self):
        super(MainMenuState, self).__init__()

        self.batches = OrderedDict([
            ('gfx', pyglet.graphics.Batch())  # this should order them properly?
        ])
        img = pyglet.image.load('images/title_2.png')
        img.anchor_x = 0
        img.anchor_y = img.height

        self.background = pyglet.sprite.Sprite(
            img, 0, window_height,
            batch=self.batches['gfx']
        )

class GameState(StateObject):
    def __init__(self):
        super(MainMenu, self).__init__()

        self.batches = OrderedDict([
            ('gfx', pyglet.graphics.Batch())
        ])

class Game(pyglet.window.Window):
    def __init__(self, height, width):
        super(Game, self).__init__(width, height, caption='Test')
        self.pr = cProfile.Profile()
        self.pr.enable()

        pyglet.gl.glClearColor(1, 1, 1, 1)

        self.alive = True
        self.framerate = 0, time()
        self.count = 0
        self.load_new_state(MainMenuState)

    def load_new_state(self, new_state):
        self.state = new_state()
        self.batches = self.state.batches

    def render(self, *args):
        self.clear()
        self.state.update()

        for batch in self.batches.values():
            batch.draw()

        if time() - self.framerate[1] > 1:
            print('fps:', self.framerate[0])
            self.framerate = 0, time()
        else:
            # Not an optimal way to do it, but it will work.
            self.framerate = self.framerate[0] + 1, self.framerate[1]

        self.flip()

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = False

    def on_key_press(self, symbol, modkey):
        self.state.on_key_press(symbol, modkey)

    def on_key_release(self, symbol, modkey):
        self.state.on_key_release(symbol, modkey)

    def on_mouse_release(self, x, y, button, modifiers):
        self.state.on_mouse_release(x, y, button, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.state.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.state.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.state.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def run(self):
        while self.alive:
            event = self.dispatch_events()
            if event:
                print(event)
            self.render()


if __name__ == '__main__':
    game = Game(window_height, window_width)
    pyglet.clock.set_fps_limit(60)
    game.run()
