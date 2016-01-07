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
