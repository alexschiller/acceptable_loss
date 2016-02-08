import pyglet # noqa

from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa
import threading
import thread # noqa
import time# noqa
from utility import * # noqa
import sys # noqa

theader = 1
window_height = 800
window_width = 1400


window = pyglet.window.Window(window_width, window_height)


class ProtoKeyStateHandler(key.KeyStateHandler):

    def __init__(self):
        self.list = []
        self.active = False

    def on_key_press(self, symbol, modifiers):
        self[symbol] = True
        if self.active:
            self.list.append(symbol)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def clear_state(self):
        self.list = []

    def get_next_item(self):
        if len(self.list) > 0:
            return self.list.pop(0)
        else:
            return False
key_handler = ProtoKeyStateHandler()

batches = [pyglet.graphics.Batch()]

sprite = pyglet.sprite.Sprite(
    button,
    10, 10, batch=batches[0]
)


class Threads(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)


def update(ts):
        while(1):
            if key_handler[key.D]:
                sprite.x += 1
            if key_handler[key.A]:
                sprite.x -= 1
            if key_handler[key.W]:
                print "SUP"
                sprite.y += 1
            if key_handler[key.S]:
                print "ok"
                sprite.y -= 1
            time.sleep(1 / 60)


def render():
        # time2 = time.time()
        # print time2 - self.timex
        # window.clear()
        pyglet.gl.glClearColor(1, 1, 1, 1)
        for batch in batches:
            batch.draw()
        window.flip()
        time.sleep(1 / 60)
        # if(time2 - time.time() < 1 / 60):
        #     self.timex = time2

# def render2(ts):
#     renderer.render()
threader = Threads(update, 1)
threader.daemon = True
states = None

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window.push_handlers(key_handler)


@window.event
def on_draw():
    render()


# pyglet.clock.schedule(render2)
threader.start()
pyglet.app.run()
