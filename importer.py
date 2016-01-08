from box import * # noqa
from effect import * # noqa
from enemy import * # noqa
from energy import * # noqa
from gun import * # noqa
from player import * # noqa
from utility import * # noqa
from friend import * # noqa
import math

class Threat(object):
    def __init__(self, master):
        self.master = master
        self.threat = 0
        self.threat_time = 0

    def threat_timer(self):
        self.threat_time += 1
        if self.threat_time >= 60:
            self.threat += self.current_threat()
            self.threat_time = 0

    def current_threat(self):
        dist = math.hypot(self.master.player.sprite.x - self.master.home.x, self.master.player.sprite.y - self.master.home.y) # noqa
        return dist / 1000.0 * 1

    def update(self):
        self.threat_timer()
        if self.threat > 1:
            self.threat -= 1
            self.master.enemies.append(Soldier(self.master, base=gen_soldier_base())) # noqa

class Radar(object):
    def __init__(self, master):
        self.x_min = window_width - 350
        self.x_max = window_width - 150
        self.x_mid = (self.x_min + self.x_max) / 2
        self.y_min = window_height - 210
        self.y_max = window_height - 10
        self.y_mid = (self.y_min + self.y_max) / 2

        green_sprite = pyglet.image.SolidColorImagePattern(color=(0, 255, 0, 150))
        self.green_dot = pyglet.image.create(5, 5, green_sprite)

        blue_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 255, 150))
        self.blue_dot = pyglet.image.create(5, 5, blue_sprite)

        red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
        self.red_dot = pyglet.image.create(5, 5, red_sprite)

        self.master = master
        self.radar_range = 600
        self.radar_scale = self.radar_range / abs(self.x_mid - self.x_min)
        self.radar_player = pyglet.sprite.Sprite(self.blue_dot,
            self.x_mid, self.y_mid, batch=gfx_batch)
        self.to_draw = []

    def update(self):
        x1 = self.master.player.sprite.x
        y1 = self.master.player.sprite.y

        to_draw = []
        for e in self.master.enemies:
            if abs(x1 - e.sprite.x) + abs(y1 - e.sprite.y) <= self.radar_range:
                x_loc = self.x_mid - ((x1 - e.sprite.x) / self.radar_scale)
                y_loc = self.y_mid - ((y1 - e.sprite.y) / self.radar_scale)
                to_draw.append(pyglet.sprite.Sprite(self.red_dot, x_loc, y_loc, batch=gfx_batch)) # noqa
        self.to_draw = to_draw


master.radar = Radar(master)
master.threat = Threat(master)
master.spriteeffect = SpriteEffect(master)
master.player = Player(master, base=player_base)

master.home = pyglet.sprite.Sprite(load_image('home.png'),
            window_width_half, window_height_half, batch=gfx_batch)

# for i in range(5):
#     master.enemies.append(Soldier(master, base=gen_soldier_base() )) # noqa

# for i in range(2):
#   master.enemies.append(Slime(master, base=gen_slime_base() )) # noqa

for i in range(5):
    master.objects.append(Box(master)) # noqa

master.friends = [Cannon(master, base=gen_cannon_base())]
