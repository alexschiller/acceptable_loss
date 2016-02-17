

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter  # noqa
    from tkFileDialog import askdirectory

except ImportError:
    # for Python3
    from tkinter import *   ## notice here too # noqa


root = Tk()
root.withdraw()
file_path = askdirectory()
print file_path


from makerbuttons import Manager, Button,TextBox, DraggableButton, foo # noqa
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
        imglist.append(pyglet.image.load(file))
    except:
        pass

os.chdir(savedpath)
batches = [pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch(), ]


class ImageMenu(object):
    def __init__(self, images):
        self.images = images
        self.backing = menu_back = pyglet.image.create(600, window_height, pyglet.image.SolidColorImagePattern(color=(1, 1, 20, 255))) # noqa
        self.sprite = pyglet.sprite.Sprite(
            self.backing,
            800, 0, batch=batches[1]
        )
        self.image_sprites = []
        for i in range(10):
            sprite = pyglet.sprite.Sprite(
                self.images[i],
                900, 100 + 100 * i, batch=batches[2]
            )
            self.image_sprites.append(sprite)


class ClickMenu(object):
    def __init__(self, button, x, y):
        self.button = button
        self.backing = menu_back = pyglet.image.create(100, 150, pyglet.image.SolidColorImagePattern(color=(100, 100, 20, 255))) # noqa
        self.sprite = pyglet.sprite.Sprite(
            self.backing,
            x, y, batch=batches[1]
        )
        self.buttons = []
        self.setup()

    def load_image(self):
        print 'sup bitches'

    def change_image(self, string):
        try:
            img = pyglet.image.load(string)
            self.button.upsprite.image = img
        except:
            pass

    def on_mouse_press(self, x, y, mode):
        if (
            self.sprite.x < x and
            x < self.sprite.x + self.sprite.width and
            self.sprite.y < y and
            y < self.sprite.y + self.sprite.height
        ):
            print self.buttons
            for button in self.buttons:
                button.on_mouse_press(x, y, mode, val=True)
            return True
        else:
            return False

    def setup(self):
        back = pyglet.image.create(90, 30, pyglet.image.SolidColorImagePattern(color=(1, 1, 1, 180)))
        self.buttons.append(
            Button(
                back, back, back, self.sprite.x + 5,
                self.sprite.y + self.sprite.height - 35, self.load_image, batches[2],
            )
        )
        print "BUT"


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
        img = pyglet.image.load('images/' + image)
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
        self.option_menu = None
        self.imagemenu = ImageMenu(imglist)

    def create_button(self):
        print "HELLO"
        self.module_manager.add_button(
            DraggableButton(
                button, buttonhover, buttondown, 600,
                600, None, self.batches[0]
            )
        )

    def setup(self):
        self.manager.add_button(
            Button(
                button, buttonhover, buttondown, 100,
                100, self.create_button, self.batches[0],
            )
        )

    def render(self, *args):
        self.clear()
        self.update()
        for batch in self.batches:
            batch.draw()

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
        try:
            self.option_menu.on_mouse_press(x, y, 1)
        except:
            pass

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.update(x, y, 0)
        self.module_manager.update(x, y, 0)
        if button == 1:
            try:
                if self.option_menu.on_mouse_press(x, y, 1):
                    pass
                else:
                    self.option_menu = None
            except:
                pass
        if button == 4:
            b = self.module_manager.get_button(x, y)
            if b is not None:
                self.option_menu = ClickMenu(button, x, y)

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
