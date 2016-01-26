import pyglet

from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa

from importer import * # noqa # Put random file imports here for now

from button import Manager, Button,TextBox, DraggableButton, foo # noqa
from placeable import * # noqa
from menu import * # noqa
from hotbar import * # noqa
from inventory import * # noqa


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
states = None
window = pyglet.window.Window(window_width, window_height)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window.push_handlers(key_handler)

#  Align sprite to mouse

global mouse_position
mouse_position = [0, 0]


@window.event
def on_mouse_motion(x, y, dx, dy):
    states.current.on_mouse_motion(x, y, dx, dy)
    global mouse_position
    mouse_position = [x, y]


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    states.current.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    global mouse_position
    mouse_position = [x, y]


@window.event
def on_mouse_release(x, y, button, modifiers):
    states.current.on_mouse_release(x, y, button, modifiers)


@window.event
def on_mouse_press(x, y, button, modifiers):
    states.current.on_mouse_press(x, y, button, modifiers)


class TextState(object):
    def __init__(self, button):
        self.button = button

    def test(self):
        ButtonBatch.draw()
        LabelBatch.draw()

    def update(self, ts):
        symbol = key_handler.get_next_item()
        while (symbol != False): # noqa
            print symbol
            if int(symbol) == 65288:
                self.button.delete()

            elif int(symbol) == 65293:
                key_handler.deactivate()
                key_handler.clear_state()
                states.pop(0)

            elif int(symbol) < 127 and int(symbol) > 31:
                self.button.add_text(symbol)
            symbol = key_handler.get_next_item()
        window.invalid = False


class PauseState():
    def __init__(self):
        self.Pause = 0
        self.manager = Manager()
        buttons = ['hi', 'button', 'chain', 'is', 'a', 'go']
        self.y = 660
        for label in buttons:
            self.manager.add_button(
                DraggableButton(button, buttonhover, buttondown, 650,
                self.y, foo, ButtonBatch, label) # noqa
            )
            self.y -= 110

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.manager.update_image(x, y, dx, dy)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        # thing = TextState(self.manager.buttons[0])
        # key_handler.activate()
        # states.insert(0, thing)

        self.manager.update(x, y, 1)

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.update(x, y, 0)

    def update(self, ts):
        if key_handler[key.P]:
            self.Pause = 1
        else:
            if self.Pause == 1:
                self.Pause = 0
                states.swapback()
        window.invalid = False

    def test(self):
        ButtonBatch.draw()
        LabelBatch.draw()

    def on_draw(self):
        window.clear()
        pyglet.gl.glClearColor(0.75, 0.75, 0.75, 1)  # gray back
        TerrainBatch.draw()
        BuildingBatch.draw()
        BulletBatch.draw()
        gfx_batch.draw()
        EffectsBatch.draw()
        BarBatch.draw()
        states.current.test()
        # MenuBatch.draw()

        window.invalid = False


class MainState(object):
    def __init__(self):
        self.Pause = 0
        self.Build = 0
        self.Menu = 0
        # for i in range(10):
            # master.enemies.append(Soldier(master, base=gen_soldier_base() )) # noqa

        # for i in range(1):
            # master.enemies.append(Portal(master, base=gen_portal_base() )) # noqa            

        # for i in range(0):
            # master.enemies.append(Slime(master, base=gen_slime_base() )) # noqa

    def on_draw(self):
        window.clear()
        pyglet.gl.glClearColor(0.75, 0.75, 0.75, 1)  # gray back
        TerrainBatch.draw()
        master.player.sprite.draw()
        BulletBatch.draw()
        EffectsBatch.draw()
        BarBatch.draw()
        gfx_batch.draw()
        BuildingBatch.draw()
        HotbarBatch.draw()
        HotbarButtonBatch.draw()
        states.current.test()
        Buildmenu.update()
        inventorymenu.update()
        window.invalid = False

    def test(self):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        Buildmenu.on_mouse_press(x, y, 1)
        HotBar.update(x, y, 1)

    def on_mouse_press(self, x, y, button, modifiers):
        # if master.player.shoot(mouse_position[0], mouse_position[1]): # noqa
        #     ret = calc_vel_xy(
        #         master.player.sprite.x, master.player.sprite.y,
        #         mouse_position[0], mouse_position[1], master.player.gun.base['recoil']
        #     ) # noqa
        #     master.player.sprite.x += ret[0]
        # master.player.sprite.y += ret[1]
        Buildmenu.on_mouse_press(x, y, 0)
        HotBar.update(x, y, 0)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        master.player_controller.rotate(x, y)

    def on_key_press(self, ts):
        pass

    def swap(self):
        states.swap('build')

    def update(self, ts):
        if key_handler[key.P]:
            self.Pause = 1
        else:
            if self.Pause == 1:
                self.Pause = 0
                states.swap('pause')
                master.reset()
                reset_imp()

        if key_handler[key.N]:
            self.Menu = 1
        else:
            if self.Menu == 1:
                self.Menu = 0
                Buildmenu.change_flag()

        if key_handler[key.B]:
            self.Build = 1
        else:
            if self.Build == 1:
                self.Build = 0
                inventorymenu.change_flag()
                # self.swap()
        mx = 0
        my = 0
        if key_handler[key.H]:
            readjust_x = master.home.x - master.player.sprite.x
            readjust_y = master.home.y - master.player.sprite.y
            master.player.sprite.x = master.home.x
            master.player.sprite.y = master.home.y
            master.move_all(-readjust_x, -readjust_y)
        if key_handler[key.TAB]:
            master.player_controller.target_closest_enemy()
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
            # Character(master, enemy_soldier_base())
            master.player_controller.slot_one_fire()

        if key_handler[key._2]:
            master.player_controller.slot_two_fire()

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


