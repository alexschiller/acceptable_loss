from pyglet.gl import * # noqa
from collide import * # noqa
import random
from utility import * # noqa
import pyglet
import math
import itertools
from gun import * # noqa

class Character(object):
    def __init__(self, sprite, coord, scale, x, y, health):
        self.sprite = pyglet.sprite.Sprite(sprite, coord[0], coord[1], batch=gfx_batch)
        self.sprite.scale = scale
        self.collision = SpriteCollision(self.sprite)
        self.x = x
        self.y = y
        self.kbr = 50

        self.max_health = health
        self.health = health
        self.base_speed = 1
        self.speed = 1

    def move(self, x, y):
        self.sprite.x += (self.speed * x)
        self.sprite.y += (self.speed * y)


class Player(Character):
    def __init__(self, master):
        super(Player, self).__init__(load_image('dreadnaught.png'),
            [50, 50], 1, 4, 4, 100)
        self.master = master
        self.max_energy = 100
        self.energy = 100
        self.spriteeffect = master.spriteeffect
        self.vel_x = 0
        self.vel_y = 0
        self.max_shield = 100
        self.shield = 100
        #movement

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

    def update(self):
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        if self.energy < 100:
            self.energy += 1
        self.shield_bar = pyglet.sprite.Sprite(
            pyglet.image.create(200 * self.shield / self.max_shield, 10, green_sprite),
            20, window_height - 20, batch=BarBatch)

        self.health_bar = pyglet.sprite.Sprite(
            pyglet.image.create(200 * self.health / self.max_health, 10, red_sprite),
            20, window_height - 40, batch=BarBatch)

        self.energy_bar = pyglet.sprite.Sprite(
            pyglet.image.create(200 * self.energy / self.max_energy, 10, blue_sprite),
            20, window_height - 60, batch=BarBatch)

    def on_hit(self, bullet):
        self.health -= bullet.damage
        self.spriteeffect.blood(bullet.sprite.x, bullet.sprite.y, 3, 5)
        impact = bullet.knockback / self.kbr
        self.sprite.x += bullet.vel_x * impact
        self.sprite.y += bullet.vel_y * impact

    def next_gun(self):
        self.gun = self.guns[next(self.cycle_guns)]

    def fire(self, target_x, target_y):
        self.gun.fire(self.sprite.x, self.sprite.y, target_x, target_y)

    def load_guns(self, guns):
        self.guns = guns
        self.cycle_guns = itertools.cycle(range(len(self.guns)))
        self.gun = self.guns[0]


class Ally(Character):
    def __init__(self, master, gun):
        self.gun = gun
        self.player = master.player
        self.enemy = master.enemies
        self.spriteeffect = master.spriteeffect

        coord = [random.randint(-500, 500) + 50, random.randint(-300, 300) + 50]
        super(Ally, self).__init__(load_image('dreadnaught.png'), coord, 1, 4, 4, 100)

    def update(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, self.speed)
        if abs(self.sprite.x - self.player.sprite.x) + abs(
                self.sprite.y - self.player.sprite.y) > 50:
                self.sprite.x += ret[0]
                self.sprite.y += ret[1]

        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()
        if random.randint(0, 200) >= 190:
            coord = self.select_target()
            gun.fire(self.sprite.x, self.sprite.y, coord[0], coord[1])

    def select_target(self):
        min_dist = 9999999999
        coord = (0, 0)
        x1 = self.sprite.x
        y1 = self.sprite.x
        for e in enemy:
            dist = (e.sprite.x - x1) ** 2 + (e.sprite.y - y1) ** 2
            if dist < min_dist:
                min_dist = dist
                coord = (e.sprite.x, e.sprite.y)
        return coord

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 10)
        self.sprite.x -= ret[0] / 2
        self.sprite.y -= ret[1] / 2
        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]


