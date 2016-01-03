from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet
from gun import * # noqa

class Character(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.spriteeffect = master.spriteeffect
        self.enemies = master.enemies
        self.player = master.player

    def move(self, x, y):
        self.sprite.x += (self.speed * x)
        self.sprite.y += (self.speed * y)

    def shoot(self, target_x, target_y):
        self.gun.fire(self.sprite.x, self.sprite.y, target_x, target_y)

    def build_character(self, base):
        self.sprite = pyglet.sprite.Sprite(base['sprite'], base['coord'][0], base['coord'][1], batch=gfx_batch) # noqa
        self.collision = SpriteCollision(self.sprite)
        self.kbr = base['kbr']

        self.max_health = base['health']
        self.health = base['health']
        self.base_speed = base['speed']
        self.speed = base['speed']

    def on_hit(self, bullet):
        self.health -= bullet.damage
        self.spriteeffect.blood(bullet.sprite.x, bullet.sprite.y, 3, 5)
        impact = bullet.knockback / self.kbr
        self.sprite.x += bullet.vel_x * impact
        self.sprite.y += bullet.vel_y * impact

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

    def check_object_collision(self, o):
        if collide(self.collision, o.collision):
            ret = calc_vel_xy(self.sprite.x, self.sprite.y,
            o.sprite.x, o.sprite.y, 3)
            self.sprite.x += ret[0]
            self.sprite.y += ret[1]
