import pyglet # noqa
import random # noqa
import json # noqa
from collide import * # noqa
from character import * # noqa
from enemy import * # noqa


window_height = 800
window_width = 1400


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


class Portal(object):
    def __init__(self, x, y, batch, master):
        # h_choice = random.randint(0, height)
        # w_choice = random.randint(0, width)
        self.sprite = pyglet.sprite.Sprite(
            load_image('portal.png'),
            x, y, batch=batch
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


class Room(object):
    def __init__(self):
        self.enemies = None
        self.walls = None
        self.portal = None
        self.dimen = [window_width, window_height]
        self.wallbatch = pyglet.graphics.Batch()

    def add_enemies(self, difficulty, master):
        room_x_min = 20
        room_x_max = self.dimen[0] - 20
        room_y_min = 20
        room_y_max = self.dimen[1] - 20
        for i in range(7):
            Character(
                master,
                random.choice([
                    enemy_soldier_base(
                        difficulty, random.randint(room_x_min, room_x_max),
                        random.randint(room_y_min, room_y_max)),

                    enemy_tank_base(
                        difficulty, random.randint(room_x_min, room_x_max),
                        random.randint(room_y_min, room_y_max)),

                    enemy_zombie_base(
                        difficulty, random.randint(room_x_min, room_x_max),
                        random.randint(room_y_min, room_y_max)),

                    enemy_drone_base(
                        difficulty, random.randint(room_x_min, room_x_max),
                        random.randint(room_y_min, room_y_max)),
                ]))

    def add_walls(self, player):
        self.walls = []
        self.walls.append(Wall(player, 0, 0, 20, self.dimen[0] - 20, self.wallbatch))
        self.walls.append(Wall(player, 0, self.dimen[1] - 20, 20, self.dimen[0], self.wallbatch))
        self.walls.append(Wall(player, self.dimen[0] - 20, 0, self.dimen[0], 20, self.wallbatch))
        self.walls.append(Wall(player, 0, 0, self.dimen[0], 20, self.wallbatch))

    def setup(self, master):
        self.add_enemies(master.difficulty, master)
        self.add_walls(master.player)
        self.portal = Portal(random.randint(40, window_width - 20), random.randint(40, window_height - 40), self.wallbatch, master)
        print "set up complete"

    def update(self):
        for wall in self.walls:
            wall.update()
        self.portal.update()

    def draw(self):
        self.wallbatch.draw()

    def delete_all(self):
        for wall in self.walls:
            wall.image = None
            wall.sprite.delete()
        self.walls = None
        self.portal.image = None
        self.portal.sprite.delete()
        self.portal = None


class Dungeon(object):
    def __init__(self):
        self.room = None
        self.rooms = None
        self.end = None

    def setup(self):
        self.room = Room()
        print " D setup"

    def initialize(self, master):
        self.room.setup(master)
        print "init"

    def update(self):
        self.room.update()

    def draw(self):
        self.room.draw()

    def delete_all(self):
        self.room.delete_all()
        self.room = None
