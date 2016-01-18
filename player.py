from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa
from functools import partial # noqa
from plasmaslinger import PlasmaslingerAbility

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
        self.hp_shield_bar = pyglet.sprite.Sprite(load_image('hp_shield.png', anchor=False), window_width - 1050, 0, batch=gfx_batch),  # noqa
        self.evade_acc_bar = pyglet.sprite.Sprite(load_image('evade_acc.png', anchor=False), window_width - 415, 0, batch=gfx_batch),  # noqa
        self.build_character(kwargs['base'])

        # Player specific defaults
        self.max_energy = 100
        self.energy = 100

        self.max_shield = 10
        self.shield = 10
        self.blood_color = (30, 30, 30, 255)
        self.gun_one = Gun(master, base=pm_magnum)
        self.gun_two = Gun(master, base=pm_carbine)

        self.guns = [self.gun_one, self.gun_two]
        self.gun = self.guns[1]

        self.master.register_guns(self.guns)
        self.acc = 0
        self.evade = 0

        self.ability = PlasmaslingerAbility(master, self, self.gun_one, self.gun_two)

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

    def slot_one_fire(self):
        self.ability.magnum_california_prayer_book()

    def slot_two_fire(self):
        self.ability.magnum_five_beans_in_the_wheel()

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
        self.sprite.x += mx * self.speed
        self.sprite.y += my * self.speed

    def update(self):
        self.ability.update()
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        if self.energy < 100:
            self.energy += 1

        if self.shield < self.max_shield:
            self.shield += .016

        sw = int(max(115 * self.shield / self.max_shield, 1))
        hw = int(max(115 * self.health / self.max_health, 1))
        ae = (window_width - 410) + self.evade / 10 * 70

        self.shield_bar = pyglet.sprite.Sprite(
            pyglet.image.create(sw, 15, blue_sprite),
            window_width - 1045, 30, batch=BarBatch)

        self.health_bar = pyglet.sprite.Sprite(
            pyglet.image.create(hw, 15, red_sprite),
            window_width - 1045, 5, batch=BarBatch)

        self.ae_bar = pyglet.sprite.Sprite(
            pyglet.image.create(70, 20, white_sprite),
            ae, 5, batch=BarBatch)
