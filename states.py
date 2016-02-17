import pyglet  # noqa
from pyglet.gl import *  # noqa
from pyglet.window import key # noqa
from utility import * # noqa
from importer import * # noqa


class ProtoKeyStateHandler(key.KeyStateHandler):

    def __init__(self):
        self.list = []
        self.active = False

    def on_key_press(self, symbol, modifiers):
        self[symbol] = True
        if self.active:
            self.list.append(symbol)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def clear_state(self):
        self.list = []

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


class GameState(StateObject):
    def __init__(self, manager):
        super(GameState, self).__init__(manager)

        self.Pause = 0
        self.Build = 0
        self.Menu = 0
        self.last_time = 0
        self.batch_setup()

    def batch_setup(self):
        self.batches = [
            TerrainBatch, PortalBatch, master.player.sprite, BulletBatch, EffectsBatch, BarBatch,
            gfx_batch, BuildingBatch, HotbarBatch, HotbarButtonBatch,
        ]

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            master.player_controller.move_to(x, y)
        if button == 4:
            master.player_controller.slot_mouse_two_fire()

    def on_mouse_motion(self, x, y, dx, dy):
        master.player_controller.sprite.x = x
        master.player_controller.sprite.y = y
        master.player_controller.rotate(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        master.player_controller.sprite.x = x
        master.player_controller.sprite.y = y
        # master.update_button_image(x, y, dx, dy)

    def update(self, ts):
        mx = 0
        my = 0
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
        mx = 0
        my = 0
        if key_handler[key.X]:
            if collide(master.player.collision, master.room_manager.portal.collision):
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
            ps = pstats.Stats(master.pr, stream=s).sort_stats(sortby)
            ps.print_stats()

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
            print "SDFSDFDSFSDFSDF"
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


class SelectState(StateObject):
    def __init__(self, manager, flag=False):
        super(SelectState, self).__init__(manager)
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
                print "test"
                reset_imp()
                master.reset()
                master.player.sprite.x = master.home.x
                master.player.sprite.y = master.home.y
        else:
            print "more test"
            ready_level(master, self.difficulty, 5)
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
        self.past = self.current
        print string
        if string == 'game':
            print "yo"
            self.current = GameState(self)
        if string == 'pause':
            self.current = self.pause
        # if string == 'build':
        #     self.current = BuildState()
        if string == 'select':
            self.current = SelectState(self)

    def swap_special(self, string):
        if string == 'select':
            self.current = SelectState(self, flag=True)

    def swapback(self):
        temp = self.past
        self.past = self.current
        self.current = temp
