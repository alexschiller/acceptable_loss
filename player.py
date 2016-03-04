from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
import itertools
from functools import partial # noqa
from controller import Controller
from plasmaslinger import * # noqa

class Player(Character):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        # self.visor = pyglet.sprite.Sprite(load_image('visor.png', anchor=False), -1, window_height-171, batch=gfx_batch),  # noqa
        self.energy = 100
        self.inventory = []

        self.jump_cycle = 0
        self.jump_cycle_direction = -1
        self.jumping = 0

        # self.shield_bar = pyglet.sprite.Sprite(pyglet.image.create(271, 13, blue_sprite),
            # 10, window_height - 25, batch=BarBatch) # noqa
        # self.hp_bar_len = int(window_width * .324)
        # self.health_bar = pyglet.sprite.Sprite(pyglet.image.create(int(window_width * .324), 30, red_sprite),
        #     20, 20, batch=gfx_batch) # noqa

        # self.ae_bar = pyglet.sprite.Sprite(
        #     pyglet.image.create(50, 13, white_sprite),
        #     31, window_height - 168, batch=BarBatch)

        # self.acc_bar = pyglet.sprite.Sprite(
        #     pyglet.image.create(3, 13, red_sprite),
        #     150, window_height - 168, batch=BarBatch)

        self.acc_mouse_bar_l = pyglet.sprite.Sprite(
            pyglet.image.create(20, 2, red_sprite),
            -50, -50, batch=BarBatch)

        self.acc_mouse_bar_r = pyglet.sprite.Sprite(
            pyglet.image.create(20, 2, red_sprite),
            -50, -50, batch=BarBatch)

        self.acc_mouse_bar_t = pyglet.sprite.Sprite(
            pyglet.image.create(2, 20, red_sprite),
            -50, -50, batch=BarBatch)

        self.acc_mouse_bar_b = pyglet.sprite.Sprite(
            pyglet.image.create(2, 20, red_sprite),
            -50, -50, batch=BarBatch)

    def mouse_target_distance(self):
        if self.target:
            dist = min(math.hypot(self.controller.sprite.x - self.target.sprite.x, self.controller.sprite.y - self.target.sprite.y), 300) # noqa
            mouse_mod = 1 - (dist / 300.0)
            return mouse_mod
        return 1

    def player_target_distance(self):
        if self.target:

            dist = math.hypot(self.sprite.x - self.target.sprite.x, self.sprite.y - self.target.sprite.y) # noqa

            gun_max = self.stats.gun_data['range_max']
            if dist > gun_max:
                return 1 - min(dist - gun_max, 300) / 300.0

            gun_min = self.stats.gun_data['range_min']
            if dist < gun_min:
                return 1 - min(gun_min - dist, 300) / 300.0
            return 1
        return 0

    def update_jump(self):
        if self.jumping:
            self.jump_cycle += self.jump_cycle_direction
            self.sprite.scale += .05 * self.jump_cycle_direction
        if self.jump_cycle >= 30:
            self.jump_cycle_direction = -2
        if self.jump_cycle < 0:
            self.sprite.scale = 1
            self.jump_cycle_direction = 1
            self.jump_cycle = 0
            self.jumping = 0
            self.master.spriteeffect.jump(self.sprite.x, self.sprite.y)

    def jump(self):
        if not self.jumping:
            self.jumping = 1

    def update_acc_mod(self):
        self.acc_mouse_mod = self.mouse_target_distance() * self.player_target_distance()

    def calc_acc(self):
        self.update_acc_mod()
        try:
            acc_val = 100 - min(int((self.stats.accuracy + self.stats.gun_data['accuracy']) * self.acc_mouse_mod), 100) # noqa
        except:
            return 0
        return acc_val

    def update_bars(self):
        self.hbubble.x = self.sprite.x
        self.hbubble.y = self.sprite.y
        self.hbubble.scale = max(1 - self.stats.health / (self.stats.health_max + .01), .01)

        self.sbubble.x = self.sprite.x
        self.sbubble.y = self.sprite.y
        self.sbubble.scale = max(1 - self.stats.shield / (self.stats.shield_max + .01), .01)
        if self.sbubble.scale >= .95:
            self.sbubble.scale = .01

        self.update_jump()
        if self.energy < 100:
            self.energy = 100

        # self.shield_bar.x = 10 - (271 - (self.stats.shield / float(self.stats.shield_max) * 271)) # noqa
        # self.health_bar.x = 20 - (self.hp_bar_len - (self.stats.health / float(self.stats.health_max) * self.hp_bar_len)) # noqa

        acc_val = self.calc_acc()
        x = self.controller.sprite.x
        y = self.controller.sprite.y
        self.acc_mouse_bar_l.x = x + acc_val + 3
        self.acc_mouse_bar_r.x = x - acc_val - 20
        self.acc_mouse_bar_l.y = y
        self.acc_mouse_bar_r.y = y

        self.acc_mouse_bar_t.x = x
        self.acc_mouse_bar_b.x = x
        self.acc_mouse_bar_t.y = y + acc_val + 3
        self.acc_mouse_bar_b.y = y - acc_val - 20

        # self.ae_bar.x = 31 + self.stats.evade_move / 10 * 50


