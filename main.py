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

window = pyglet.window.Window(window_width, window_height)
states = []
spriteeffect = SpriteEffect()
player = Player(spriteeffect)

enemy = []
pg = [shotgun]
pistol = Gun(enemy, base=exgun,)
player_gun = Gun(enemy, base=random.choice(pg), pistol=pistol)
cannon_gun = Gun(enemy, base=shotgun)
enemy_gun = Gun(player, base=slimegun)

guns = [player_gun, cannon_gun, enemy_gun, pistol]
for i in range(4):
    enemy.append(Enemy(player, enemy, spriteeffect, enemy_gun))

grenade = Grenade()

friends = [
    Healer(player, enemy, cannon_gun, spriteeffect),
    # Cannon(player, enemy, gun, spriteeffect)
]
key_handler = key.KeyStateHandler()

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
        @window.event
        def on_key_release(symbol, modifiers):
            # print symbol
            if symbol == key.DELETE:
                self.button.delete()
            elif symbol == key.ENTER or symbol == key.RETURN:
                states.pop(0)
            else:
                self.button.add_text(symbol)


class PauseState():
    def __init__(self):
        self.Pause = 0
        self.manager = Manager()
        buttons = ['hi', 'button', 'chain', 'is', 'a', 'go']
        self.y = 660
        for label in buttons:
            self.manager.add_button(DraggableButton(button, buttonhover, buttondown, 650,
                self.y, foo, ButtonBatch, label))
            self.y -= 110

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.manager.update_image(x, y, dx, dy)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        # thing = TextState(self.manager.buttons[0])
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
        if player_gun.fire(player.sprite.x, player.sprite.y, mouse_position[0], mouse_position[1]): # noqa
            ret = calc_vel_xy(player.sprite.x, player.sprite.y, mouse_position[0], mouse_position[1], player_gun.base['recoil']) # noqa
            player.sprite.x += ret[0]
            player.sprite.y += ret[1]

    def on_mouse_motion(self, x, y, dx, dy):
        x_dist = x - float(player.sprite.x)
        y_dist = y - float(player.sprite.y)

        deg = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

        player.sprite.rotation = deg
        # print dx, dy

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        x_dist = x - float(player.sprite.x)
        y_dist = y - float(player.sprite.y)

        deg = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90
        if player_gun.fire(player.sprite.x, player.sprite.y, mouse_position[0], mouse_position[1]): # noqa
            ret = calc_vel_xy(player.sprite.x, player.sprite.y, mouse_position[0], mouse_position[1], player_gun.base['recoil']) # noqa
            player.sprite.x += ret[0]
            player.sprite.y += ret[1]
        player.sprite.rotation = deg

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
        player.move(mx, my)

        if key_handler[key.Q]:
            grenade.throw(
                player.sprite.x,
                player.sprite.y, mouse_position[0],
                mouse_position[1]
            )

        if key_handler[key.F] and player.energy >= 100:
            player.energy -= 100
            spriteeffect.teleport(player.sprite.x, player.sprite.y)
            player.sprite.x = mouse_position[0]
            player.sprite.y = mouse_position[1]
            spriteeffect.teleport(player.sprite.x, player.sprite.y)

        # Run Updates
        for g in guns:
            g.update()
        grenade.update()
        spriteeffect.update()
        player.update()
        for f in friends:
            f.update()
        for e in enemy:
            e.update()

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
    player.sprite.draw()
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
