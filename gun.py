from pyglet.gl import * # noqa
from collide import * # noqa
import random
from utility import * # noqa
import pyglet
# import math
# import itertools
from collide import * # noqa


class Bullet(object):
    def __init__(self, base, start_x, start_y, target_x, target_y, chits=[]):
        # Base stats
        self.base = base
        self.damage = self.base['damage']
        self.travel = self.base['travel']
        self.velocity = self.base['velocity']
        self.spread = self.base['spread']
        self.accuracy = self.base['accuracy']
        self.knockback = self.base['knockback']
        self.pierce = self.base['pierce']

        x_dist = target_x - float(start_x)
        y_dist = target_y - float(start_y)

        self.calc_acc = float(1 - self.accuracy) * self.velocity
        self.calc_travel = self.travel - random.randint(
            0, int(float(1 - self.accuracy) * self.travel)
        )
        # Updated Stats
        self.travelled = 0
        self.sprite = pyglet.sprite.Sprite(base['image'],
            start_x, start_y, batch=BulletBatch)
        self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90
        self.sprite.scale = 1
        self.collision = SpriteCollision(self.sprite)
        # compute directions

        ret = calc_vel_xy(target_x, target_y,
            start_x, start_y, self.velocity)

        self.vel_x = ret[0] + (random.gauss(0, self.spread) * self.velocity)
        self.vel_y = ret[1] + (random.gauss(0, self.spread) * self.velocity)


class Gun(object):
    def __init__(self, enemy, base, pistol=None, chips=[]): # noqa
        self.enemy = enemy
        self.rof = 60 / base['rof']
        self.rofl = 0
        self.bullets = []
        self.base = base
        self.pistol = pistol
        self.energy_cost = base['energy_cost']
        self.gun_fire_sound = base['gun_fire_sound']
        self.on_hit_sound = base['on_hit_sound']
        print self.gun_fire_sound
        print self.on_hit_sound

    def fire(self, start_x, start_y, target_x, target_y):
        if self.rofl == self.rof:
            self.rofl -= self.rof
        # if len(self.bullets) > 30 or player.energy < self.energy_cost:
            # return True
        # player.energy -= self.energy_cost
            play_sound(self.gun_fire_sound)
            for b in range(self.base['bullets']):
                self.bullets.append(Bullet(self.base, start_x, start_y, target_x, target_y)) # noqa
            return True

    def delete_bullet(self, bullet):
        if self.base['special']:
            ret = self.select_target(bullet)
            if random.randint(1, 10) != 1:
                self.fire(bullet.sprite.x, bullet.sprite.y, ret[0], ret[1])
        try:
            bullet.sprite.delete()
            self.bullets.remove(bullet)
        except:
            pass

    def update(self):
        if self.rofl < self.rof:
            self.rofl += 1
        for bullet in self.bullets:
            # bullet.sprite.rotation += 10
            bullet.sprite.x += bullet.vel_x
            bullet.sprite.y += bullet.vel_y
            bullet.travelled = bullet.travelled + abs(bullet.vel_x) + abs(bullet.vel_y)
            try:
                for e in self.enemy:
                    if collide(bullet.collision, e.collision):
                        play_sound(self.on_hit_sound)
                        e.on_hit(bullet)
                        bullet.pierce -= 1
                        if bullet.pierce < 0:
                            self.delete_bullet(bullet)
                    # if bullet.check_collision(e):
                        # if not bullet.handle_collision():

                        break
                    # self.delete_bullet(bullet)
            except:
                if collide(bullet.collision, self.enemy.collision):
                    play_sound(self.on_hit_sound)
                    self.enemy.on_hit(bullet)
                    bullet.pierce -= 1
                    if bullet.pierce < 0:
                        self.delete_bullet(bullet)
                # if bullet.check_collision(e):
                    # if not bullet.handle_collision():

                    break
            if bullet.travelled > bullet.calc_travel:
                self.delete_bullet(bullet)

    def select_target(self, bullet):
        try:
            min_dist = float("inf")
            coord = (0, 0)
            x1 = bullet.sprite.x
            y1 = bullet.sprite.x
            for e in self.enemy:
                dist = (e.sprite.x - x1) ** 2 + (e.sprite.y - y1) ** 2
                if dist < min_dist:
                    min_dist = dist
                    coord = (e.sprite.x, e.sprite.y)
            return coord
        except:
            return [bullet.sprite.x, bullet.sprite.y]

