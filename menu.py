from button import Button
from utility import * # noqa
from importer import * # noqa

xyz = load_image('drawing.png', False)


class MenuButton(Button):
    def __init__(self, upsprite, hoversprite, downsprite, x, y, xory, callback=None, batch=None, label=None):
        super(MenuButton, self).__init__(
            upsprite, hoversprite, downsprite, x, y,
            callback, batch, label
        )
        self.menus = []
        self.flag = False
        self.xory = xory

    def on_mouse_press(self, x, y, mode):
        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height):
                    self.showmenu()
        for menu in self.menus:
            menu.on_mouse_press(x, y, mode)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def populate(self, x, y, flag):
        if flag:
            for i in range(5):
                self.menus.append(
                    MenuButton(
                        xyz, xyz, xyz, self.sprite.x + x * (10 * (i + 1) + self.sprite.width * (i + 1)),
                        self.sprite.y + y * (10 * (i + 1) + self.sprite.height * (i + 1)), False, None, MenuBatch, None
                    )
                )

                self.menus[i].sprite.scale = .2
        else:
            for i in range(5):
                self.menus.append(
                    Button(
                        xyz, xyz, xyz, self.sprite.x + x * (10 * (i + 1) + self.sprite.width * (i + 1)),
                        self.sprite.y - y * (10 * (i + 1) + self.sprite.height * (i + 1)), None, MenuBatch, None
                    )
                )
                self.menus[i].sprite.scale = .2

    def showmenu(self):
        print "FUCK"

        if self.flag:
            self.flag = False
            self.menus = []
        else:
            self.flag = True
            if self.xory:
                self.populate(1, 0, True)
            else:
                self.populate(0, 1, False)
Buildmenu = MenuButton(
    xyz, xyz, xyz, 850,
    730, True, None, MenuBatch, None
)
Buildmenu.sprite.scale = .2
