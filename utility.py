# import random
import math # noqa
import pyglet
# import random
# import itertools
from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa
from collide import * # noqa
from gem import Gem
import cProfile
import pstats # noqa
import StringIO # noqa

# Window sizes
window_height = 800
window_width = 1400

window_height_half = float(window_height / 2)
window_width_half = float(window_width / 2)

frame_width = 50
TerrainBatch = pyglet.graphics.Batch()
PortalBatch = pyglet.graphics.Batch()


class Master(object):
    def __init__(self):
        self.player_controller = None
        self.player = None
        self.gem = None
        self.people = {'red': [], 'blue': []}
        self.spriteeffect = None
        self.buildings = []
        self.pr = cProfile.Profile()
        self.pr.enable()

        self.resources = None
        self.radar = None
        self.home = None
        self.threat = None
        self.loot = None

    def update(self):

        self.room_manager.update()
        for p in self.people['blue']:
            p.update()

        for p in self.people['red']:
            p.update()

        for b in self.buildings:
            b.update()

        # self.player.update()
        self.spriteeffect.update()
        # self.resources.update()
        self.update_camera()
        # self.threat.update()
        # self.radar.update()
        self.loot.update()

    def update_button(self, x, y, mode):
        for button in self.buildings:
            button.on_mouse_press(x, y, mode)

    def update_button_image(self, x, y, dx, dy):
        for button in self.buildings:
            button.on_mouse_motion(x, y, dx, dy)

    def update_camera(self):

        mouse_camera_x = (window_width_half - self.player.controller.sprite.x) / window_width_half # noqa
        mouse_camera_y = (window_height_half - self.player.controller.sprite.y) / window_height_half # noqa

        player_camera_x = (window_width_half - self.player.sprite.x) / window_width_half # noqa
        player_camera_y = (window_height_half - self.player.sprite.y) / window_height_half # noqa
        mx = 0
        my = 0

        if abs(player_camera_x) > .8:
            mx = player_camera_x * 10
        elif abs(mouse_camera_x) > .5:
            mx = mouse_camera_x * 10

        if abs(player_camera_y) > .8:
            my = player_camera_y * 10
        elif abs(mouse_camera_y) > .5:
            my = mouse_camera_y * 10
        self.move_all(mx, my)

    def reset(self):

        self.room_manager.setup(3)
        self.room_manager.parent.create_sprites(0, 0, TerrainBatch, self.player)
        self.room_manager.add_enemies()
        self.room_manager.create_portal()

        self.home = pyglet.sprite.Sprite(
            load_image('home.png'),
            window_width_half, window_height_half, batch=gfx_batch
        )

    def move_all(self, mx, my):

        # self.player.sprite.x += mx
        # self.player.sprite.y += my
        self.home.x += mx
        self.home.y += my
        try:
            self.room_manager.move_all(mx, my)
        except:
            pass

        for p in self.loot.current_loot:
            p.sprite.x += mx
            p.sprite.y += my

        for c in self.loot.moving_loot:
            c.sprite.x += mx
            c.sprite.y += my

        for p in self.people['red']:
            p.sprite.x += mx
            p.sprite.y += my
            for a in p.ability.thrown:
                a.sprite.x += mx
                a.sprite.y += my

        for p in self.people['blue']:
            p.sprite.x += mx
            p.sprite.y += my
            for a in p.ability.thrown:
                a.sprite.x += mx
                a.sprite.y += my

master = Master()
master.gem = Gem()
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
HotbarButtonBatch = pyglet.graphics.Batch()
InventoryBatch = pyglet.graphics.Batch()
ItemBatch = pyglet.graphics.Batch()
ItemBorderBatch = pyglet.graphics.Batch()

# Manually Built Static Sprites
green_sprite = pyglet.image.SolidColorImagePattern(color=(0, 255, 0, 150))
green_bar = pyglet.image.create(200, 10, green_sprite)

blue_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 255, 150))
blue_bar = pyglet.image.create(200, 10, blue_sprite)


orange_sprite = pyglet.image.SolidColorImagePattern(color=(180, 107, 50, 255))
camo_sprite = pyglet.image.SolidColorImagePattern(color=(100, 107, 50, 255))


white_sprite = pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 150))
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