class GrenadeEffect(object):
    def __init__(self, start_x, start_y, vel_x, vel_y, travel=20, ecolor=[0, 0, 0], esizex=3, esizey=3,shadow=0): # noqa
        if vel_x == 0 and vel_y == 0:
            vel_x, vel_y = 5, 10
        effect_color = pyglet.image.SolidColorImagePattern(color=(ecolor[0],
            ecolor[1], ecolor[2], 255))
        effect_shape = pyglet.image.create(esizex, esizey, effect_color)

        self.sprite = pyglet.sprite.Sprite(effect_shape,
        start_x, start_y, batch=EffectsBatch)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.travel = travel
        self.travelled = 0
        self.shadow = shadow

class Grenade(object):
    def __init__(self):
        self.effects = []
        self.grenades = 1

    def update(self):
        if self.grenades < 1:
            self.grenades += .01
        for effect in self.effects:
            effect.sprite.x += effect.vel_x
            effect.sprite.y += effect.vel_y
            perc_trav = effect.travelled / effect.travel
            if not effect.shadow:
                if perc_trav < .5:
                    effect.sprite.scale += .2
                else:
                    effect.sprite.scale -= .2

            effect.travelled = effect.travelled + abs(effect.vel_x) + abs(effect.vel_y)
            if effect.travelled > effect.travel:
                effect.sprite.delete()
                self.effects.remove(effect)

    def throw(self, start_x, start_y, target_x, target_y):
        if self.grenades >= 1:
            self.grenades -= 1
            ret = calc_vel_xy(target_x, target_y, start_x, start_y, 10)
            travel = abs(target_x - start_x) + abs(target_y - start_y)
            self.effects.append(
                GrenadeEffect(start_x=start_x, start_y=start_y,
                    vel_x=ret[0], vel_y=ret[1],
                    travel=travel,
                    ecolor=[random.randint(0, 255), random.randint(0, 255),
                        random.randint(0, 255)],
                    esizex=3, esizey=3, shadow=0)
            )
            # self.effects.append(
            #     GrenadeEffect(start_x=start_x, start_y=start_y,
            #         vel_x=ret[0], vel_y=ret[1],
            #         travel=travel,
            #         ecolor=[150, 150, 150],
            #         esizex=10, esizey=10, shadow=1)
            # )

# Prefab guns for now, belong elsewhere
shotgun = {
    'damage': 1,
    'travel': 300,
    'velocity': 4,
    'accuracy': .85,
    'spread': .10,
    'energy_cost': 20,
    'bullets': 50,
    'pierce': 0,
    'rof': 1,
    'knockback': 20.0,
    'image': load_image('shotgun.png'),
    'recoil': 10,
    'special': None,
    'gun_fire_sound': load_sound('shotgun.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}

exgun = {
    'damage': 5,
    'travel': 100,
    'velocity': 15,
    'accuracy': .85,
    'spread': 0,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 0,
    'rof': 6000,
    'knockback': 1.0,
    'image': load_image('ex.png'),
    'recoil': 1,
    'special': False,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}

stargun = {
    'damage': 5,
    'travel': 700,
    'velocity': 15,
    'accuracy': .85,
    'spread': .01,
    'energy_cost': 20,
    'bullets': 3,
    'pierce': 0,
    'rof': 2,
    'knockback': 1.0,
    'image': load_image('star.png'),
    'recoil': 1,
    'special': None,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}

lineshot = {
    'damage': 1,
    'travel': 300,
    'velocity': 10,
    'accuracy': .85,
    'spread': .10,
    'energy_cost': 20,
    'bullets': 50,
    'pierce': 0,
    'rof': 1,
    'knockback': 20.0,
    'image': load_image('lineshot.png'),
    'recoil': 10,
    'special': None,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}

red_laser = {
    'damage': 1,
    'travel': 600,
    'velocity': 10,
    'accuracy': .85,
    'spread': .02,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 0,
    'rof': 60,
    'knockback': 10.0,
    'image': load_image('red_laser.png'),
    'recoil': 1,
    'special': None,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}


slimegun = {
    'damage': 1,
    'travel': 300,
    'velocity': 8,
    'accuracy': .85,
    'spread': .3,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 20,
    'rof': 10,
    'knockback': 10.0,
    'image': load_image('slimeball.png'),
    'recoil': 10,
    'special': None,
    'gun_fire_sound': None,
    'on_hit_sound': load_sound('on_hit.wav'),
}

tracker = {
    'damage': 1,
    'travel': 300,
    'velocity': 10,
    'accuracy': .85,
    'spread': .15,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 99,
    'rof': 99,
    'knockback': 0.0,
    'image': load_image('tracker.png'),
    'recoil': 0,
    'special': True,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}
