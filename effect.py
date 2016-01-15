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

class Text(object):
    def __init__(self, start_x, start_y, text, f_color, f_size): # noqa

        self.sprite = pyglet.text.Label(text, font_name='Sans Serif', color=f_color, font_size=f_size, x=start_x, y=start_y, anchor_x='left',anchor_y='center', batch=gfx_batch) # noqa        
        self.vel_x = random.randint(-2, 2)
        self.vel_y = random.randint(1, 2)
        self.travel = abs(self.vel_x) + abs(self.vel_y) * 30
        self.travelled = 0

class SpriteEffect(object):
    def __init__(self, master):
        self.effects = []
        self.master = master

    def update(self):
        for effect in self.effects:
            effect.sprite.x += effect.vel_x
            effect.sprite.y += effect.vel_y
            effect.travelled = effect.travelled + abs(effect.vel_x) + abs(effect.vel_y)
            if effect.travelled >= effect.travel:
                effect.sprite.delete()
                self.effects.remove(effect)

    def bullet_wound(self, vel_x, vel_y, start_x, start_y, sprites, ecolor):
        for e in range(sprites):
            e_vel_x = vel_x / 8 + random.randint(-3, 3)
            e_vel_y = vel_y / 8 + random.randint(-3, 3)
            self.effects.append(
                Effect(start_x=start_x, start_y=start_y,
                    vel_x=e_vel_x,
                    vel_y=e_vel_y,
                    travel=(abs(e_vel_x) + abs(e_vel_y)) * random.randint(5, 10),
                    ecolor=ecolor,
                    esizex=random.randint(1, 4), esizey=random.randint(1, 4),)
            )

    def message(self, start_x, start_y, text):
        self.effects.append(
            Text(start_x=start_x, start_y=start_y,
                text=str(text),
                f_color=(255, 0, 0, 150),
                f_size=14)
        )

    def bullet_hit(self, start_x, start_y, text):
        self.effects.append(
            Text(start_x=start_x, start_y=start_y,
                text=str(text),
                f_color=(255, 255, 255, 255),
                f_size=8)
        )

    def bullet_evade(self, start_x, start_y, text):
        self.effects.append(
            Text(start_x=start_x, start_y=start_y,
                text=str(text),
                f_color=(0, 0, 255, 155),
                f_size=8)
        )

    def bullet_crit(self, start_x, start_y, text):
        self.effects.append(
            Text(start_x=start_x, start_y=start_y,
                text=str(text),
                f_color=(255, 0, 0, 255),
                f_size=14)
        )

    def bullet_miss(self, start_x, start_y, text):
        self.effects.append(
            Text(start_x=start_x, start_y=start_y,
                text='miss',
                f_color=(255, 255, 255, 155),
                f_size=8)
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

    def explosion(self, start_x, start_y):
        for e in range(50):
            self.effects.append(
                Effect(start_x=start_x + random.randint(-5, 5),
                    start_y=start_y + random.randint(-5, 5),
                    vel_x=random.randint(-10, 10), vel_y=random.randint(-10, 10),
                    travel=50,
                    ecolor=[random.randint(200, 255), random.randint(0, 200),
                        random.randint(0, 55)],
                    esizex=random.randint(3, 6), esizey=random.randint(3, 6))
            )