class Cannon(Ally):
    def __init__(self, master, gun):
        self.spriteeffect = master.spriteeffect

        super(Cannon, self).__init__(master, gun)
        self.sprite = pyglet.sprite.Sprite(load_image('cannon.png'),
            int(700) + random.randint(-600, 600), int(400) + random.randint(-400, 400),
            batch=gfx_batch)
        self.speed = 0
        self.collision = SpriteCollision(self.sprite)
        self.health = 100
        self.max_health = 100

    def update(self):
        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()
        if random.randint(0, 200) >= 190:

            coord = self.select_target()
            x_dist = coord[0] - float(self.sprite.x)
            y_dist = coord[1] - float(self.sprite.y)
            self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1)
            self.gun.fire(self.sprite.x, self.sprite.y, coord[0], coord[1])
            # self.spriteeffect.smoke(self.sprite.x, self.sprite.y, coord[0], coord[1])

    def select_target(self):
        min_dist = float("inf")
        coord = (0, 0)
        x1 = self.sprite.x
        y1 = self.sprite.x
        for e in self.enemy:
            dist = (e.sprite.x - x1) ** 2 + (e.sprite.y - y1) ** 2
            if dist < min_dist:
                min_dist = dist
                coord = (e.sprite.x, e.sprite.y)
        return coord

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 2)
        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]


class Healer(Ally):
    def __init__(self, master, gun):
        super(Healer, self).__init__(master, gun)
        # self.master = master
        self.spriteeffect = master.spriteeffect
        self.enemy = master.enemies
        self.player = master.player

        self.sprite = pyglet.sprite.Sprite(load_image('healer.png'),
            int(self.player.sprite.x) + 50,
            int(self.player.sprite.y) + 50, batch=gfx_batch)
        self.speed = 1
        self.collision = SpriteCollision(self.sprite)
        self.health = 100
        self.max_health = 100

    def update(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, self.speed)
        if abs(self.sprite.x - self.player.sprite.x) + abs(
                self.sprite.y - self.player.sprite.y) > 50:
                self.sprite.x += ret[0]
                self.sprite.y += ret[1]

        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()
        if self.player.health < self.player.max_health:
            dist = math.sqrt(
                (self.player.sprite.x - self.sprite.x) ** 2 + (
                    self.player.sprite.y - self.sprite.y) ** 2)
            if dist <= 100:
                self.spriteeffect.heal(self.sprite.x, self.sprite.y,
                    self.player.sprite.x, self.player.sprite.y)
                self.player.health += 1

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 10)
        self.sprite.x -= ret[0] / 2
        self.sprite.y -= ret[1] / 2
        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]


class Enemy(object):
    def __init__(self, master, gun):
        self.enemy = master.enemies
        self.player = master.player
        self.spriteeffect = master.spriteeffect
        self.sprite = pyglet.sprite.Sprite(load_image('big_slime.png'),
            random.randint(50, 1350), random.randint(50, 750), batch=gfx_batch)
        self.touch_damage = 10
        self.health = 100
        self.max_health = 100.0
        self.sprite.scale = 1
        self.gun = gun

        # self.sprite.rotation = random.randint(0, 360)
        self.kbr = 100

        #movement
        self.speed = 2
        self.collision = SpriteCollision(self.sprite)
        anim = []
        anim += ([0] * random.randint(10, 30)) + ([2] * random.randint(25, 50))

        self.animation = itertools.cycle(anim)

    def on_death(self):
        self.enemy.append(Enemy(master, self.gun))
        self.spriteeffect.explosion(self.sprite.x, self.sprite.y, 30, 50)
        try:
            self.sprite.delete()
            self.enemy.remove(self)
        except:
            pass

    def shoot(self):
        self.gun.fire(self.sprite.x, self.sprite.y,
        self.player.sprite.x, self.player.sprite.y)

    def on_hit(self, bullet):
        self.spriteeffect.explosion(bullet.sprite.x, bullet.sprite.y, 3, 5)
        impact = bullet.knockback / self.kbr
        self.sprite.x += bullet.vel_x * impact
        self.sprite.y += bullet.vel_y * impact
        self.health -= bullet.damage
        self.sprite.scale = (self.health / self.max_health * .5) + .5

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 20)
        self.sprite.x -= ret[0] / 2
        self.sprite.y -= ret[1] / 2
        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]
        # self.player.health -= self.touch_damage

    def update(self):

        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
            self.sprite.x, self.sprite.y, self.speed)
        self.speed = next(self.animation)
        self.sprite.x += ret[0]
        self.sprite.y += ret[1]
        if random.randint(0, 300) > 270:
            self.shoot()
        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()

