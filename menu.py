from utility import * # noqa
from importer import * # noqa
from building_dict import * # noqa


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
    def __init__(self, sprite, manager, build_dict, identity):
        self.manager = manager
        self.identity = identity
        self.build_dict = build_dict
        self.trigger = 0
        self.sprite = sprite
        self.trigger = 0
        self.costs = []
        self.labels = []
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
        self.building_sprite = pyglet.sprite.Sprite(
            load_image(self.build_dict['icon']),
            self.sprite.x + self.sprite.width / 2,
            self.sprite.y + self.sprite.height / 2, batch=MenuBatch
        )
        self.setup()

    def setup(self):
        i = 0
        convert = {'fo': 'resource.png', 'po': 'power.png', 'en': 'engineering.png', 'sc': 'science.png', 'mo': 'money.png'}
        for key in self.build_dict['cost']:
            value = self.build_dict['cost'][key]
            if value != 0:
                image = load_image(convert[key])
                sprite = pyglet.sprite.Sprite(
                    image,
                    self.sprite.x + self.sprite.width + 10 + i * 40, self.sprite.y + self.sprite.height / 2, batch=MenuBatch
                )
                sprite.scale = .125
                self.costs.append(sprite)
                i += 1
                templabel = pyglet.text.Label(
                    str(value),
                    font_name='Times New Roman',
                    font_size=12,
                    color=(0, 0, 0, 255),
                    x=sprite.x + sprite.width + 3,
                    y=sprite.y,
                    anchor_x='center',
                    anchor_y='center',
                    batch=MenuBatch
                )
                self.labels.append(templabel)

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
        print self.identity
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
        self.flag = False
        self.setup()
        self.tier_select = pyglet.sprite.Sprite(
            load_image('tierselect.png', False),
            10000, 10000, batch=SelectBatch
        )
        self.resource_select = pyglet.sprite.Sprite(
            load_image('resourceselect.png', False),
            10000, 10000, batch=SelectBatch
        )
        self.resource_select.scale = .25
        self.tier_select.scale = .5

    def set_build_manager(self, manager):
        self.build_manager = manager

    def setup(self):
        i = 0
        for item in ['resource.png', 'power.png', 'engineering.png', 'science.png', 'money.png']:
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

    def delete_buildbuttons(self):
        for button in self.build_buttons:
            button.label.delete()
            for label in button.labels:
                label.delete()
        self.build_buttons = []

    def create_buildbuttons(self):
        self.delete_buildbuttons()
        buildlist = self.build_manager.getlist(self.selected[0], self.selected[1])
        # buildlist = ['farm', 'field', 'tractor', 'worker', 'fascist government']
        i = 0
        for key in buildlist:
            item = buildlist[key]
            sprite = pyglet.sprite.Sprite(
                load_image('drawing.png', False),
                self.sprite.x + 5, window_height - 200 - (i * 90), batch=MenuBatch
            )
            sprite.scale = .15
            self.build_buttons.append(BuildButton(sprite, self.build_manager, item, item['name'] + '(' + str(self.selected[1] + 1) + ')'))
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

    def update(self):
        if self.flag:
            MenuBackground.draw()
            MenuBatch.draw()
            SelectBatch.draw()

    def change_flag(self):
        if self.flag:
            self.flag = False
            self.delete_buildbuttons()
            self.selected = [-1, -1]
            self.tier_select.x = 2000
            self.resource_select.x = 2000
        else:
            self.flag = True


class BuildingManager(object):
    def __init__(self, library):
        self.library = library
        self.convert = ['fo', 'po', 'en', 'sc', 'mo']

    def lookup(self, key):
        return self.library[key]

    def getlist(self, key1, key2):
        return self.library[self.convert[key1]][str(key2 + 1)]

    def build(self, key):
        pass
