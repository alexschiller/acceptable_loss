from utility import * # noqa
from importer import * # noqa


class MenuButton(object):
    def __init__(self, sprite, manager, identity):
        self.manager = manager
        self.identity = identity
        self.trigger = 0
        self.sprite = sprite
        self.trigger = 0

    def on_mouse_press(self, x, y, mode):

        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height):
            if mode == 1 and self.trigger == 1:
                self.trigger = 0
                self.press_action()
            if mode == 0:
                self.trigger = 1

    def press_action(self):
        self.manager.alert(self.identity)


class BuildButton(MenuButton):
    def __init__(self, sprite, manager, identity):
        self.manager = manager
        self.identity = identity
        self.trigger = 0
        self.sprite = sprite
        self.trigger = 0

    def on_mouse_press(self, x, y, mode):

        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height):
            if mode == 1 and self.trigger == 1:
                self.trigger = 0
                self.press_action()
            if mode == 0:
                self.trigger = 1

    def press_action(self):
        self.manager.alert(self.identity)


class MenuManager(object):
    def __init__(self, x, y, menusprite):
        self.selected = [0, 0]
        self.sprite = pyglet.sprite.Sprite(
            menusprite,
            x, y, batch=MenuBackground
        )
        self.resource_buttons = []
        self.tier_buttons = []
        self.setup()
        self.tier_select = pyglet.sprite.Sprite(
            load_image('tierselect.png', False),
            100, 100, batch=SelectBatch
        )
        self.resource_select = pyglet.sprite.Sprite(
            load_image('resourceselect.png', False),
            100, 100, batch=SelectBatch
        )
        self.resource_select.scale = .25
        self.tier_select.scale = .5

    def setup(self):
        i = 0
        for item in ['resource.png', 'engineering.png', 'power.png', 'science.png', 'money.png']:
            sprite = pyglet.sprite.Sprite(
                load_image(item, False),
                self.sprite.x + 5 + i * 40, window_height - 50, batch=MenuBatch
            )
            sprite.scale = .25
            self.resource_buttons.append(MenuButton(sprite, self, i))
            i += 1
        for i in range(5):
            sprite = pyglet.sprite.Sprite(
                load_image('tier' + str(i + 1) + '.png', False),
                self.sprite.x + 5 + i * 40, window_height - 90, batch=MenuBatch
            )
            sprite.scale = .5
            self.tier_buttons.append(MenuButton(sprite, self, i + 10))

    def alert(self, identity):
        if identity < 10:
            self.selected[0] = identity
            self.resource_select.x = self.resource_buttons[identity].sprite.x
            self.resource_select.y = self.resource_buttons[identity].sprite.y

        else:
            self.selected[1] = identity - 10
            self.tier_select.x = self.tier_buttons[identity - 10].sprite.x
            self.tier_select.y = self.tier_buttons[identity - 10].sprite.y

    def on_mouse_press(self, x, y, mode):
        for button in self.resource_buttons:
            button.on_mouse_press(x, y, mode)

        for button in self.tier_buttons:
            button.on_mouse_press(x, y, mode)


class BuildingManager(object):
    def __init__(self, library):
        self.library = library
        self.selection

    def lookup(self, key):
        return self.library[key]

    def build(self, key):
        pass

Buildmenu = MenuManager(1200, 0, menu_back)