class Soldier(object):
    def __init__(self, master, gun):
        self.enemy = master.enemies
        self.player = master.player
        self.master = master
        self.spriteeffect = master.spriteeffect
        self.sprite = pyglet.sprite.Sprite(load_image('soldier.png'),
            random.randint(50, 1350), random.randint(50, 750), batch=gfx_batch)
        self.touch_damage = 0
        self.health = 10
        self.max_health = 10
        self.sprite.scale = 1
        self.gun = gun

        # self.sprite.rotation = random.randint(0, 360)
        self.kbr = 50
        self.spriteeffect.teleport(self.sprite.x, self.sprite.y, 5, 5)
        #movement
        self.speed = .5
        self.collision = SpriteCollision(self.sprite)
        # anim = []
        # anim += ([0] * random.randint(10, 30)) + ([2] * random.randint(25, 50))

        # self.animation = itertools.cycle(anim)

    def on_death(self):
        self.enemy.append(Soldier(master, self.gun))
        self.spriteeffect.blood(self.sprite.x, self.sprite.y, 30, 50)
        try:
            self.sprite.delete()
            self.enemy.remove(self)
        except:
            pass

    def shoot(self):
        self.gun.fire(self.sprite.x, self.sprite.y,
        self.player.sprite.x, self.player.sprite.y)

    def on_hit(self, bullet):
        self.spriteeffect.blood(bullet.sprite.x, bullet.sprite.y, 3, 5)
        impact = bullet.knockback / self.kbr
        self.sprite.x += bullet.vel_x * impact
        self.sprite.y += bullet.vel_y * impact
        self.health -= bullet.damage
        # self.sprite.scale = (self.health / self.max_health * .5) + .5

    def on_collide(self):
        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        self.sprite.x, self.sprite.y, 10)
        self.sprite.x -= ret[0] * 2
        self.sprite.y -= ret[1] * 2
        self.player.sprite.x += ret[0]
        self.player.sprite.y += ret[1]
        self.health -= 10

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

    def update(self):
        try:
            self.check_object_collision(self.closest_object())
        except:
            pass

        x_dist = self.player.sprite.x - float(self.sprite.x)
        y_dist = self.player.sprite.y - float(self.sprite.y)
        self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

        ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
            self.sprite.x, self.sprite.y, self.speed)
        self.speed = .5
        self.sprite.x += ret[0]
        self.sprite.y += ret[1]
        if random.randint(0, 300) > 270:
            self.shoot()
        if collide(self.collision, self.player.collision):
            self.on_collide()
        if self.health <= 0:
            self.on_death()

class Box(object):
    def __init__(self, master):
        self.sprite = pyglet.sprite.Sprite(load_image('box.png'),
            random.randint(50, 1350), random.randint(50, 750), batch=gfx_batch)
        self.collision = SpriteCollision(self.sprite)
        self.health = 1000
        self.max_health = 1000.0

    # def on_death(self):
    #     self.enemy.append(Enemy(master, self.gun))
    #     self.spriteeffect.explosion(self.sprite.x, self.sprite.y, 30, 50)
    #     try:
    #         self.sprite.delete()
    #         self.enemy.remove(self)
    #     except:
    #         pass

    # def on_hit(self, bullet):
    #     self.spriteeffect.explosion(bullet.sprite.x, bullet.sprite.y, 3, 5)
        # self.sprite.scale = (self.health / self.max_health * .5) + .5

    # def on_collide(self):
    #     pass
        # ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
        # self.sprite.x, self.sprite.y, 20)
        # self.sprite.x -= ret[0] / 2
        # self.sprite.y -= ret[1] / 2
        # self.player.sprite.x += ret[0]
        # self.player.sprite.y += ret[1]
        # self.player.health -= self.touch_damage

    # def update(self):

    #     ret = calc_vel_xy(self.player.sprite.x, self.player.sprite.y,
    #         self.sprite.x, self.sprite.y, self.speed)
    #     self.speed = next(self.animation)
    #     self.sprite.x += ret[0]
    #     self.sprite.y += ret[1]
    #     if random.randint(0, 300) > 270:
    #         self.shoot()
    #     if collide(self.collision, self.player.collision):
    #         self.on_collide()
    #     if self.health <= 0:
    #         self.on_death()

