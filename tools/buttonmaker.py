

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter  # noqa
    from tkFileDialog import askdirectory

except ImportError:
    # for Python3
    from tkinter import *   ## notice here too # noqa
import json
from callables import callables
root = Tk()
root.withdraw()
file_path = askdirectory()
print file_path


from makerbuttons import Manager, Button,TextBox, DraggableButton, foo, MenuButton # noqa
import pyglet # noqa
import glob # noqa
import os # noqa
from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa

savedpath = os.path.dirname(os.path.realpath(__file__))

imglist = []

os.chdir(file_path)
for file in glob.glob("*.png"):
    try:
        img = pyglet.image.load(file)
        if img.height <= 200 and img.width <= 200 and img.height * img.width >= 700:
            imglist.append([img, file])
    except:
        pass
os.chdir(savedpath)
batches = [pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch(), ]


class ImageMenu(object):
    def __init__(self, images, game):
        self.flag = 0
        self.batches = [pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch()]
        self.game = game
        self.images = images
        self.page = 1
        self.maxpage = len(self.images) / 5
        if len(self.images) % 5 > 0:
            self.maxpage += 1

        self.backing = menu_back = pyglet.image.create(400, window_height, pyglet.image.SolidColorImagePattern(color=(200, 200, 120, 155))) # noqa
        self.sprite = pyglet.sprite.Sprite(
            self.backing,
            1000, 0, batch=self.batches[0]
        )
        self.image_sprites = []
        self.buttons = []
        for i in range(5):
            try:
                sprite = pyglet.sprite.Sprite(
                    self.images[i][0],
                    self.sprite.x + self.sprite.width / 2, 100 + 100 * i, batch=self.batches[1]
                )
                self.image_sprites.append(MenuButton(sprite, self, i))
            except:
                pass
        self.setup()
        self.buttonflag = 0
        self.hoverflag = 0
        self.pressflag = 0

    def changebf(self):
        self.buttonflag = 1
        self.hoverflag = 0
        self.pressflag = 0

    def changehf(self):
        self.buttonflag = 0
        self.hoverflag = 1
        self.pressflag = 0

    def changeall(self):
        self.buttonflag = 1
        self.hoverflag = 1
        self.pressflag = 1

    def changepf(self):
        self.buttonflag = 0
        self.hoverflag = 0
        self.pressflag = 1

    def alert(self, ide):
        if self.buttonflag:
            print "bf : " + str(self.buttonflag)
            self.game.option_menu.button.sprite.image = self.images[ide][0]

        if self.hoverflag:
            self.game.option_menu.button.hoversprite = self.images[ide][0]
            self.game.option_menu.button.hoversprite_img_loc = self.images[ide][1]
            print self.images[ide][1]

        if self.pressflag:
            self.game.option_menu.button.downsprite = self.images[ide][0]
            self.game.option_menu.button.downsprite_img_loc = self.images[ide][1]
            print self.images[ide][1]

        if self.buttonflag:
            self.game.option_menu.button.upsprite = self.images[ide][0]
            self.game.option_menu.button.upsprite_img_loc = self.images[ide][1]
            print self.images[ide][1]

    def changepage(self):
        self.image_sprites = []
        x = 0
        for i in range((self.page - 1) * 5, self.page * 5):
            try:
                sprite = pyglet.sprite.Sprite(
                    self.images[i][0],
                    self.sprite.x + self.sprite.width / 2, 100 + 100 * x, batch=self.batches[1]
                )
                self.image_sprites.append(MenuButton(sprite, self, i))

                x += 1
            except:
                pass

    def pageleft(self):
        self.page -= 1
        if self.page < 1:
            self.page = self.maxpage
        self.changepage()

    def pageright(self):
        self.page += 1
        if self.page > self.maxpage:
            self.page = 1
        self.changepage()

    def setup(self):
        back = pyglet.image.create(30, 30, pyglet.image.SolidColorImagePattern(color=(100, 100, 90, 180)))
        back2 = pyglet.image.create(60, 30, pyglet.image.SolidColorImagePattern(color=(100, 100, 90, 180)))
        self.buttons.append(
            Button(
                back, back, back, self.sprite.x + 5,
                self.sprite.y + self.sprite.height - 35, self.pageleft, self.batches[1],
            )
        )
        self.buttons.append(
            Button(
                back, back, back, self.sprite.x + self.sprite.width - 35,
                self.sprite.y + self.sprite.height - 35, self.pageright, self.batches[1],
            )
        )
        #  flag changers
        self.buttons.append(   # all
            Button(
                back2, back2, back2, self.sprite.x + self.sprite.width / 2 - 130,
                self.sprite.y + self.sprite.height - 75, self.changeall, self.batches[1], "all", None, self.batches[2]
            )
        )

        self.buttons.append(   # bf
            Button(
                back2, back2, back2, self.sprite.x + self.sprite.width / 2 - 65,
                self.sprite.y + self.sprite.height - 75, self.changebf, self.batches[1], " button", None, self.batches[2]
            )
        )

        self.buttons.append(   # hf
            Button(
                back2, back2, back2, self.sprite.x + self.sprite.width / 2 + 130,
                self.sprite.y + self.sprite.height - 75, self.changehf, self.batches[1], "hover", None, self.batches[2]
            )
        )

        self.buttons.append(   # pf
            Button(
                back2, back2, back2, self.sprite.x + self.sprite.width / 2 + 65,
                self.sprite.y + self.sprite.height - 75, self.changepf, self.batches[1], "press", None, self.batches[2]
            )
        )
        self.buttons[2].label.font_size = 12
        self.buttons[3].label.font_size = 12
        self.buttons[4].label.font_size = 12
        self.buttons[5].label.font_size = 12

    def on_mouse_press(self, x, y, mode):
        if self.flag:
            if (
                self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height
            ):
                for button in self.buttons:
                    button.on_mouse_press(x, y, mode, val=True)
                for button in self.image_sprites:
                    button.on_mouse_press(x, y, mode)
                return True
        else:
            return False

    def update(self):
        if self.flag:
            for batch in self.batches:
                batch.draw()


