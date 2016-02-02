import pyglet # noqa

from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa


from menu import * # noqa
from hotbar import * # noqa
from inventory import * # noqa
from levelgenerator import * # noqa


# fuck this
def load_assets(hb, bm, bum, im, difficulty, amount):
    hb = HotBarManager(hotbar_sprite, master) # noqa
    hb.setup()
    bm = BuildingManager(building_menu) # noqa
    bum = MenuManager(1200, 0, menu_back) # noqa
    bum.set_build_manager(buildmanager)
    im = Inventory(master) # noqa
    return hb, bm, bum, im


class InterfaceManager(object):
    def __init__(self):
        self.hotbar = None
        self.building_manager = None
        self. menu_manager = None
        self.inventory = None
