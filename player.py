from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa

player_base = {
    'sprite': load_image('dreadnaught.png'),
    'coord': [window_width / 2, window_height / 2],
    'kbr': 50,
    'health': 100,
    'speed': 3,
    'guns': [Shrap(master, hits='enemies', base=red_laser)],
}


class Player(Character):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        self.build_character(kwargs['base'])

        # Player specific defaults
        self.max_energy = 100
        self.energy = 100

        self.max_shield = 10
        self.shield = 10

    def on_hit(self, bullet):
        self.shield -= bullet.damage
        if self.shield < 0:
            self.health += self.shield
            self.shield = 0
        self.spriteeffect.blood(bullet.sprite.x, bullet.sprite.y, 3, 5)
        impact = bullet.knockback / self.kbr
        self.master.move_player(bullet.vel_x * impact, bullet.vel_y * impact)

    def check_object_collision(self, o):
        if collide(self.collision, o.collision):
            ret = calc_vel_xy(self.sprite.x, self.sprite.y,
            o.sprite.x, o.sprite.y, self.speed + 1)
            self.master.move_player(ret[0], ret[1])

    def update(self):
        # if self.shield < self.max_shield:
        #     self.shield += .001
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        if self.energy < 100:
            self.energy += 1

        if self.shield < self.max_shield:
            self.shield += .016

        sw = int(max(200 * self.shield / self.max_shield, 1))
        hw = int(max(200 * self.health / self.max_health, 1))
        ew = int(max(200 * self.energy / self.max_energy, 1))

        self.shield_bar = pyglet.sprite.Sprite(
            pyglet.image.create(sw, 10, green_sprite),
            20, window_height - 20, batch=BarBatch)

        self.health_bar = pyglet.sprite.Sprite(
            pyglet.image.create(hw, 10, red_sprite),
            20, window_height - 40, batch=BarBatch)

        self.energy_bar = pyglet.sprite.Sprite(
            pyglet.image.create(ew, 10, blue_sprite),
            20, window_height - 60, batch=BarBatch)
