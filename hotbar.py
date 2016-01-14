from utility import * # noqa
from importer import * # noqa
from button import Button
hotbar_sprite = pyglet.sprite.Sprite(
    hotbarback,
    window_width / 2 - hotbarback.width / 2, 0, batch=HotbarBatch
)


class HotBarManager(object):

    def __init__(self, sprite, master):
        self.sprite = sprite
        self.master = master
        self.buttons = []

    # def setup(self):
    #     for i in range(len(self.master.player.guns)):
    #         tempbutton = Button(
    #             button, buttonhover, buttondown, self.sprite.x,
    #             self.y, foo, HotbarButtonBatch, label
    #         )
    #         self.buttons.append(tempbutton)

HotBar = HotBarManager(hotbar_sprite, master)
