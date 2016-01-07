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

        self.threat_time = 0
        self.home = None
        self.threat = 0

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
        self.threat_timer()

    def register_guns(self, guns):
        for gun in guns:
            self.guns.append(gun)

    def threat_timer(self):
        self.threat_time += 1
        if self.threat_time >= 360:
            self.update_threat()
            self.threat_time = 0

    def calculate_threat(self):
        dist = math.hypot(self.player.sprite.x - self.home.x, self.player.sprite.y - self.home.y) # noqa
        return dist / 1000.0 * 1  # object threat?

    def update_threat(self):
        self.threat += self.calculate_threat()
        print self.threat

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
        for o in self.objects:
            o.sprite.x += mx
            o.sprite.y += my

        self.player.sprite.x += mx
        self.player.sprite.y += my
        self.home.x += mx
        self.home.y += my

        for e in self.enemies:
            e.sprite.x += mx
            e.sprite.y += my
        for gun in self.guns:
            for b in gun.bullets:
                b.sprite.x += mx
                b.sprite.y += my

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
