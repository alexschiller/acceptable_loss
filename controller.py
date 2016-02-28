from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa

class Controller(object):
    def __init__(self, puppet):
        self.puppet = puppet
        self.last_my = 0
        self.last_mx = 0

    def move(self, mx, my):
        if mx and my:
            mx = mx / 1.41
            my = my / 1.41
        self.puppet.stats.update_move(mx, my)
        self.puppet.sprite.x += (self.puppet.stats.speed * mx)
        self.puppet.sprite.y += (self.puppet.stats.speed * my)
        self.last_my = mx
        self.last_mx = my
        self.move_target = None
        self.mouse_target_sprite = None

    def undo_move(self):
        self.move(-self.last_mx, -self.last_my)

    # Controls
    def rotate(self, x, y):
        x_dist = x - float(self.puppet.sprite.x)
        y_dist = y - float(self.puppet.sprite.y)
        self.puppet.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

    def attack(self):  # necessary?
        pass

    def slot_mouse_one_fire(self):
        pass

    def slot_mouse_two_fire(self):
        self.puppet.ability.slot_mouse_two_fire()

    def slot_one_fire(self):
        self.puppet.ability.slot_one_fire()

    def slot_two_fire(self):
        self.puppet.ability.slot_two_fire()

    def slot_three_fire(self):
        self.puppet.ability.slot_three_fire()

    def slot_four_fire(self):
        self.puppet.ability.slot_four_fire()

    def slot_q_fire(self):
        self.puppet.ability.slot_q_fire()

    def slot_e_fire(self):
        self.puppet.ability.slot_e_fire()

    def update(self):
        if self.puppet.target:
            self.rotate(self.puppet.target.sprite.x, self.puppet.target.sprite.y)
            if self.puppet.stats.gun_data['range_max'] > math.hypot(
                self.puppet.sprite.x - self.puppet.target.sprite.x,
                self.puppet.sprite.y - self.puppet.target.sprite.y
            ):
                self.slot_mouse_two_fire()
            else:
                ret = calc_vel_xy(self.puppet.target.sprite.x,
                    self.puppet.target.sprite.y,
                    self.puppet.sprite.x,
                    self.puppet.sprite.y,
                    1)
                self.move(ret[0], ret[1])

        else:
            self.target_closest_enemy()

    # AI Commands

    def on_hit(self):
        self.target_enemy()

    def target_enemy(self, distance=float("inf")):
        if not self.puppet.target:
            try:
                min_dist = distance
                x1 = self.puppet.sprite.x
                y1 = self.puppet.sprite.y
                if len(self.puppet.enemies) == 0:
                    return False
                for e in self.puppet.enemies:
                    dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                    if dist < min_dist:
                        min_dist = dist
                        self.puppet.target = e
                        for f in self.puppet.friends:
                            if not f.target:
                                if abs(math.hypot(x1 - f.sprite.x, y1 - f.sprite.y)) < 300: # noqa
                                    f.target = e
            except:
                self.puppet.target = None

    def target_closest_enemy(self):
        self.target_enemy(self.puppet.stats.gun_data['range_max'] + 50)

    def update_movement(self):
        if self.puppet.target:
            ret = calc_vel_xy(self.puppet.target.sprite.x, self.puppet.target.sprite.y,
                self.puppet.sprite.x, self.puppet.sprite.y, self.puppet.stats.speed)
            self.puppet.sprite.x += ret[0]
            self.puppet.sprite.y += ret[1]

    def update_attack(self):
        pass

        # if math.hypot(abs(self.puppet.sprite.x - self.puppet.target.sprite.x), abs(self.puppet.sprite.y - self.puppet.target.sprite.y)) < self.puppet.gun.travel: # noqa
        # self.attack()
