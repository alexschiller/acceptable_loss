from importer import * # noqa
import pyglet
import random
import json # noqa
from collide import * # noqa
from character import * # noqa
from enemy import * # noqa
#from utility import * # noqa

window_height = 800
window_width = 1400
level_dict = ['bridge', 'flat', 'maze', 'puzzle', 'shop']
node_dict = ['right', 'left', 'up', 'down']
sprite_dict = {}
sprite_dict['bridge'] = pyglet.image.create(window_width/2, window_height/2, pyglet.image.SolidColorImagePattern(color=(120, 120, 120, 150))) # noqa
sprite_dict['flat'] = pyglet.image.create(window_width/2, window_height/2, pyglet.image.SolidColorImagePattern(color=(150, 150, 0, 150))) # noqa
sprite_dict['maze']= pyglet.image.create(window_width/2, window_height/2, pyglet.image.SolidColorImagePattern(color=(100, 0, 100, 150))) # noqa
sprite_dict['puzzle'] = pyglet.image.create(window_width/2, window_height/2, pyglet.image.SolidColorImagePattern(color=(0, 200, 50, 150))) # noqa
sprite_dict['shop'] = pyglet.image.create(window_width/2, window_height/2, pyglet.image.SolidColorImagePattern(color=(100, 0, 200, 150))) # noqa


def calc_vel_xy(tar_x, tar_y, start_x, start_y, velocity):
    dif_y = tar_y - start_y
    dif_x = tar_x - start_x
    try:
        dir_y = dif_y / abs(dif_y)
    except:
        dir_y = 1
    try:
        dir_x = dif_x / abs(dif_x)
    except:
        dir_x = 1
    try:
        perc = float(abs(dif_y)) / (abs(dif_y) + abs(dif_x))
    except:
        perc = .1
    vel_y = perc * velocity * dir_y
    vel_x = (velocity - abs(vel_y)) * dir_x
    return (vel_x, vel_y)


class Portal(object):
    def __init__(self, x, y, width, height, batch, master):
        h_choice = random.randint(0, height)
        w_choice = random.randint(0, width)
        self.sprite = pyglet.sprite.Sprite(
            load_image('portal.png'),
            x + w_choice, y + h_choice, batch=batch
        )
        self.collision = SpriteCollision(self.sprite)
        self.manager = master

    def on_colide(self):
        master.reset()

    def move(self, dx, dy):
        self.sprite.x += dx
        self.sprite.y += dy

    def update(self):
        self.sprite.rotation += 3
        if self.sprite.rotation > 359:
            self.sprite.rotation = self.sprite.rotation - 360


class Wall(object):
    def __init__(self, player, x, y, height, width, batch=None):
        self.player = player
        image = pyglet.image.create(width, height, pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 255)))
        self.sprite = pyglet.sprite.Sprite(
            image,
            x, y, batch=batch
        )
        self.collision = SpriteCollision(self.sprite)

    def on_collide(self):
        self.player.controller.undo_move()

    def update(self):
        if collide(self.collision, self.player.collision):
            self.on_collide()


class Room(object):
    def __init__(self, number):
        self.walls = []
        self.called = False
        self.sprite = None
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

    def move(self, dx, dy):
        self.sprite.x += dx
        self.sprite.y += dy
        for wall in self.walls:
            wall.sprite.x += dx
            wall.sprite.y += dy

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

    def create_sprites(self, x, y, batch, player):
        if self.called is False:
            self.sprite = pyglet.sprite.Sprite(
                sprite_dict[self.type],
                x, y, batch=batch
            )
            self.called = True
            if self.left is not None:
                self.left.create_sprites(x - window_width / 2, y, batch, player)
            else:
                self.walls.append(Wall(player, self.sprite.x - 30, self.sprite.y, self.sprite.height, 30, batch))
            if self.right is not None:
                self.right.create_sprites(x + window_width / 2, y, batch, player)
            else:
                self.walls.append(Wall(player, self.sprite.x + self.sprite.width, self.sprite.y, self.sprite.height, 30, batch))
            if self.up is not None:
                self.up.create_sprites(x, y + window_height / 2, batch, player)
            else:
                self.walls.append(Wall(player, self.sprite.x, self.sprite.y + self.sprite.height, 30, self.sprite.width, batch))
            if self.down is not None:
                self.down.create_sprites(x, y - window_height / 2, batch, player)
            else:
                self.walls.append(Wall(player, self.sprite.x, self.sprite.y - 30, 30, self.sprite.width, batch))


class RoomManager(object):
    def __init__(self, master):
        self.master = master
        self.grid = []
        for i in range(100):
            self.grid.append([-1] * 100)
        self.parent = Room(0)
        self.parent.setup()
        self.roomlist = []
        self.roomlist.append(self.parent)
        self.grid[49][49] = 0
        self.parent.location = [49, 49]
        self.portal = None

    def setup(self, amount):
        self.parent.left = 1
        # for i in range(1, 4):
        k = 1
        for i in ['left', 'right', 'down']:
            temproom = Room(k)
            parent = self.roomlist[0]
            while not parent.available():
                parent = self.roomlist[random.randint(0, len(self.roomlist) - 1)]

            # choices = parent.available()
            # choice = choices[random.randint(0, len(choices) - 1)]
            choice = i
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
            k += 1

    def add_enemies(self, difficulty):
        for room in self.roomlist:
            room_x_min = room.sprite.x
            room_x_max = room_x_min + room.sprite.width
            room_y_min = room.sprite.y
            room_y_max = room_y_min + room.sprite.height
            for i in range(2):
                Character(
                    self.master,
                    random.choice([
                        # enemy_soldier_base(
                        #     difficulty, random.randint(room_x_min, room_x_max),
                        #     random.randint(room_y_min, room_y_max)),

                        # enemy_tank_base(
                        #     difficulty, random.randint(room_x_min, room_x_max),
                        #     random.randint(room_y_min, room_y_max)),

                        enemy_zombie_base(
                            difficulty, random.randint(room_x_min, room_x_max),
                            random.randint(room_y_min, room_y_max)),

                        enemy_drone_base(
                            difficulty, random.randint(room_x_min, room_x_max),
                            random.randint(room_y_min, room_y_max)),
                    ]))

    def move_all(self, dx, dy):
        for room in self.roomlist:
            room.move(dx, dy)
        self.portal.move(dx, dy)

    def update(self):
        for room in self.roomlist:
            for wall in room.walls:
                wall.update()
        self.portal.update()

    def create_portal(self):
        choice = random.choice(self.roomlist)
        self.portal = Portal(choice.sprite.x, choice.sprite.y, choice.sprite.width, choice.sprite.height, PortalBatch, self.master)

    def delete_all(self):
        for room in self.roomlist:
            room.sprite.delete()
            room.right = None
            room.left = None
            room.up = None
            room.down = None
            for wall in room.walls:
                wall.sprite.delete()
                wall = None
            room.walls = None
            room = None
        self.roomlist = None
        self = None
# with open('testthing.py', 'w') as f:
#     json.dump(test.grid, f)