class ClickMenu(object):
    def __init__(self, button, x, y, game):
        self.flag = 0
        self.batches = [pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch()]
        self.game = game
        self.button = button
        self.backing = pyglet.image.create(100, 150, pyglet.image.SolidColorImagePattern(color=(144, 144, 144, 255))) # noqa
        self.sprite = pyglet.sprite.Sprite(
            self.backing,
            x, y, batch=self.batches[0]
        )
        self.buttons = []
        self.setup()

    def setlocation(self, x, y):
        dify = self.sprite.y - y
        difx = self.sprite.x - x
        self.sprite.x -= difx
        self.sprite.y -= dify
        for button in self.buttons:
            button.move(button.sprite.x - difx, button.sprite.y - dify)

    def load_image(self):
        print "load_image"
        self.game.select_image()

    def load_strings(self):
        self.game.select_func()

    def load_coord(self):
        self.game.select_coord()

    def change_image(self, string):
        try:
            img = pyglet.image.load(string)
            self.button.upsprite.image = img
        except:
            pass

    def on_mouse_press(self, x, y, mode):
        if self.flag:
            if (
                self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height
            ):
                for button in self.buttons:
                    button.on_mouse_press(x, y, mode)
                return True
        else:
            return False

    def setup(self):
        back = pyglet.image.create(90, 30, pyglet.image.SolidColorImagePattern(color=(40, 44, 44, 180)))
        self.buttons.append(
            Button(
                back, back, back, self.sprite.x + 5,
                self.sprite.y + self.sprite.height - 35, self.load_image, self.batches[1], "change image",
                None, self.batches[2]
            )
        )
        self.buttons[0].label.font_size = 12

        self.buttons.append(
            Button(
                back, back, back, self.sprite.x + 5,
                self.sprite.y + self.sprite.height - 70, self.load_strings, self.batches[1], "set callable",
                None, self.batches[2]
            )
        )

        self.buttons[1].label.font_size = 12

        self.buttons.append(
            Button(
                back, back, back, self.sprite.x + 5,
                self.sprite.y + self.sprite.height - 105, self.load_coord, self.batches[1], "set cords",
                None, self.batches[2]
            )
        )

        self.buttons[2].label.font_size = 12

        # self.buttons.append(
        #     Button(
        #         back, back, back, self.sprite.x + 5,
        #         self.sprite.y + self.sprite.height - 70, , batches[2],
        #     )
        # )

    def update(self):
        if self.flag:
            for batch in self.batches:
                batch.draw()


