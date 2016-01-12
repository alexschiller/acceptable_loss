from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import itertools
import pyglet
from gun import * # noqa

class Character(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.spriteeffect = master.spriteeffect
        self.enemies = master.enemies
        self.player = master.player
        self.health_bar = None
        self.target = None

    def update_health_bar(self):
        hw = int(self.sprite.width * 2 * self.health / self.max_health)
        if hw > 0:
            self.health_bar = pyglet.sprite.Sprite(
                pyglet.image.create(hw, 2, red_sprite),
                self.sprite.x - self.sprite.width,
                self.sprite.y + self.sprite.height, batch=BarBatch)
        else:
            self.health_bar = None

    def move(self, x, y):
        self.sprite.x += (self.speed * x)
        self.sprite.y += (self.speed * y)

    def attack(self):
        if self.target:
            self.gun.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self.target) # noqa            

    def update_rotation(self):
        if self.target:
            dist_x = self.target.sprite.x - float(self.sprite.x)
            dist_y = self.target.sprite.y - float(self.sprite.y)
            self.sprite.rotation = (math.degrees(math.atan2(dist_y, dist_x)) * -1) + 90

    def update_movement(self):
        if self.target:
            ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y,
                self.sprite.x, self.sprite.y, self.speed)
            self.sprite.x += ret[0]
            self.sprite.y += ret[1]

    def update_attack(self):
        if math.hypot(abs(self.sprite.x - self.target.sprite.x), abs(self.sprite.y - self.target.sprite.y)) < self.gun.travel: # noqa
            self.attack()

    def death_check(self):
        if self.health <= 0:
            self.on_death()

    def required_updates(self):
        if not self.target:  # This should probably be checked more often
            self.update_target()
        self.update_movement()
        self.update_rotation()
        self.update_attack()
        self.death_check()

    def on_hit(self, bullet):
        self.health -= bullet.damage
        self.update_health_bar()
        self.spriteeffect.blood(bullet.sprite.x, bullet.sprite.y, 3, 5)

    def closest_object(self):
        closest = None
        min_dist = float('inf')
        x1 = self.sprite.x
        y1 = self.sprite.y
        for o in self.master.objects:
            dist = math.sqrt((o.sprite.x - x1) ** 2 + (o.sprite.y - y1) ** 2)
            if dist < min_dist:
                closest = o
                min_dist = dist
        return closest

    def next_gun(self):
        self.gun = self.guns[next(self.cycle_guns)]

    def load_guns(self, guns):
        self.guns = guns
        self.cycle_guns = itertools.cycle(range(len(self.guns)))
        self.gun = self.guns[0]
        self.master.register_guns(self.guns)

    def check_object_collision(self, o):
        if collide(self.collision, o.collision):
            ret = calc_vel_xy(self.sprite.x, self.sprite.y,
            o.sprite.x, o.sprite.y, 1)
            self.sprite.x += ret[0] * self.speed
            self.sprite.y += ret[1] * self.speed

    def build_character(self, base):
        self.sprite = pyglet.sprite.Sprite(base['sprite'], base['coord'][0], base['coord'][1], batch=gfx_batch) # noqa
        self.collision = SpriteCollision(self.sprite)
        self.kbr = base['kbr']

        self.max_health = base['health']
        self.health = base['health']
        self.base_speed = base['speed']
        self.speed = base['speed']
        self.load_guns(base['guns'])
