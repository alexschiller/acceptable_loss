from utility import * # noqa
from importer import * # noqa
from button import Button, Manager
hotbar_sprite = pyglet.sprite.Sprite(
    hotbarback,
    window_width / 2 - hotbarback.width / 2, 0, batch=HotbarBatch
)


def foo():
    pass


class HotBarManager(Manager):

    def __init__(self, sprite, master):
        self.sprite = sprite
        self.master = master
        self.buttons = []

    def setup(self):
        brick = load_image('hbutton1.png', False)
        image2 = load_image('hbutton2.png', False)
        # for i in range(9):
        #     tempbutton = Button(
        #         brick, image2, image2, self.sprite.x + i * (5 + brick.width),
        #         self.sprite.y + 5, self.master.player.slot_one_fire(), HotbarButtonBatch, str(i + 1)
        #     )
        #     self.buttons.append(tempbutton)

HotBar = HotBarManager(hotbar_sprite, master)
HotBar.setup()
