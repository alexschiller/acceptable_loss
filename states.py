import pyglet  # noqa
from pyglet.gl import *  # noqa
from pyglet.window import key # noqa
from utility import * # noqa
from importer import * # noqa


def randotest():
    print "TEST COMPLETE BOITCH"

keycodes = [
    1, 2, 4, 8, 16, 32, 64, 128, 256, 2, 65288, 65289, 65290, 65291, 65293, 65293, 65299, 65300, 65301, 65307, 65360,
    65361, 65362, 65363, 65364, 65365, 65366, 65367, 65368, 65535, 65376, 65377, 65378, 65379, 65381, 65382, 65383, 65384,
    65385, 65386, 65387, 65406, 65406, 65362, 65363, 65364, 65361, 1, 2, 3, 4, 65366, 65365, 5, 6, 65288, 65535, 65407, 65408,
    65417, 65421, 65425, 65426, 65427, 65428, 65429, 65430, 65431, 65432, 65433, 65434, 65434, 65435, 65435, 65436, 65437,
    65438, 65439, 65469, 65450, 65451, 65452, 65453, 65454, 65455, 65456, 65457, 65458, 65459, 65460, 65461, 65462, 65463,
    65464, 65465, 65470, 65471, 65472, 65473, 65474, 65475, 65476, 65477, 65478, 65479, 65480, 65481, 65482, 65483, 65484,
    65485, 65505, 65506, 65507, 65508, 65509, 65511, 65512, 65513, 65514, 65515, 65516, 65517, 65518, 65488, 65489, 32, 33,
    34, 35, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
    58, 59, 60, 61, 62, 63, 64, 91, 92, 93, 94, 95, 96, 96, 97, 98, 99, 100, 101,
    52, 53, 54, 55, 56, 57, 65490, 65519,
    102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126
]


class KeyManager(object):
    def __init__(self):
        self.keys_held = []
        self.window = None
        self.release_states = {}
        self.hold_states = {}
        self.key_handler = None

    def register_handler(self, handler):
        self.key_handler = handler
        for symbol in keycodes:
            print symbol
            self.release_states[symbol] = {}
            self.hold_states[symbol] = {}
            for state in ['PauseState', 'GameState', 'MainMenuState', 'SelectState']:
                self.release_states[symbol][state] = 0
                self.hold_states[symbol][state] = 0

    def register_window(self, window):
        self.window = window

    def on_key_press(self, symbol, modifiers):
        if symbol not in self.keys_held:
            self.keys_held.append(symbol)

    def on_key_hold(self):
        for symbol in self.keys_held:
            if self.hold_states[symbol][str(self.window.state_manager.current)] is not 0:
                self.hold_states[symbol][str(self.window.state_manager.current)]()

    def on_key_release(self, symbol, modifiers):
        if self.release_states[symbol][str(self.window.state_manager.current)] is not 0:
            self.release_states[symbol][str(self.window.state_manager.current)]()
        if symbol in self.keys_held:
            self.keys_held.remove(symbol)

    def register_event_hold(self, state, symbol, func):
        self.hold_states[symbol][state] = func

    def register_event_release(self, state, symbol, func):
        self.release_states[symbol][state] = func


class ProtoKeyStateHandler(key.KeyStateHandler):

    def __init__(self):
        self[key.A] = False
        self.list = []
        self.active = False
        self.manager = None

    def on_key_press(self, symbol, modifiers):
        self[symbol] = True
        self.manager.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self[symbol] = False
        self.manager.on_key_release(symbol, modifiers)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def clear_state(self):
        self.list = []

    def register(self, manager):
        self.manager = manager

    def get_next_item(self):
        if len(self.list) > 0:
            return self.list.pop(0)
        else:
            return False

key_handler = ProtoKeyStateHandler()


class StateObject(object):
    def __init__(self, manager):
        self.manager = manager
        self.change = 0
        self.batches = []

    def register_batch(self, batch):
        self.batches.append(batch)

    def on_key_press(self, symbol, modkey):
        pass

    def on_key_release(self, symbol, modkey):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def update(self, ts):
        pass

    def __str__(self): # noqa
        return "StateObject"


