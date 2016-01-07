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

window_height_half = window_height / 2
window_width_half = window_width / 2

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

    def update(self):
        try:
            self.player.update()
        except:
            pass

        for e in self.enemies:
            try:
                e.update()
            except:
                pass
        for f in self.friends:
            try:
                f.update()
            except:
                pass
        for g in self.guns:
            try:
                g.update()
            except:
                pass
        try:
            self.spriteeffect.update()
        except:
            pass
        try:
            for b in self.buildings:
                b.update()
        except:
            pass
        self.update_camera()

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

        camera_x = float((window_width_half - self.player.sprite.x) / window_width_half) # noqa
        camera_y = float((window_height_half - self.player.sprite.y) / window_height_half) # noqa
        mx = camera_x * 5
        my = camera_y * 5
        for o in self.objects:
            o.sprite.x += mx
            o.sprite.y += my

        self.player.sprite.x += mx
        self.player.sprite.y += my

        for e in self.enemies:
            e.sprite.x += mx
            e.sprite.y += my
        for gun in self.guns:
            for b in gun.bullets:
                b.sprite.x += mx
                b.sprite.y += my

    def move_player(self, mx, my):
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


# Manually Built Static Sprites
green_sprite = pyglet.image.SolidColorImagePattern(color=(0, 255, 0, 150))
green_bar = pyglet.image.create(200, 10, green_sprite)

blue_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 255, 150))
blue_bar = pyglet.image.create(200, 10, blue_sprite)

red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
red_bar = pyglet.image.create(200, 10, red_sprite)

# Image loader function and dict
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
