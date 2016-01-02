# import random
import math # noqa
import pyglet
# import random
from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa
from collide import * # noqa
from character import * # noqa
from utility import * # noqa
from gun import * # noqa
from button import Manager, Button,TextBox, DraggableButton, foo # noqa
from energy import * # noqa


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
states = []
window = pyglet.window.Window(window_width, window_height)
master.spriteeffect = SpriteEffect(master)

master.player = Player(master)

# todo: Gun 'hits' (e.g., master.enemies, master.player) needs refactor to two subclasses,
# one that hits friends, one that hits enemies
gun_dict = {'pistol': Gun(master, hits='enemies', base=fire),
            'master.player_1': Gun(master,
                hits='enemies', base=red_laser),
            'master.player_2': Gun(master, hits='enemies', base=shotgun),
            'soldier_gun': Gun(master, hits='friends', base=missile),
            }

# player_guns = [gun_dict['master.player_1'], gun_dict['master.player_2'], gun_dict['master.player_3']] # noqa
player_guns = [gun_dict['master.player_2']]

master.player.load_guns(player_guns)
master.pistol = gun_dict['pistol']

# guns = [master.player, cannon_gun, enemy_gun, pistol, soldier_gun]
# for i in range(2):
    # enemy.append(Enemy(master, gun_dict['enemy_gun'])) # noqa

for i in range(5):
    master.enemies.append(Soldier(master, gun_dict['soldier_gun'])) # noqa

for i in range(50):
    master.objects.append(Box(master)) # noqa


master.friends = [
    # Healer(master, gun_dict['cannon_gun']), # noqa
    # Cannon(player, enemy, gun, spriteeffect)
]
for k in gun_dict.keys():
    master.guns.append(gun_dict[k])


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

    def on_draw(self):
        window.clear()
        pyglet.gl.glClearColor(0.75, 0.75, 0.75, 1)  # gray back
        master.player.sprite.draw()
        BulletBatch.draw()
        EffectsBatch.draw()
        BarBatch.draw()
        gfx_batch.draw()
        states[0].test()
        window.invalid = False


class MainState():
    def __init__(self):
        self.Pause = 0

    def on_draw(self):
        window.clear()
        pyglet.gl.glClearColor(0.75, 0.75, 0.75, 1)  # gray back
        master.player.sprite.draw()
        BulletBatch.draw()
        EffectsBatch.draw()
        BarBatch.draw()
        gfx_batch.draw()
        states[0].test()
        window.invalid = False

    def test(self):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if master.player.fire(mouse_position[0], mouse_position[1]): # noqa
            ret = calc_vel_xy(master.player.sprite.x, master.player.sprite.y, mouse_position[0], mouse_position[1], master.player.base['recoil']) # noqa
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
        if master.player.fire(mouse_position[0], mouse_position[1]): # noqa
            ret = calc_vel_xy(master.player.sprite.x, master.player.sprite.y, mouse_position[0], mouse_position[1], master.player.base['recoil']) # noqa
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

        # if key_handler[key.Q]:
        #     master.grenade.throw(
        #         master.player.sprite.x,
        #         master.player.sprite.y, mouse_position[0],
        #         mouse_position[1]
        # )
        if key_handler[key.E]:
            master.player.next_gun()

        if key_handler[key.F] and master.player.energy >= 100:
            # teleport(master, mouse_position)
            teleport(master, mouse_position)
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
    states[0].on_draw()
    states[0].test()
    window.invalid = False


class StartState(object):

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.shrinking = False
        # self.label = pyglet.text.Label(
        #     'Press Start',
        #     font_name='Times New Roman',
        #     font_size=32,
        #     x=window_width / 2 - 250,
        #     y=window_height / 2,
        #     anchor_x='center',
        #     anchor_y='center',
        #     batch=self.batch
        # )

        img = pyglet.image.load('images/title_2.png')
        img.anchor_x = 0
        img.anchor_y = img.height

        self.sprite = pyglet.sprite.Sprite(img,
            0, window_height, batch=self.batch)
        # self.label = pyglet.text.Label(
        #     'ACCEPTABLE LOSS',
        #     font_name='Times New Roman',
        #     font_size=96,
        #     x=window_width / 2,
        #     y=window_height / 2 + 200,
        #     anchor_x='center',
        #     anchor_y='center',
        #     batch=self.batch
        # )

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
        self.sprite.scale -= .01

    def update(self, ts):
        if key_handler[key.ENTER] or key_handler[key.RETURN]:
            self.shrinking = True
        else:
            if self.flag:
                states.pop(0)
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


states.append(StartState())
states.append(MainState())  # add state to run time
states.append(PauseState())
pyglet.clock.schedule_interval(update, 1 / 60.0)

pyglet.app.run()
