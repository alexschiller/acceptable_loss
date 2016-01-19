from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa
from functools import partial # noqa
from ability import * # noqa
# import random

class BolaEffect(object):
    def __init__(self, master, owner, start_x, start_y, target_x, target_y): # noqa
        self.sprite = pyglet.sprite.Sprite(load_image('bola.png'), start_x, start_y, batch=gfx_batch) # noqa
        self.travel = 200 + random.randint(-50, 50)
        self.master = master
        self.owner = owner
        self.target_x = target_x
        self.target_y = target_y
        self.start_x = start_x
        self.start_y = start_y
        ret = calc_vel_xy(target_x, target_y,
            start_x, start_y, random.randint(7, 10))

        self.vel_x = ret[0] + random.randint(-2, 2)
        self.vel_y = ret[1] + random.randint(-2, 2)

        self.travelled = 0

    def remove_bola(self):
        self.master.spriteeffect.bola_explosion(self.sprite.x, self.sprite.y)
        try:
            self.sprite.delete()
            self.owner.thrown.remove(self)
        except:
            pass

    def get_target(self):
        try:
            min_dist = 300  # must be within 300 of the bola
            x1 = self.sprite.x
            y1 = self.sprite.y
            self.target = None
            for e in self.owner.owner.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    self.target = e
            return min_dist
        except:
            self.target = None

    def shoot(self):
        enemy_range = self.get_target()
        if self.target:
            bullet_base = self.owner.build_bullet(
                self.owner.gun_one,
                self.sprite.x,
                self.sprite.y,
                self.target.sprite.x,
                self.target.sprite.y,
                enemy_range,
                self.target,)
            bullet_base['damage']
            bullet_base['image'] = self.owner.plasma_shot
            self.owner.thrown.append(Thrown(self.master, self.owner, bullet_base))
        self.remove_bola()

    def update(self):
        self.sprite.rotation += 5
        try:
            self.sprite.x += self.vel_x
            self.sprite.y += self.vel_y
            self.travelled += math.hypot(self.vel_x, self.vel_y)
            if self.travelled > self.travel:
                self.shoot()
        except:
            pass

