from box import * # noqa
from effect import * # noqa
from enemy import * # noqa
from energy import * # noqa
from gun import * # noqa
from player import * # noqa
from utility import * # noqa
from friend import * # noqa
master.spriteeffect = SpriteEffect(master)
master.player = Player(master, base=player_base)

# for i in range(5):
#     master.enemies.append(Soldier(master, base=gen_soldier_base() )) # noqa

# for i in range(2):
# 	master.enemies.append(Slime(master, base=gen_slime_base() )) # noqa

for i in range(5):
    master.objects.append(Box(master)) # noqa

master.friends = [  # Friend(master, base=gen_friend_base())
]