class BuildState(MainState):
    def __init__(self):
        # for i in range(len(master.enemies)):
            # master.enemies.pop(0)
        self.Pause = 0
        self.Build = 0
        self.Menu = 0
        self.manager = Manager()

        # master.buildings.append(Placeable(load_image('brick.png', anchor=False), 400, 400, None, BuildingBatch)) # noqa

    def on_mouse_release(self, x, y, button, modifiers):
        Buildmenu.on_mouse_press(x, y, 1)
        HotBar.update(x, y, 1)

    def on_mouse_press(self, x, y, button, modifiers):
        master.player_controller.update_target()
        Buildmenu.on_mouse_press(x, y, 0)
        HotBar.update(x, y, 0)
        master.player.ability.auto_attack()

    def on_mouse_motion(self, x, y, dx, dy):
        master.player_controller.sprite.x = x
        master.player_controller.sprite.y = y
        master.player_controller.rotate(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        master.player_controller.sprite.x = x
        master.player_controller.sprite.y = y
        # x_dist = x - float(master.player.sprite.x)
        # y_dist = y - float(master.player.sprite.y)
        master.update_button_image(x, y, dx, dy)
        # deg = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90
        # if master.player.shoot(mouse_position[0], mouse_position[1]): # noqa
        #     ret = calc_vel_xy(
        #         master.player.sprite.x, master.player.sprite.y,
        #         mouse_position[0], mouse_position[1],
        #         master.player.gun.base['recoil']
        #     )
        #     master.player.sprite.x += ret[0]
        #     master.player.sprite.y += ret[1]

    def swap(self):
        states.swap('main')

    def test(self):
        pass


def update(ts):
    states.current.update(ts)


@window.event
def on_draw():
    states.current.on_draw()
    states.current.test()
    window.invalid = False


class StartState(object):

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.shrinking = False
        img = pyglet.image.load('images/title_2.png')
        img.anchor_x = 0
        img.anchor_y = img.height

        self.sprite = pyglet.sprite.Sprite(
            img, 0, window_height,
            batch=self.batch
        )
        self.flag = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def shrink(self):
        if self.sprite.scale < .01:
            self.flag = True
        self.sprite.scale -= .1

    def update(self, ts):
        if key_handler[key.ENTER] or key_handler[key.RETURN]:
            self.shrinking = True
        else:
            if self.flag:
                states.swap('build')
        if self.shrinking:
            self.shrink()
        window.invalid = False

    def test(self):
        pass

    def on_draw(self):
        window.clear()
        pyglet.gl.glClearColor(1, 1, 1, 1)  # gray back
        self.batch.draw()
        window.invalid = False


class StateManager(object):

    def __init__(self):
        self.current = StartState()
        self.past = None
        self.pause = PauseState()

    def swap(self, string):
        self.past = self.current
        if string == 'main':
            self.current = MainState()
        if string == 'pause':
            self.current = self.pause
        if string == 'build':
            self.current = BuildState()

    def swapback(self):
        temp = self.past
        self.past = self.current
        self.current = temp
states = StateManager()
pyglet.clock.schedule_interval(update, 1 / 60.0)

pyglet.app.run()
