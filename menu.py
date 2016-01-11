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
        self.label = pyglet.text.Label(
            identity,
            font_name='Times New Roman',
            font_size=16,
            color=(0, 0, 0, 255),
            x=self.sprite.x + self.sprite.width * 2,
            y=self.sprite.y + self.sprite.height + 10,
            anchor_x='center',
            anchor_y='center',
            batch=MenuBatch
        )

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
        print identity
        # self.manager.alert(self.identity)


class MenuManager(object):
    def __init__(self, x, y, menusprite):
        self.selected = [-1, -1]
        self.sprite = pyglet.sprite.Sprite(
            menusprite,
            x, y, batch=MenuBackground
        )
        self.resource_buttons = []
        self.tier_buttons = []
        self.build_buttons = []
        self.build_manager = None
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

    def set_build_manager(self, manager):
        self.build_manager = manager

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

    def create_buildbuttons(self):
        for button in self.build_buttons:
            button.label.delete()
        self.build_buttons = []
        # buildlist = self.build_manager.getlist(self.selected[0], self.selected[1])
        buildlist = ['farm', 'field', 'tractor', 'worker', 'fascist government']
        i = 0
        for item in buildlist:
            sprite = pyglet.sprite.Sprite(
                load_image('drawing.png', False),
                self.sprite.x + 5, window_height - 200 - (i * 90), batch=MenuBatch
            )
            sprite.scale = .15
            self.build_buttons.append(BuildButton(sprite, self.build_manager, item + '(' + str(self.selected[1] + 1) + ')'))
            i += 1

    def alert(self, identity):
        if identity < 10:
            self.selected[0] = identity
            self.resource_select.x = self.resource_buttons[identity].sprite.x
            self.resource_select.y = self.resource_buttons[identity].sprite.y

        else:
            self.selected[1] = identity - 10
            self.tier_select.x = self.tier_buttons[identity - 10].sprite.x
            self.tier_select.y = self.tier_buttons[identity - 10].sprite.y

        if self.selected[0] > -1 and self.selected[1] > -1:
            self.create_buildbuttons()

    def on_mouse_press(self, x, y, mode):
        for button in self.resource_buttons:
            button.on_mouse_press(x, y, mode)

        for button in self.tier_buttons:
            button.on_mouse_press(x, y, mode)

        for button in self.build_buttons:
            button.on_mouse_press(x, y, mode)


class BuildingManager(object):
    def __init__(self, library):
        self.library = library

    def lookup(self, key):
        return self.library[key]

    def getlist(self, key1, key2):
        return library[key1][key2]

    def build(self, key):
        pass

buildmanager = BuildingManager([])
Buildmenu = MenuManager(1200, 0, menu_back)
Buildmenu.set_build_manager(buildmanager)
