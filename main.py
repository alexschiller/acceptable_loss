# import random
import math # noqa
import pyglet
# import random
# import itertools
from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa
from collide import * # noqa
from character import * # noqa
from utility import * # noqa
from gun import * # noqa
from button import Manager, Button,TextBox, DraggableButton, foo # noqa


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


window = pyglet.window.Window(window_width, window_height)
states = []
master.spriteeffect = SpriteEffect(master)

master.player = Player(master)

# todo: Gun 'hits' (e.g., master.enemies, master.player) needs refactor to two subclasses,
# one that hits friends, one that hits enemies
gun_dict = {'pistol': Gun(master, master.enemies, base=exgun),
            'player_gun': Gun(master, master.enemies, base=red_laser),
            'cannon_gun': Gun(master, master.enemies, base=shotgun),
            'enemy_gun': Gun(master, master.player, base=slimegun),
            'soldier_gun': Gun(master, master.player, base=exgun),
            }
player_gun = gun_dict['player_gun']

# guns = [player_gun, cannon_gun, enemy_gun, pistol, soldier_gun]
# for i in range(2):
    # enemy.append(Enemy(master, gun_dict['enemy_gun'])) # noqa

for i in range(10):
    master.enemies.append(Soldier(master, gun_dict['soldier_gun'])) # noqa

master.grenade = Grenade(master)

master.friends = [
    Healer(master, gun_dict['cannon_gun']), # noqa
    # Cannon(player, enemy, gun, spriteeffect)
]
for k in gun_dict.keys():
    master.guns.append(gun_dict[k])

key_handler = ProtoKeyStateHandler()

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window.push_handlers(key_handler)

#  Align sprite to mouse


def jesustakethewheel():
        thing = states[0]
        states[0] = states[1]
        states[1] = thing

global mouse_position
mouse_position = [0, 0]


@window.event
def on_mouse_motion(x, y, dx, dy):
    states[0].on_mouse_motion(x, y, dx, dy)
    global mouse_position
    mouse_position = [x, y]


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    states[0].on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    global mouse_position
    mouse_position = [x, y]


@window.event
def on_mouse_release(x, y, button, modifiers):
    states[0].on_mouse_release(x, y, button, modifiers)


@window.event
def on_mouse_press(x, y, button, modifiers):
    states[0].on_mouse_press(x, y, button, modifiers)


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
                jesustakethewheel()
        window.invalid = False

    def test(self):
        ButtonBatch.draw()
        LabelBatch.draw()


class MainState():
    def __init__(self):
        self.Pause = 0

    def test(self):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if player_gun.fire(master.player.sprite.x, master.player.sprite.y, mouse_position[0], mouse_position[1]): # noqa
            ret = calc_vel_xy(master.player.sprite.x, master.player.sprite.y, mouse_position[0], mouse_position[1], player_gun.base['recoil']) # noqa
            master.player.sprite.x += ret[0]
            master.player.sprite.y += ret[1]

    def on_mouse_motion(self, x, y, dx, dy):
        x_dist = x - float(master.player.sprite.x)
        y_dist = y - float(master.player.sprite.y)

        deg = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

        master.player.sprite.rotation = deg
        # print dx, dy

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        x_dist = x - float(master.player.sprite.x)
        y_dist = y - float(master.player.sprite.y)

        deg = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90
        if player_gun.fire(master.player.sprite.x, master.player.sprite.y, mouse_position[0], mouse_position[1]): # noqa
            ret = calc_vel_xy(master.player.sprite.x, master.player.sprite.y, mouse_position[0], mouse_position[1], player_gun.base['recoil']) # noqa
            master.player.sprite.x += ret[0]
            master.player.sprite.y += ret[1]
        master.player.sprite.rotation = deg

    def on_key_press(self, ts):
        pass

    def update(self, ts):
        if key_handler[key.P]:
            self.Pause = 1
        else:
            if self.Pause == 1:
                self.Pause = 0
                jesustakethewheel()
        mx = 0
        my = 0
        if key_handler[key.D]:
            mx += 1
        if key_handler[key.A]:
            mx -= 1
        if key_handler[key.W]:
            my += 1
        if key_handler[key.S]:
            my -= 1
        master.player.move(mx, my)

        if key_handler[key.Q]:
            master.grenade.throw(
                master.player.sprite.x,
                master.player.sprite.y, mouse_position[0],
                mouse_position[1]
            )

        if key_handler[key.F] and master.player.energy >= 100:
            master.player.energy -= 100
            master.spriteeffect.teleport(master.player.sprite.x, master.player.sprite.y)
            master.player.sprite.x = mouse_position[0]
            master.player.sprite.y = mouse_position[1]
            master.spriteeffect.teleport(master.player.sprite.x, master.player.sprite.y)

        # Run Updates
        master.update()
        window.invalid = False


def update(ts):
    states[0].update(ts)

# @window.event
# def on_key_release(symbol, modifiers):
#     if symbol == pyglet.window.key.ESCAPE:
#         jesustakethewheel()
#         return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    window.clear()
    pyglet.gl.glClearColor(0.75, 0.75, 0.75, 1)  # gray back
    master.player.sprite.draw()
    BulletBatch.draw()
    EffectsBatch.draw()
    BarBatch.draw()
    gfx_batch.draw()
    states[0].test()
    window.invalid = False

states.append(MainState())  # add state to run time
states.append(PauseState())
pyglet.clock.schedule_interval(update, 1 / 60.0)

pyglet.app.run()