class NumMenu(ClickMenu):
    def __init__(self, x, y, game):
        self.flag = 0
        self.select = 0
        self.cords = ""

        self.batches = [pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch()]
        self.game = game
        self.backing = menu_back = pyglet.image.create(400, window_height, pyglet.image.SolidColorImagePattern(color=(200, 200, 120, 155))) # noqa
        self.sprite = pyglet.sprite.Sprite(
            self.backing,
            1000, 0, batch=self.batches[0]
        )
        self.buttons = []
        self.label = pyglet.text.Label(
            "",
            font_name='Times New Roman',
            font_size=32,
            x=self.sprite.x + self.sprite.width / 2,
            y=self.sprite.height - 200,
            anchor_x='center',
            anchor_y='center',
            batch=self.batches[2]
        )
        self.setup()

    def set(self):
        if self.select == 0:
            self.game.option_menu.button.sprite.x = int(self.cords)
        else:
            self.game.option_menu.button.sprite.y = int(self.cords)

    def clear(self):
        self.cords = ""
        print self.cords

    def alert(self, ide):
        if ide != 'set' and ide != 'c':
            self.cords += str(ide)
            print self.cords
        else:
            if ide == 'set':
                self.set()
            if ide == 'c':
                self.clear()

    def setup(self):
        size = 50
        back = pyglet.image.create(size, size, pyglet.image.SolidColorImagePattern(color=(100, 100, 120, 155))) # noqa
        for i in range(10):
                sprite = pyglet.sprite.Sprite(
                    back,
                    self.sprite.x + self.sprite.width / 2 + (size + 5) * ((i % 3) - 1), 300 + (size + 5) * (i / 3), batch=self.batches[1]
                )
                self.buttons.append(MenuButton(sprite, self, i, str(i), self.batches[2]))
        sprite = pyglet.sprite.Sprite(
            back,
            self.sprite.x + self.sprite.width / 2 + (size + 5) * ((10 % 3) - 1), 300 + (size + 5) * (10 / 3), batch=self.batches[1]
        )
        self.buttons.append(MenuButton(sprite, self, 'c', 'c', self.batches[2]))

        sprite = pyglet.sprite.Sprite(
            back,
            self.sprite.x + self.sprite.width / 2 + (size + 5) * ((11 % 3) - 1), 300 + (size + 5) * (11 / 3), batch=self.batches[1]
        )
        self.buttons.append(MenuButton(sprite, self, 'set', 'set', self.batches[2]))

    def update(self):
        if self.flag:
            self.label.text = self.cords
            for batch in self.batches:
                batch.draw()


class StringMenu(ClickMenu):
    def __init__(self, x, y, game):
        self.page = 1
        self.maxpage = len(callables) / 10
        if len(callables) % 10 > 0:
            self.maxpage += 1

        self.flag = 0
        self.batches = [pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch()]
        self.game = game
        self.backing = pyglet.image.create(400, window_height, pyglet.image.SolidColorImagePattern(color=(200, 200, 120, 155))) # noqa
        self.sprite = pyglet.sprite.Sprite(
            self.backing,
            1000, 0, batch=self.batches[0]
        )
        self.buttons = []
        self.string_calls = []
        self.setup()

    def alert(self, ide):
        self.game.option_menu.button.callbackstr = callables[ide]

    def changepage(self):
        for item in self.string_calls:
            item.label.delete()
        self.string_calls = []
        backing = pyglet.image.create(90, 30, pyglet.image.SolidColorImagePattern(color=(144, 144, 144, 255))) # noqa
        x = 0
        for i in range((self.page - 1) * 10, self.page * 10):
            try:
                sprite = pyglet.sprite.Sprite(
                    backing,
                    self.sprite.x + self.sprite.width / 2, 300 + 40 * x, batch=self.batches[1]
                )
                self.string_calls.append(MenuButton(sprite, self, i, callables[i], self.batches[2]))
                x += 1
            except:
                pass

    def pageleft(self):
        self.page -= 1
        if self.page < 1:
            self.page = self.maxpage
        self.changepage()

    def pageright(self):
        self.page += 1
        if self.page > self.maxpage:
            self.page = 1
        self.changepage()

    def setup(self):
        # i = 0
        backing = pyglet.image.create(90, 30, pyglet.image.SolidColorImagePattern(color=(144, 144, 144, 255))) # noqa
        self.changepage()
        # for item in callables:
        #     sprite = pyglet.sprite.Sprite(
        #         backing, self.sprite.x + self.sprite.width / 2 - backing.width / 2, 200 + (backing.height + 10) * i,
        #         batch=self.batches[1]
        #     )
        #     self.string_calls.append(MenuButton(sprite, self, i, item, self.batches[2]))
        #     i += 1
        #     if i == 10:
        #         break

        back = pyglet.image.create(30, 30, pyglet.image.SolidColorImagePattern(color=(100, 100, 90, 180)))
        self.buttons.append(
            Button(
                back, back, back, self.sprite.x + 5,
                self.sprite.y + self.sprite.height - 35, self.pageleft, self.batches[1],
            )
        )
        self.buttons.append(
            Button(
                back, back, back, self.sprite.x + self.sprite.width - 35,
                self.sprite.y + self.sprite.height - 35, self.pageright, self.batches[1],
            )
        )

    def on_mouse_press(self, x, y, mode):
        if self.flag:
            if (
                self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height
            ):
                for button in self.string_calls:
                    button.on_mouse_press(x, y, mode)
                for button in self.buttons:
                    button.on_mouse_press(x, y, mode)
                return True
        else:
            return False


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


