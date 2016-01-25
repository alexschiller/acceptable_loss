from utility import * # noqa
from importer import * # noqa
from button import Button, Manager # noqa

gem_icons = {}
gem_borders = []

for item in ['wood_border.png', 'bronze_border.png', 'silver_border.png', 'gold_border.png', 'obsidian_border.png', 'platinum_border.png']:
    gem_borders.append(load_image(item, False))

for item in ['sapphire', 'topaz', 'emerald', 'ruby', 'diamond']:
    gem_icons[item] = load_image(item + '.png', False)


class Item(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        pass

    def display(self):
        pass


class Gem(Item):
    def __init__(self, dictionary):
        self.dictionary = dictionary


class Inventory(object):
    def __init__(self, master):
        self.flag = False
        self.master = master
        self.gems = []
        self.borders = []
        self.sprite = pyglet.sprite.Sprite(
            load_image('inventory.png', False),
            950, 20, batch=InventoryBatch
        )

    def update_inventory(self):
        self.gems = []
        self.borders = []
        i = 0
        for item in self.master.player.inventory:
            if i > 49:
                break
            # 44 x 50
            x = self.sprite.x + 8 + (i % 7) * 55
            y = self.sprite.y + 5 + (i / 7) * 55
            border = pyglet.sprite.Sprite(
                gem_borders[item['rarity']],
                x, y, batch=ItemBorderBatch
            )
            gem = pyglet.sprite.Sprite(
                gem_icons[item['color']],
                x, y, batch=ItemBatch
            )
            self.gems.append(gem)
            self.borders.append(border)
            i += 1

    def update(self):
        if self.flag:
            self.update_inventory()
            InventoryBatch.draw()
            ItemBatch.draw()
            ItemBorderBatch.draw()

    def change_flag(self):
        self.flag = not self.flag

inventorymenu = Inventory(master)
