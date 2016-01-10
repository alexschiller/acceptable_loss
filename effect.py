from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
from character import * # noqa
import pyglet
from gun import * # noqa

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

    def blood(self, start_x, start_y, size_min=1, size_max=5):
        for e in range(random.randint(size_min, size_max)):
            self.effects.append(
                Effect(start_x=start_x, start_y=start_y,
                    vel_x=random.randint(-20, 20), vel_y=random.randint(-20, 20),
                    travel=15,
                    ecolor=[255, 10, 10],
                    esizex=4, esizey=4,)
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