def load_image(image, anchor=True):
    try:
        return image_dict(image)
    except:
        img = pyglet.image.load('../images/' + image)
        if anchor:
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
        return img

# tank = load_image('tank.png', False)
# sprite = pyglet.sprite.Sprite(
#     tank,
#     0, 0, batch=batches[0]
# )


button = load_image('button.png', False)
buttonhover = load_image('buttonhover.png', False)
buttondown = load_image('buttondown.png', False)


class Game(pyglet.window.Window):
    def __init__(self, height, width, batches):
        super(Game, self).__init__(width, height, caption='Buttons')

        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.alive = True
        self.batches = batches
        self.buttons = []
        self.manager = Manager()
        self.module_manager = Manager()
        self.setup()
        self.option_menu = ClickMenu(None, 0, 0, self)
        self.imagemenu = ImageMenu(imglist, self)
        self.stringmenu = StringMenu(0, 0, self)
        self.coordmenu = NumMenu(0, 0, self)

    def select_image(self):
        self.imagemenu.flag = 1

    def select_func(self):
        self.stringmenu.flag = 1

    def select_coord(self):
        self.coordmenu.flag = 1

    def create_button(self):
        self.module_manager.add_button(
            DraggableButton(
                button, buttonhover, buttondown, 600,
                600, None, self.batches[0]
            )
        )

    def export_buttons(self):
        blist = []
        for button in self.module_manager.buttons:
            blist.append(button.export())
        json.dump(blist, open("button_dict.py", 'w'), indent=4, separators=(',', ': '))

    def setup(self):
        self.manager.add_button(
            Button(
                button, buttonhover, buttondown, 100,
                100, self.create_button, self.batches[0], "make button", None, self.batches[1]
            )
        )
        self.manager.add_button(
            Button(
                button, buttonhover, buttondown, 100,
                340, self.export_buttons, self.batches[0], "export", None, self.batches[1]
            )
        )

    def render(self, *args):
        self.clear()
        self.update()
        for batch in self.batches:
            batch.draw()

        self.option_menu.update()
        self.imagemenu.update()
        self.stringmenu.update()
        self.coordmenu.update()
        self.flip()

    def make_dict(self):
        pass

    def update(self):
        pass
        # if key_handler[key.D]:
        #     sprite.x += 1
        # if key_handler[key.A]:
        #     sprite.x -= 1
        # if key_handler[key.W]:
        #     sprite.y += 1
        # if key_handler[key.S]:
        #     sprite.y -= 1

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = False

    # def on_key_press(self, symbol, modkey):
    #     self.state_manager.current.on_key_press(symbol, modkey)

    # def on_key_release(self, symbol, modkey):
    #     self.state_manager.current.on_key_release(symbol, modkey)

    def on_mouse_release(self, x, y, button, modifiers):
        self.manager.update(x, y, 1)
        self.module_manager.update(x, y, 1)
        self.option_menu.on_mouse_press(x, y, 1)
        self.imagemenu.on_mouse_press(x, y, 1)
        self.stringmenu.on_mouse_press(x, y, 1)
        self.coordmenu.on_mouse_press(x, y, 1)

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.update(x, y, 0)
        self.module_manager.update(x, y, 0)

        if button == 1:
            if self.coordmenu.on_mouse_press(x, y, 0):
                pass
            else:
                self.coordmenu.flag = 0

            if self.imagemenu.on_mouse_press(x, y, 0):
                pass
            else:
                self.imagemenu.flag = 0

            if self.option_menu.on_mouse_press(x, y, 0):
                pass
            else:
                self.option_menu.flag = 0
            if self.stringmenu.on_mouse_press(x, y, 0):
                pass
            else:
                self.stringmenu.flag = 0
        if button == 4:
            b = self.module_manager.get_button(x, y)
            if b is not None:

                self.option_menu.flag = 1
                self.option_menu.button = b
                self.option_menu.setlocation(x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        self.manager.update_image(x, y, dx, dy)
        self.module_manager.update_image(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.manager.update_image(x, y, dx, dy)
        self.module_manager.update_image(x, y, dx, dy)

    def run(self):
        while self.alive:
            event = self.dispatch_events()
            if event:
                print(event)
            self.render()

window_height = 800
window_width = 1400
window = Game(window_height, window_width, batches)
key_handler = ProtoKeyStateHandler()

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
window.push_handlers(key_handler)

if __name__ == '__main__':
    pyglet.clock.set_fps_limit(10)

    window.run()