class Effect(object):
    def __init__(self, start_x, start_y, vel_x, vel_y, travel=20, ecolor=[0, 0, 0], esizex=3, esizey=3): # noqa
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


class SpriteEffect(object):
    def __init__(self, master):
        self.effects = []
        self.master = master

    def update(self):
        for effect in self.effects:
            effect.sprite.x += effect.vel_x
            effect.sprite.y += effect.vel_y
            effect.sprite.rotation += random.randint(0, 5)
            effect.travelled = effect.travelled + abs(effect.vel_x) + abs(effect.vel_y)
            if effect.travelled > effect.travel:
                effect.sprite.delete()
                self.effects.remove(effect)

    def heal(self, start_x, start_y, target_x, target_y, travel=50):
        ret = calc_vel_xy(target_x, target_y, start_x, start_y, 10)
        for e in range(3):
            self.effects.append(
                Effect(start_x=start_x, start_y=start_y,
                    vel_x=ret[0], vel_y=ret[1],
                    travel=travel,
                    ecolor=[random.randint(100, 255), random.randint(0, 55),
                        random.randint(0, 55)],
                    esizex=random.randint(1, 10), esizey=random.randint(1, 10))
            )

    def explosion(self, start_x, start_y, size_min=10, size_max=10):
        for e in range(random.randint(size_min, size_max)):
            self.effects.append(
                Effect(start_x=start_x, start_y=start_y,
                    vel_x=random.randint(-20, 20), vel_y=random.randint(-20, 20),
                    travel=random.randint(30, 50),
                    ecolor=[random.randint(0, 55), random.randint(100, 255),
                        random.randint(0, 55)],
                    esizex=random.randint(1, 10), esizey=random.randint(1, 10))
            )

    def blood(self, start_x, start_y, size_min=5, size_max=5):
        for e in range(random.randint(size_min, size_max)):
            self.effects.append(
                Effect(start_x=start_x, start_y=start_y,
                    vel_x=random.randint(-20, 20), vel_y=random.randint(-20, 20),
                    travel=15,
                    ecolor=[random.randint(100, 255), random.randint(0, 55),
                        random.randint(0, 55)],
                    esizex=random.randint(1, 10), esizey=random.randint(1, 10))
            )

    def smoke(self, start_x, start_y, target_x, target_y):
        ret = calc_vel_xy(target_x, target_y, start_x, start_y, 5)
        for e in range(20):
            color = random.randint(0, 255)
            self.effects.append(
                Effect(start_x=start_x, start_y=start_y,
                    vel_x=ret[0] + random.randint(-2, 2),
                    vel_y=ret[1] + random.randint(-2, 2),
                    travel=100 + random.randint(25, 50),
                    ecolor=[color, color, color],
                    esizex=random.randint(1, 10), esizey=random.randint(1, 10))
            )

    def teleport(self, start_x, start_y, size_min=10, size_max=10):
        play_sound(load_sound('teleport.wav'))
        for e in range(random.randint(size_min, size_max)):
            self.effects.append(
                Effect(start_x=start_x, start_y=start_y,
                    vel_x=random.randint(-20, 20), vel_y=random.randint(-20, 20),
                    travel=random.randint(30, 50),
                    ecolor=[random.randint(0, 50), random.randint(50, 100),
                        random.randint(100, 255)],
                    esizex=random.randint(1, 10), esizey=random.randint(1, 10))
            )