class PauseState(StateObject):
    def __init__(self, manager):
        super(PauseState, self).__init__(self)

        self.Pause = 0
        self.manager = Manager()
        buttons = ['hi', 'button', 'chain', 'is', 'a', 'go']
        self.y = 660
        for label in buttons:
            self.manager.add_button(
                DraggableButton(button, buttonhover, buttondown, 650,
                self.y, foo, ButtonBatch, label) # noqa
            )
            self.y -= 110

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.manager.update_image(x, y, dx, dy)

    def on_mouse_motion(self, x, y, dx, dy):
        self.manager.update_image(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        self.manager.update(x, y, 1)

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.update(x, y, 0)

    def update(self, ts):
        if key_handler[key.P]:
            self.Pause = 1
        else:
            if self.Pause == 1:
                self.Pause = 0
                self.manager.swapback()

    def batch_setup(self):
        self.batches = [
            TerrainBatch, PortalBatch, BuildingBatch, BulletBatch,
            gfx_batch, EffectsBatch, BarBatch, ButtonBatch, LabelBatch,
        ]
    def __str__(self): # noqa
        return "PauseState"


class GameState(StateObject):
    def __init__(self, manager):
        super(GameState, self).__init__(manager)

        self.Pause = 0
        self.Build = 0
        self.Menu = 0
        self.last_time = 0
        self.batch_setup()
        self.mouse_two_down = False

    def __str__(self): # noqa
        return "GameState"

    def batch_setup(self):
        self.batches = [
            TerrainBatch, PortalBatch, master.player.sprite, BulletBatch, EffectsBatch, BarBatch,
            gfx_batch, BuildingBatch, HotbarBatch, HotbarButtonBatch,
        ]

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 4:
            self.mouse_two_down = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            master.player_controller.move_to(x, y, .05)
        if button == 4:
            self.mouse_two_down = True

    def on_mouse_motion(self, x, y, dx, dy):
        master.player_controller.sprite.x = x
        master.player_controller.sprite.y = y
        master.player_controller.rotate(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        master.player_controller.sprite.x = x
        master.player_controller.sprite.y = y
        # master.update_button_image(x, y, dx, dy)

    def update(self, ts):
        # mx = 0
        # my = 0
        if self.mouse_two_down:
            master.player_controller.slot_mouse_two_fire()
        if key_handler[key.P]:
            self.Pause = 1
        else:
            if self.Pause == 1:
                self.Pause = 0
                self.manager.swap('pause')

        if key_handler[key.N]:
            self.Menu = 1
        else:
            if self.Menu == 1:
                self.Menu = 0
                self.manager.assets.bum.change_flag()

        if key_handler[key.B]:
            self.Build = 1
        else:
            if self.Build == 1:
                self.Build = 0
                self.manager.assets.im.change_flag()
                # self.swap()
        # mx = 0
        # my = 0
        if key_handler[key.X]:
            if collide(master.player.collision, master.dungeon.room.portal.collision):
                self.manager.swap_special('select')

        if key_handler[key.H]:
            readjust_x = master.home.x - master.player.sprite.x
            readjust_y = master.home.y - master.player.sprite.y
            master.player.sprite.x = master.home.x
            master.player.sprite.y = master.home.y
            master.move_all(-readjust_x, -readjust_y)
        if key_handler[key.TAB]:
            pass
            master.pr.disable()
            s = StringIO.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(master.pr, stream=s).sort_stats(sortby) # noqa

            f = open('output.txt', 'w')
            f.write(s.getvalue())
            # print s.getvalue()
            # master.player_controller.target_closest_enemy()
        # if key_handler[key.D]:
        #     mx += 1
        # if key_handler[key.A]:
        #     mx -= 1
        # if key_handler[key.W]:
        #     my += 1
        # if key_handler[key.S]:
        #     my -= 1
        # master.player_controller.move(mx, my)

        if key_handler[key._1]:
            master.player_controller.slot_one_fire()

        if key_handler[key._2]:
            master.player_controller.slot_two_fire()

        if key_handler[key._3]:
            master.player_controller.slot_three_fire()

        if key_handler[key._4]:
            master.player_controller.slot_four_fire()

        if key_handler[key.Q]:
            master.player_controller.slot_q_fire()

        if key_handler[key.E]:
            master.player_controller.slot_e_fire()

        if key_handler[key.SPACE]:
            master.player.jump()

        # master.player.move(mx, my)

        # if key_handler[key.Q]:
        #     master.grenade.throw(
        #         master.player.sprite.x,
        #         master.player.sprite.y, mouse_position[0],
        #         mouse_position[1]
        # )

        if key_handler[key.F] and master.player.energy >= 100:
            # teleport(master, mouse_position)
            teleport(master, self.manager.assets.mouse_position)
        # Run Updates
        master.update()


class MainMenuState(StateObject):
    def __init__(self, manager):
        super(MainMenuState, self).__init__(manager)

        self.batches = [pyglet.graphics.Batch()]  # this should order them properly?
        img = pyglet.image.load('images/title_2.png')
        img.anchor_x = 0
        img.anchor_y = img.height

        self.background = pyglet.sprite.Sprite(
            img, 0, window_height,
            batch=self.batches[0]
        )

    def on_key_press(self, symbol, modkey):
        self.manager.swap('select')

    def update(self, ts):
        if key_handler[key.ENTER] or key_handler[key.RETURN]:
            self.manager.swap('select')

    def __str__(self): # noqa
        return "MainMenuState"


class SelectState(StateObject):
    def __init__(self, manager, flag=False):
        super(SelectState, self).__init__(manager)
        master.reset(0)
        self.val = flag
        self.batch = pyglet.graphics.Batch()
        self.state_manager = manager
        self.manager = Manager()
        self.buttons = []
        self.locked_buttons = []
        self.disp_buttons = []
        self.difficulty = 0
        self.label_batch = pyglet.graphics.Batch()
        self.batches = [self.batch, self.label_batch]
        self.max_dif = 50
        self.dict = [
            "blank.png", "down_all_down.png",
            "down_all_up.png", "down_down.png",
            "down_more_down.png", "down_more_up.png",
            "down_up.png", "locked_down.png",
            "locked_up.png", "side_down.png",
            "side_up.png", "up.png", "up_all_down.png",
            "up_all_up.png", "up_more_down.png",
            "up_more_up.png", "up_up.png"
        ]
        self.image_dict = {}
        self.number_button_images = []
        self.make_images()
        self.setup()

    def __str__(self): # noqa
        return "SelectState"

    def make_images(self):
        for item in self.dict:
            self.image_dict[item] = load_image(item, False)
        for i in range(10):
            self.number_button_images.append(load_image('blank_' + str(i) + ".png", False))
        self.number_button_images.append(self.image_dict['blank.png'])

    def set_icons(self, x, y, z, flag):
        if flag == 0:
            self.disp_buttons[0].upsprite = self.number_button_images[x]
            self.disp_buttons[1].upsprite = self.number_button_images[y]
            self.disp_buttons[2].upsprite = self.number_button_images[z]
            for button in self.disp_buttons:
                button.sprite.image = button.upsprite
        else:
            self.locked_buttons[0].upsprite = self.number_button_images[x]
            self.locked_buttons[1].upsprite = self.number_button_images[y]
            self.locked_buttons[2].upsprite = self.number_button_images[z]
            for i in range(3):
                self.locked_buttons[i].sprite.image = self.locked_buttons[i].upsprite

    def update_icons(self):
        temp = str(self.difficulty)
        if self.difficulty < 10:
            self.set_icons(self.difficulty, 10, 10, 0)
        if self.difficulty > 9:
            self.set_icons(int(temp[1]), int(temp[0]), 10, 0)
        if self.difficulty > 99:
            self.set_icons(int(temp[2]), int(temp[1]), int(temp[0]), 0)

        temp = str(self.max_dif)
        if self.max_dif < 10:
            self.set_icons(self.max_dif, 10, 10, 1)
        if self.max_dif > 9:
            self.set_icons(int(temp[1]), int(temp[0]), 10, 1)
        if self.max_dif > 99:
            self.set_icons(int(temp[2]), int(temp[1]), int(temp[0]), 1)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.manager.update_image(x, y, dx, dy)

    def on_mouse_motion(self, x, y, dx, dy):
        self.manager.update_image(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        self.manager.update(x, y, 1)

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.update(x, y, 0)

    def update(self, ts):
        self.update_icons()

    def register_keys(self, manager):
        manager.register_event_release(str(self), key.A, randotest)

    def test(self):
        pass

    def increase_max_dif(self):
        self.max_dif += 1

    def increase_all(self):
        self.difficulty = self.max_dif
        print self.difficulty

    def decrease_all(self):
        self.difficulty = 0
        print self.difficulty

    def increase_five(self):
        self.difficulty += 5
        if self.difficulty > self.max_dif:
            self.difficulty = self.max_dif
        print self.difficulty

    def decrease_five(self):
        self.difficulty -= 5
        if self.difficulty < 0:
            self.difficulty = 0
        print self.difficulty

    def increase(self):
        self.difficulty += 1
        if self.difficulty > self.max_dif:
            self.difficulty = self.max_dif
        print self.difficulty

    def decrease(self):
        self.difficulty -= 1
        if self.difficulty < 0:
            self.difficulty = 0
        print self.difficulty

    def enter_game(self):
        if self.val:
                master.reset(self.difficulty)
                reset_imp()
                master.player.sprite.x = master.home.x
                master.player.sprite.y = master.home.y
        else:
            ready_level(master, self.difficulty)
        print "YO"
        self.state_manager.swap("game")

    def setup(self):
        func = {
            'increase': self.increase, 'decrease': self.decrease, 'enter_game': self.enter_game, 'decrease_five': self.decrease_five,
            'increase_five': self.increase_five, 'increase_all': self.increase_all, 'decrease_all': self.decrease_all,
            'increase_max_dif': self.increase_max_dif
        }
        self.buttons, self.locked_buttons, self.disp_buttons = start_state_buttons(self.image_dict, func, self.batch, self.label_batch)
        for button in self.buttons:
            self.manager.add_button(button)
        for button in self.disp_buttons:
            self.manager.add_button(button)
        for button in self.locked_buttons:
            self.manager.add_button(button)


class StateManager(object):

    def __init__(self, assets):
        self.assets = assets
        self.current = MainMenuState(self)
        self.past = None
        self.pause = PauseState(self)

    def swap(self, string):
        print string + " swap"
        self.past = self.current
        if string == 'game':
            self.current = GameState(self)
        if string == 'pause':
            self.current = self.pause
        # if string == 'build':
        #     self.current = BuildState()
        if string == 'select':
            self.current = SelectState(self)

    def swap_special(self, string):
        print string + " special"
        if string == 'select':
            self.current = SelectState(self, flag=True)

    def swapback(self):
        temp = self.past
        self.past = self.current
        self.current = temp