class PlayerController(Controller):
    def __init__(self, *args, **kwargs):
        super(PlayerController, self).__init__(*args, **kwargs)
        self.master = master
        self.black_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 150))
        self.black_dot = pyglet.image.create(1, 1, self.black_sprite)
        self.sprite = pyglet.sprite.Sprite(self.black_dot, 0, 0, batch=gfx_batch)

        self.collision = SpriteCollision(self.sprite)
        red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
        self.red_dot = pyglet.image.create(5, 5, red_sprite)
        self.marker = None
        self.timg = load_image('target_round.png')
        self.move_target = None
        self.move_img = load_image('ex.png')

        self.time_to_speed = 30
        self.moving = 0

        self.breath_timer_base = 60
        self.breath_timer = 1
        self.breath = 0
        self.breath_cycle = itertools.cycle([-.0025, .0025])

        self.anim_rx = 0
        self.anim_ry = 0

    def on_hit(self):
        pass

    def build_target(self, e):
        self.marker = pyglet.sprite.Sprite(self.timg, e.sprite.x, e.sprite.y, batch=gfx_batch)  # noqa 

    def target_closest_enemy(self, distance=300):
        self.remove_target()
        try:
            min_dist = distance
            x1 = self.sprite.x
            y1 = self.sprite.y
            if len(self.puppet.enemies) == 0:
                return False
            for e in self.puppet.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    self.puppet.target = e
            if min_dist >= distance:
                self.remove_target()
        except:
            self.remove_target()

    def remove_target(self):
            self.puppet.target = None
            self.marker = None

    def move_to(self, x, y, scale):

        self.move_target = [x, y]
        self.mouse_target_sprite = pyglet.sprite.Sprite(self.move_img,
            x, y, batch=BarBatch) # noqa
        self.mouse_target_sprite.scale = scale

    def add_jitter(self):
        self.breath_timer -= 1
        if not self.breath_timer:
            self.anim_rx = (random.randint(-1, 1) / 10.0)
            self.anim_ry = (random.randint(-1, 1) / 10.0)
            self.breath = self.breath_cycle.next()
            self.breath_timer += self.breath_timer_base

        self.puppet.sprite.scale += self.breath
        self.puppet.sprite.x += self.anim_rx
        self.puppet.sprite.y += self.anim_ry

    def update_movement(self):
        if self.move_target:
            if self.moving < self.time_to_speed:
                self.moving += 1

            self.add_jitter()

            if self.mouse_target_sprite.scale < 1:
                self.mouse_target_sprite.scale += .05
            dist_x = float(self.move_target[0]) - self.puppet.sprite.x
            dist_y = float(self.move_target[1]) - self.puppet.sprite.y

            self.sprite.rotation = (math.degrees(math.atan2(dist_y, dist_x)) * -1) + 90
            self.sprite.scale = 1
            if abs(dist_x) + abs(dist_y) <= self.puppet.stats.speed:
                ret = calc_vel_xy(self.move_target[0], self.move_target[1],
                    self.puppet.sprite.x, self.puppet.sprite.y, abs(dist_x) + abs(dist_y))
            else:
                ret = calc_vel_xy(self.move_target[0], self.move_target[1],
                    self.puppet.sprite.x, self.puppet.sprite.y, self.puppet.stats.speed * self.moving / self.time_to_speed)

            self.last_mx = ret[0]
            self.last_my = ret[1]

            self.puppet.sprite.x += ret[0]
            self.puppet.sprite.y += ret[1]
            if abs(dist_x) + abs(dist_y) <= self.puppet.stats.speed:
                self.move_target = None
                self.mouse_target_sprite = None
        else:
            self.moving = 0

    def check_target(self):
        if self.puppet.target:
            try:
                self.build_target(self.puppet.target)
            except:
                self.remove_target()
        else:
            self.rotate(self.sprite.x, self.sprite.y)

    def update(self):
        self.update_movement()
        self.puppet.update_bars()
        self.target_closest_enemy()
        for p in self.master.loot.current_loot:
            self.master.loot.unpack_package(p)
        self.check_target()

def read_data(data):
    data['coord'] = [window_width / 2, window_height / 2]
    data['controller'] = PlayerController
    if data['class'] == 'plasmaslinger':
        data['skillset'] = plasmaslinger_skillset

    data['sprite'] = load_image(data['sprite'])
    data['gun']['image'] = load_image(data['gun']['image'])
    data['gun']['gun_fire_sound'] = load_sound(data['gun']['gun_fire_sound'])
    data['gun']['on_hit_sound'] = load_sound(data['gun']['on_hit_sound'])
    return data
