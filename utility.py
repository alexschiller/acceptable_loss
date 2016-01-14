# import random
import math # noqa
import pyglet
# import random
# import itertools
from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa
from collide import * # noqa
# Window sizes
window_height = 800
window_width = 1400

window_height_half = float(window_height / 2)
window_width_half = float(window_width / 2)

frame_width = 50


class Master(object):
    def __init__(self):
        self.player = None
        self.enemies = []
        self.friends = []
        self.guns = []
        self.objects = []
        self.spriteeffect = None
        self.buildings = []

        self.resources = None
        self.radar = None
        self.home = None
        self.threat = None
        self.loot = None

    def update(self):

        for e in self.enemies:
            e.update()

        for f in self.friends:
            f.update()

        for g in self.guns:
            g.update()

        for b in self.buildings:
            b.update()

        self.player.update()
        self.spriteeffect.update()
        self.resources.update()
        self.update_camera()
        self.threat.update()
        self.radar.update()
        self.pip.update()
        self.loot.update()

    def register_guns(self, guns):
        for gun in guns:
            self.guns.append(gun)

    def update_button(self, x, y, mode):
        for button in self.buildings:
            button.on_mouse_press(x, y, mode)

    def update_button_image(self, x, y, dx, dy):
        for button in self.buildings:
            button.on_mouse_motion(x, y, dx, dy)

    def update_camera(self):

        camera_x = (window_width_half - self.player.sprite.x) / window_width_half # noqa
        camera_y = (window_height_half - self.player.sprite.y) / window_height_half # noqa
        mx = 0
        my = 0
        if abs(camera_x) > .2:
            mx = camera_x * 5
        if abs(camera_y) > .2:
            my = camera_y * 5

        self.move_all(mx, my)

    def move_all(self, mx, my):
        for o in self.objects:
            o.sprite.x += mx
            o.sprite.y += my

        self.player.sprite.x += mx
        self.player.sprite.y += my
        self.home.x += mx
        self.home.y += my
        for p in self.loot.current_loot:
            p.sprite.x += mx
            p.sprite.y += my

        for c in self.loot.moving_loot:
            c.sprite.x += mx
            c.sprite.y += my

        for e in self.enemies:
            e.sprite.x += mx
            e.sprite.y += my
        for gun in self.guns:
            for b in gun.bullets:
                b.sprite.x += mx
                b.sprite.y += my
        for f in self.friends:
            f.sprite.x += mx
            f.sprite.y += my

    def move_player(self, mx, my):
        if mx and my:
            mx = mx / 1.41
            my = my / 1.41
        self.player.sprite.x += mx
        self.player.sprite.y += my

master = Master()

# Batches
LabelBatch = pyglet.graphics.Batch()
BarBatch = pyglet.graphics.Batch()
gfx_batch = pyglet.graphics.Batch()
BulletBatch = pyglet.graphics.Batch()
EffectsBatch = pyglet.graphics.Batch()
ButtonBatch = pyglet.graphics.Batch()
BuildingBatch = pyglet.graphics.Batch()
MenuBatch = pyglet.graphics.Batch()
MenuBackground = pyglet.graphics.Batch()
SelectBatch = pyglet.graphics.Batch()
HotbarBatch = pyglet.graphics.Batch()
HotbarButtonBatch= pyglet.graphics.Batch()

# Manually Built Static Sprites
green_sprite = pyglet.image.SolidColorImagePattern(color=(0, 255, 0, 150))
green_bar = pyglet.image.create(200, 10, green_sprite)

blue_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 255, 150))
blue_bar = pyglet.image.create(200, 10, blue_sprite)

red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
red_bar = pyglet.image.create(200, 10, red_sprite)

menu_back = pyglet.image.create(200, window_height, pyglet.image.SolidColorImagePattern(color=(238, 232, 170, 150))) # noqa
# Image loader function and dict
hotbarback = pyglet.image.create(455, 50, pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 150))) # noqa

image_dict = {}


def load_image(image, anchor=True):
    try:
        return image_dict(image)
    except:
        img = pyglet.image.load('images/' + image)
        if anchor:
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
        image_dict[image] = img
        return img


def load_sound(file_name):
    if file_name:
        return pyglet.media.load('sounds/' + file_name, streaming=False)
    return False


def play_sound(sound_file):
    if sound_file:
        sound = pyglet.media.Player()
        sound.queue(sound_file)
       # sound.play() # noqa


# todo move elsewhere
button = load_image('button.png', False)
buttonhover = load_image('buttonhover.png', False)
buttondown = load_image('buttondown.png', False)


def calc_vel_xy(tar_x, tar_y, start_x, start_y, velocity):
    dif_y = tar_y - start_y
    dif_x = tar_x - start_x
    try:
        dir_y = dif_y / abs(dif_y)
    except:
        dir_y = 1
    try:
        dir_x = dif_x / abs(dif_x)
    except:
        dir_x = 1
    try:
        perc = float(abs(dif_y)) / (abs(dif_y) + abs(dif_x))
    except:
        perc = .1
    vel_y = perc * velocity * dir_y
    vel_x = (velocity - abs(vel_y)) * dir_x
    return (vel_x, vel_y)

resource_base = {
    'food': 0,
    'eng': 0,
    'sci': 0,
    'pow': 0,
    'mon': 0,
    'red': 0,
    'orange': 0,
    'yellow': 0,
    'sap': 0,
    'green': 0,
    'brown': 0,
    'grey': 0,
    'dgreen': 0,
    'teal': 0,
    'blue': 0,
    'dblue': 0,
    'purple': 0
}
