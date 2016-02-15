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
import threading # noqa
import thread # noqa


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

window_height = 800
window_width = 1400
global mouse_position
mouse_position = [0, 0]


class StateHandler(object):
    def __init__(self):
        self.main_menu_state = MainMenuState()
        self.game_state = GameState()


class StateObject(object):
    def __init__(self):
        self.change = 0
        self.batches = OrderedDict([])

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

    def on_key_press(self, symbol, modkey):
        self.change = 1
        self.change_state = GameState


class GameState(StateObject):
    def __init__(self):
        super(GameState, self).__init__()
        self.batches = OrderedDict([
            ('gfx', pyglet.graphics.Batch())
        ])
        ready_level(master, 5, 5)
        self.last_time = 0

    def update(self):
        mx = 0
        my = 0
        if key_handler[key.X]:
            if collide(master.player.collision, master.ready.portal.collision):
                reset_imp()
                master.reset()
                master.player.sprite.x = master.home.x
                master.player.sprite.y = master.home.y

        if key_handler[key.H]:
            readjust_x = master.home.x - master.player.sprite.x
            readjust_y = master.home.y - master.player.sprite.y
            master.player.sprite.x = master.home.x
            master.player.sprite.y = master.home.y
            master.move_all(-readjust_x, -readjust_y)
        if key_handler[key.TAB]:
            master.pr.disable()
            s = StringIO.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(master.pr, stream=s).sort_stats(sortby)
            ps.print_stats()

            f = open('output.txt', 'w')
            f.write(s.getvalue())
            # print s.getvalue()
            # master.player_controller.target_closest_enemy()
        if key_handler[key.D]:
            mx += 1
        if key_handler[key.A]:
            mx -= 1
        if key_handler[key.W]:
            my += 1
        if key_handler[key.S]:
            my -= 1
        master.player_controller.move(mx, my)

        if key_handler[key._1]:
            master.player_controller.slot_one_fire()

        if key_handler[key._2]:
            master.player_controller.slot_two_fire()

        if key_handler[key._3]:
            master.player_controller.slot_three_fire()

        if key_handler[key._4]:
            master.player_controller.slot_four_fire()

        if key_handler[key._5]:
            master.player_controller.slot_five_fire()

        if key_handler[key.SPACE]:
            master.player.jump()

        # master.player.move(mx, my)

        # if key_handler[key.Q]:
        #     master.grenade.throw(
        #         master.player.sprite.x,
        #         master.player.sprite.y, mouse_position[0],
        #         mouse_position[1]
        # )

        if key_handler[key.F] and master.player.energy >= 100:
            # teleport(master, mouse_position)
            teleport(master, mouse_position)
        # Run Updates
        master.update()

        TerrainBatch.draw()
        PortalBatch.draw()
        BuildingBatch.draw()
        BulletBatch.draw()
        gfx_batch.draw()
        EffectsBatch.draw()
        BarBatch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 4:
            master.player_controller.slot_mouse_two_fire()

    def on_mouse_motion(self, x, y, dx, dy):
        master.player_controller.sprite.x = x
        master.player_controller.sprite.y = y
        master.player_controller.rotate(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        master.player_controller.sprite.x = x
        master.player_controller.sprite.y = y

        # if button == 4:
        master.player_controller.slot_mouse_two_fire()
        master.update_button_image(x, y, dx, dy)


class Game(pyglet.window.Window):
    def __init__(self, height, width):
        super(Game, self).__init__(width, height, caption='Acceptable Loss')
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
        if self.state.change:
            self.load_new_state(self.state.change_state)
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

game = Game(window_height, window_width)
key_handler = ProtoKeyStateHandler()
game.push_handlers(key_handler)

if __name__ == '__main__':
    pyglet.clock.set_fps_limit(10)

    game.run()