class SpectreAbility(Ability):
    def __init__(self, *args, **kwargs):
        super(SpectreAbility, self).__init__(*args, **kwargs)
        self.opp = 50
        self.vul = 50
        self.opp_max = 100
        self.vul_max = 100

        self.vat = pyglet.sprite.Sprite(load_image('opp_vul_bar.png', anchor=False), window_width-472, 0, batch=gfx_batch),  # noqa
        # self.plasma_shot = load_image('bola_shot.png')
        # self.bushwhack_shot = load_image('bushwhack_shot.png')

    def update(self):
        self.update_delayed()
        # self.update_plasma()

        for t in self.thrown:
            t.update()

        oh = int(max(115 * self.opp / self.opp_max, 1))
        self.opp_bar = pyglet.sprite.Sprite(
            pyglet.image.create(15, oh, red_sprite),
            window_width - 468, 5, batch=BarBatch)

        vh = int(max(115 * self.vul / self.vul_max, 1))
        self.vul_bar = pyglet.sprite.Sprite(
            pyglet.image.create(15, vh, white_sprite),
            window_width - 433, 5, batch=BarBatch)

    # def action_checks(self, plasma):
    #     if self.owner.target:
    #         if not self.global_cooldown:
    #             if self.plasma >= plasma:
    #                 return True
    #     return False

    # def update_plasma(self):
    #     if self.plasma < self.max_plasma:
    #         self.plasma += .3 * self.plasma / self.max_plasma + .05
    #     else:
    #         self.plasma = self.max_plasma

    def enemy_in_range(self, enemy, gun):
            dist_x = self.owner.sprite.x - enemy.sprite.x
            dist_y = self.owner.sprite.y - enemy.sprite.y
            dist = math.hypot(dist_x, dist_y)
            if dist < gun['travel']:
                return dist
            return False

    def add_bullet(self, bullet_base):
        self.thrown.append(Thrown(master, self, bullet_base))

    # def magnum_double_tap(self):
    #     if self.action_checks(10):
    #         enemy_range = self.can_ability_shoot(self.gun_one)
    #         if enemy_range:
    #             bullet_base = self.build_bullet(
    #                 self.gun_one,
    #                 self.owner.sprite.x,
    #                 self.owner.sprite.y,
    #                 self.owner.target.sprite.x,
    #                 self.owner.target.sprite.y,
    #                 enemy_range,
    #                 self.owner.target,)
    #             bullet_base['image'] = self.plasma_shot
    #             self.add_bullet(bullet_base)
    #             self.delayed.append([5, partial(self.add_bullet, bullet_base)])
    #             self.trigger_global_cooldown()
    #             self.plasma -= 10

    # def magnum_five_beans_in_the_wheel(self):
    #     if self.action_checks(10):
    #         enemy_range = self.can_ability_shoot(self.gun_one)
    #         if enemy_range:
    #             bullet_base = self.build_bullet(
    #                 self.gun_two,
    #                 self.owner.sprite.x,
    #                 self.owner.sprite.y,
    #                 self.owner.target.sprite.x,
    #                 self.owner.target.sprite.y,
    #                 enemy_range,
    #                 self.owner.target,)
    #             bullet_base['damage'] *= .5
    #             bullet_base['image'] = self.bushwhack_shot
    #             self.owner.stats.temp_stat_change(180, 'health_regen', bullet_base['damage']) # noqa
    #             self.thrown.append(Thrown(master, self, bullet_base))
    #             self.trigger_global_cooldown()
    #             self.plasma -= 10

    # def magnum_california_prayer_book(self):
    #     if self.action_checks(5):
    #         keep_going = 1
    #         keep_count = 0
    #         while keep_going:
    #             if random.choice([1, 1, 1, 0]):
    #                 self.thrown.append(
    #                     BolaEffect(self.master, self, self.owner.sprite.x,
    #                         self.owner.sprite.y, self.owner.target.sprite.x,
    #                         self.owner.target.sprite.y,)
    #                 )
    #                 keep_count += 1
    #             else:
    #                 keep_going = 0
    #         self.master.spriteeffect.message(self.owner.sprite.x, self.owner.sprite.y, 'shot: ' + str(keep_count), time=90) # noqa                    
    #         self.trigger_global_cooldown()
    #         self.plasma -= 5

    # def carbine_bushwhack(self):
    #     if self.action_checks(10):
    #         enemy_range = self.can_ability_shoot(self.gun_two)
    #         if enemy_range:
    #             bullet_base = self.build_bullet(
    #                 self.gun_two,
    #                 self.owner.sprite.x,
    #                 self.owner.sprite.y,
    #                 self.owner.target.sprite.x,
    #                 self.owner.target.sprite.y,
    #                 enemy_range,
    #                 self.owner.target,)
    #             bullet_base['damage'] *= 1.9
    #             bullet_base['image'] = self.bushwhack_shot
    #             self.thrown.append(Thrown(master, self, bullet_base))
    #             self.trigger_global_cooldown()
    #             self.plasma -= 10

    # def carbine_crackerjack(self):
    #     if not self.global_cooldown and self.plasma >= 10:
    #         for e in self.owner.enemies:
    #             enemy_range = self.enemy_in_range(e, self.gun_two)
    #             if enemy_range:
    #                 bullet_base = self.build_bullet(
    #                     self.gun_two,
    #                     self.owner.sprite.x,
    #                     self.owner.sprite.y,
    #                     e.sprite.x,
    #                     e.sprite.y,
    #                     enemy_range,
    #                     e,)
    #                 bullet_base['damage']
    #                 bullet_base['image'] = self.bushwhack_shot
    #                 self.thrown.append(Thrown(master, self, bullet_base))
    #         self.trigger_global_cooldown()
    #         self.plasma -= 10
