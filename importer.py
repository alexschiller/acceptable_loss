from box import * # noqa
from effect import * # noqa
from enemy import * # noqa
from energy import * # noqa
from gun import * # noqa
from player import * # noqa
from utility import * # noqa

master.spriteeffect = SpriteEffect(master)
master.player = Player(master, base=player_base)

for i in range(5):
    master.enemies.append(Enemy(master, base=gen_soldier_base() )) # noqa

for i in range(20):
    master.objects.append(Box(master)) # noqa


master.friends = [
    # Healer(master, gun_dict['cannon_gun']), # noqa
    # Cannon(player, enemy, gun, spriteeffect)
]
