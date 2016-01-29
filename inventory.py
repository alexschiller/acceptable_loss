from utility import * # noqa
from importer import * # noqa
from button import Button, Manager # noqa
gem_icons = {}
gem_borders = []

for item in ['wood_border.png', 'bronze_border.png', 'silver_border.png', 'gold_border.png', 'obsidian_border.png', 'platinum_border.png']:
    gem_borders.append(load_image(item, False))

for item in ['sapphire', 'topaz', 'emerald', 'ruby', 'diamond']:
    gem_icons[item] = load_image(item + '.png', False)


class InventoryButton(object):
    def __init__(self, x, y, ide, manager):
        self.manager = manager
        self.trigger = 0
        self.x = x
        self.y = y
        self.id = ide

    def on_mouse_press(self, x, y, mode):

        if (self.x < x and
                x < self.x + 50 and
                self.y < y and
                y < self.y + 50):
            if mode == 1 and self.trigger == 1:
                self.trigger = 0
                self.press_action()
            if mode == 0:
                self.trigger = 1

    def press_action(self):
        # print "Hello from button" + str(self.id)
        self.manager.alert(self.id)


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
        self.buttons = []
        self.create_buttons()
        self.label = None
        self.tooltip_back = pyglet.image.create(200, 200, pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 100)))
        self.tooltip_sprite = None

    def create_buttons(self):
        for i in range(49):
            x = self.sprite.x + 8 + (i % 7) * 55
            y = self.sprite.y + 5 + (i / 7) * 55
            self.buttons.append(InventoryButton(x, y, i, self))

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

    def on_mouse_press(self, x, y, mode):
        for button in self.buttons:
            button.on_mouse_press(x, y, mode)

    def change_flag(self):
        self.flag = not self.flag
        if not self.flag:
            try:
                self.tooltip_sprite.delete()

                self.label.delete()
            except:
                pass

    def alert(self, i):
        try:
            self.label.delete()
        except:
            pass
        try:
            gem = self.master.player.inventory[i] # noqa
            print gem
            self.tooltip_sprite = pyglet.sprite.Sprite(
                self.tooltip_back,
                self.sprite.x + 15, self.sprite.y + self.sprite.height - 215, batch=ItemBorderBatch
            )
            labelstr = ""
            for key in gem:
                if key == 'stats':
                    for stat in gem[key]:
                        labelstr += stat + ": " + str(gem[key][stat]) + "\n"
                else:
                    labelstr += key + ": " + str(gem[key]) + "\n"
            self.label = pyglet.text.Label(
                labelstr,
                font_name='Times New Roman',
                font_size=12,
                x=self.tooltip_sprite.x,
                y=self.tooltip_sprite.y + self.tooltip_sprite.height,
                multiline=True,
                width=200,
                anchor_x='left',
                anchor_y='top',
                batch=ItemBatch
            )
        except:
            pass

inventorymenu = Inventory(master)
