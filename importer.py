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
        self.radar_range = 1000
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

class Resources(object):
    def __init__(self, master):
        self.sci = 0
        self.foo = 0
        self.pow = 0
        self.eng = 0
        self.mon = 0

        self.foo_ps = .1
        self.pow_ps = .12
        self.eng_ps = .09
        self.sci_ps = .11
        self.mon_ps = .15

        self.timer = 0
        self.foo_lab = pyglet.text.Label('F: ' + str(round(self.foo, 1)), font_name='Courier New', font_size=12, x=window_width - 150, y=130, anchor_x='left',anchor_y='center', batch=gfx_batch) # noqa        
        self.pow_lab = pyglet.text.Label('P: ' + str(round(self.pow, 1)), font_name='Courier New', font_size=12, x=window_width - 150, y=110, anchor_x='left',anchor_y='center', batch=gfx_batch) # noqa        
        self.eng_lab = pyglet.text.Label('E: ' + str(round(self.eng, 1)), font_name='Courier New', font_size=12, x=window_width - 150, y=90, anchor_x='left',anchor_y='center', batch=gfx_batch) # noqa        
        self.sci_lab = pyglet.text.Label('S: ' + str(round(self.sci, 1)), font_name='Courier New', font_size=12, x=window_width - 150, y=70, anchor_x='left',anchor_y='center', batch=gfx_batch) # noqa
        self.mon_lab = pyglet.text.Label('M: ' + str(round(self.mon, 1)), font_name='Courier New', font_size=12, x=window_width - 150, y=50, anchor_x='left',anchor_y='center', batch=gfx_batch) # noqa        

    def update_timer(self):
        self.timer += 1
        if self.timer == 60:
            self.timer = 0
            self.update_resources()

    def update_resources(self):
        self.labs = []
        self.sci += self.sci_ps
        self.foo += self.foo_ps
        self.pow += self.pow_ps
        self.eng += self.eng_ps
        self.mon += self.mon_ps
        self.update_labs()

    def update_labs(self):
        self.foo_lab.text = 'F: ' + str(round(self.foo, 1))
        self.pow_lab.text = 'P: ' + str(round(self.pow, 1))
        self.eng_lab.text = 'E: ' + str(round(self.eng, 1))
        self.sci_lab.text = 'S: ' + str(round(self.sci, 1))
        self.mon_lab.text = 'M: ' + str(round(self.mon, 1))

    def update(self):
        self.update_timer()
        self.update_labs()

class Pip(object):  # Personal Information Panel (PIP)
    def __init__(self, master):
        self.master = master
        self.player = master.player
        self.black_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 150))
        self.black_dot = pyglet.image.create(10, 10, self.black_sprite)
        self.sprite = pyglet.sprite.Sprite(self.black_dot,
                    0, 0, batch=gfx_batch)
        self.collision = SpriteCollision(self.sprite)

        self.marker = []

    def update(self):
        self.marker = []
        if self.player.target:
            try:
                x_dist = self.player.target.sprite.x - float(self.master.player.sprite.x)
                y_dist = self.player.target.sprite.y - float(self.master.player.sprite.y)
                self.build_target(self.player.target)
                master.player.attack()
            except:
                self.player.target = None
        else:
            x_dist = self.sprite.x - float(self.master.player.sprite.x)
            y_dist = self.sprite.y - float(self.master.player.sprite.y)
        deg = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90
        self.master.player.sprite.rotation = deg

    def closest_enemy(self):
        try:
            min_dist = float("inf")
            x1 = self.master.player.sprite.x
            y1 = self.master.player.sprite.y
            if len(self.master.enemies) == 0:
                return False
            for e in self.master.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    self.player.target = e
        except:
            self.player.target = None

    def build_target(self, e):
        # frame = 10
        bar = 2
        # half = 5
        self.player.target = e
        h = e.sprite.height
        w = e.sprite.width
        v = max(h, w)
        v2 = v / 2
        x = e.sprite.x
        y = e.sprite.y

        vs = pyglet.image.create(bar, v2, red_sprite)
        hs = pyglet.image.create(v2, bar, red_sprite)

        self.marker = [
            #  Bottom two verticals
            pyglet.sprite.Sprite(vs, x - v - 2, y - v, batch=gfx_batch),  # noqa 
            pyglet.sprite.Sprite(vs, x + v, y - v, batch=gfx_batch),  # noqa 
            #  Bottom two horizontals
            pyglet.sprite.Sprite(hs, x - v - 2, y - v, batch=gfx_batch),  # noqa 
            pyglet.sprite.Sprite(hs, x + v - v2 + 2, y - v, batch=gfx_batch),  # noqa 
            #  Top two verticals
            pyglet.sprite.Sprite(vs, x - v - 2, y + v, batch=gfx_batch),  # noqa 
            pyglet.sprite.Sprite(vs, x + v, y + v, batch=gfx_batch),  # noqa 
            #  Top two horizontals
            pyglet.sprite.Sprite(hs, x - v - 2, y + v + 5, batch=gfx_batch),  # noqa 
            pyglet.sprite.Sprite(hs, x + v - v2 + 2, y + v + 5, batch=gfx_batch),  # noqa 

        ]

    def update_target(self):
        red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
        self.red_dot = pyglet.image.create(5, 5, red_sprite)

        for e in master.enemies:
            if collide(self.collision, e.collision):
                self.build_target(e)
                break

master.resources = Resources(master)
master.radar = Radar(master)
master.threat = Threat(master)
master.spriteeffect = SpriteEffect(master)
master.player = Player(master, base=player_base)
master.pip = Pip(master)

master.home = pyglet.sprite.Sprite(load_image('home.png'),
            window_width_half, window_height_half, batch=gfx_batch)

# for i in range(5):
#     master.enemies.append(Soldier(master, base=gen_soldier_base() )) # noqa

# for i in range(2):
#   master.enemies.append(Slime(master, base=gen_slime_base() )) # noqa

for i in range(5):
    master.objects.append(Box(master)) # noqa

master.friends = [Cannon(master, base=gen_cannon_base())]
