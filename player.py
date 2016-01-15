from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa
from functools import partial # noqa

player_base = {
    'sprite': load_image('dreadnaught.png'),
    'coord': [window_width / 2, window_height / 2],
    'kbr': 50,
    'health': 100,
    'speed': 3,
    'guns': [Gun(master, base=pm_magnum)],
    'slot_one': AOEGun(master, base=rocket),
    'slot_two': Gun(master, base=sniper),
}

plasmaslinger_base = {
    'sprite': load_image('dreadnaught.png'),
    'coord': [window_width / 2, window_height / 2],
    'kbr': 50,
    'health': 100,
    'speed': 3,
    'guns': [Gun(master, base=pm_magnum)],
    'slot_one': AOEGun(master, base=rocket),
    'slot_two': Gun(master, base=sniper),
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
        self.blood_color = (30, 30, 30, 255)
        self.slot_one = kwargs['base']['slot_one']
        self.slot_two = kwargs['base']['slot_two']
        self.guns = [self.slot_one, self.slot_two]
        self.master.register_guns(self.guns)
        self.acc = 0
        self.evade = 0

    def update_evade(self, mx, my):
        if (abs(mx) + abs(my)) > 0:
            self.evade += .1
        else:
            self.evade -= .1
        if self.evade > 10:
            self.evade = 10
        elif self.evade <= 0:
            self.evade = 0
        self.acc = 10 - self.evade
        print self.evade, self.acc

    def slot_one_fire(self):
        if self.target:
            self.slot_one.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target) # noqa

    def slot_two_fire(self):
        if self.target:
            self.slot_two.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target) # noqa            

    def attack(self):
        if self.target:
            self.gun.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target) # noqa

    def on_hit(self, bullet):
        self.shield -= bullet.damage
        if self.shield < 0:
            self.health += self.shield
            self.shield = 0

        splatter = min(max(int(bullet.damage / self.max_health) * 10, 3), 50)
        self.spriteeffect.bullet_wound(bullet.vel_x, bullet.vel_y, self.sprite.x, self.sprite.y, splatter, self.blood_color) # noqa

    def fire_gun(self, gunnum):
        if self.target:
            self.guns[gunnum](self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self.acc, self.target) # noqa            

    def add_gun(self, gun):
        self.guns.append(gun)
        self.master.register_guns(gun)

    def check_object_collision(self, o):
        if collide(self.collision, o.collision):
            ret = calc_vel_xy(self.sprite.x, self.sprite.y,
            o.sprite.x, o.sprite.y, self.speed + 1) # noqa
            self.master.move_player(ret[0], ret[1])

    def move(self, mx, my):
        if mx and my:
            mx = mx / 1.41
            my = my / 1.41
        self.update_evade(mx, my)
        self.sprite.x += mx
        self.sprite.y += my

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
            pyglet.image.create(ew, 5, blue_sprite),
            20, window_height - 60, batch=BarBatch)
