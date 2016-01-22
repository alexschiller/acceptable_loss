from utility import * # noqa
from importer import * # noqa
import json # noqa
level_dict = ['bridge', 'flat', 'maze', 'puzzle', 'shop']
node_dict = ['right', 'left', 'up', 'down']
sprite_dict = {}
sprite_dict['bridge'] = pyglet.image.create(windowwidth/2, windowheight/2, pyglet.image.SolidColorImagePattern(color=(120, 120, 120, 150))) # noqa
sprite_dict['flat'] = pyglet.image.create(windowwidth/2, windowheight/2, pyglet.image.SolidColorImagePattern(color=(150, 150, 0, 150))) # noqa
sprite_dict['maze']= pyglet.image.create(windowwidth/2, windowheight/2, pyglet.image.SolidColorImagePattern(color=(100, 0, 100, 150))) # noqa
sprite_dict['puzzle'] = pyglet.image.create(windowwidth/2, windowheight/2, pyglet.image.SolidColorImagePattern(color=(0, 200, 50, 150))) # noqa
sprite_dict['shop'] = pyglet.image.create(windowwidth/2, windowheight/2, pyglet.image.SolidColorImagePattern(color=(100, 0, 200, 150))) # noqa


class Room(object):
    def __init__(self, number):
        self.called = False
        self.Sprite = None
        self.number = number
        self.location = None
        self.type = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None

    def setup(self):
        self.type = level_dict[random.randint(0, len(level_dict) - 1)]

    def available(self):
        child = []
        if self.left is None:
            child.append('left')
        if self.right is None:
            child.append('right')
        if self.up is None:
            child.append('up')
        if self.down is None:
            child.append('down')
        if len(child) is 0:
            return False
        else:
            return child

    def printobject(self):
        print str(self.number) + " " + str(self.type) + "   begin"

        try:
            self.left.printobject()
        except:
            pass
        try:
            self.down.printobject()
        except:
            pass
        try:
            self.up.printobject()
        except:
            pass
        try:
            self.right.printobject()
        except:
            pass
        print str(self.number) + " " + str(self.type) + "   end"

    def create_sprites(self, x, y):
        if self.called is False:
            self.Sprite = pyglet.sprite.Sprite(
                sprite_dict[self.type],
                x, y, batch=TerrainBatch
            )
            self.called = True
            if self.left is not None:
                self.left.create_sprites(x - windowwidth / 2, y)
            if self.right is not None:
                self.right.create_sprites(x + windowwidth / 2, y)
            if self.up is not None:
                self.up.create_sprites(x, y + windowheight / 2)
            if self.down is not None:
                self.down.create_sprites(x, y - windowheight / 2)


class RoomManager(object):
    def __init__(self):
        self.grid = []
        for i in range(100):
            self.grid.append([-1] * 100)
        self.parent = Room(0)
        self.parent.setup()
        self.roomlist = []
        self.roomlist.append(self.parent)
        self.grid[49][49] = 0
        self.parent.location = [49, 49]

    def setup(self, amount):
        for i in range(1, amount):
            temproom = Room(i)
            parent = self.roomlist[random.randint(0, len(self.roomlist) - 1)]
            while not parent.available():
                parent = self.roomlist[random.randint(0, len(self.roomlist) - 1)]
                print "FUCK"

            choices = parent.available()
            choice = choices[random.randint(0, len(choices) - 1)]
            # test = ""
            # for shit in choices:
            #     test += " " + shit
            # print test + " :::::" + choice
            temproom.location = []
            temproom.location.append(parent.location[0])
            temproom.location.append(parent.location[1])

            if choice == 'left':
                temproom.location[1] -= 1
            if choice == 'down':
                temproom.location[0] += 1
            if choice == 'right':
                temproom.location[1] += 1
            if choice == 'up':
                temproom.location[0] -= 1
            temproom.setup()
            self.roomlist.append(temproom)
            x = temproom.location
            self.grid[x[0]][x[1]] = i
            if self.grid[x[0]][x[1] - 1] != -1:  # left
                temproom.left = self.roomlist[self.grid[x[0]][x[1] - 1]]
                self.roomlist[self.grid[x[0]][x[1] - 1]].right = temproom
            if self.grid[x[0]][x[1] + 1] != -1:  # right
                temproom.right = self.roomlist[self.grid[x[0]][x[1] + 1]]
                self.roomlist[self.grid[x[0]][x[1] + 1]].left = temproom
            if self.grid[x[0] - 1][x[1]] != -1:  # up
                temproom.up = self.roomlist[self.grid[x[0] - 1][x[1]]]
                self.roomlist[self.grid[x[0] - 1][x[1]]].down = temproom
            if self.grid[x[0] + 1][x[1]] != -1:  # down
                temproom.down = self.roomlist[self.grid[x[0] + 1][x[1]]]
                self.roomlist[self.grid[x[0] + 1][x[1]]].up = temproom


test = RoomManager()
test.setup(13)

# with open('testthing.py', 'w') as f:
#     json.dump(test.grid, f)
