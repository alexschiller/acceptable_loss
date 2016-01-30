from box import * # noqa
from effect import * # noqa
# from enemy import * # noqa
from levelgenerator import * # noqa
from character import * # noqa
from energy import * # noqa
from gun import * # noqa
from player import * # noqa
from utility import * # noqa
from friend import * # noqa
from loot import * # noqa
from plasmaslinger import * # noqa


def reset_imp():
    for thing in master.people['red']:
            thing.on_death()
    master.room_manager.delete_all()
    master.room_manager = None
    master.room_manager = RoomManager(master)
    for item in master.loot.current_loot:
        del item
    for item in master.loot.moving_loot:
        del item
    # master.threat.threat = 0
    # master.threat.threat_time = 0


def ready_level(master, difficulty, num_rooms):
    master.loot = Loot(master)
    # master.resources = Resources(master)
    # master.radar = Radar(master)
    # master.threat = Threat(master)
    master.spriteeffect = SpriteEffect(master)
    # comment out this block to get rid of room color stuff

    # end of block, block party that is
    # master.player = load_save(save_1)

    master.player = Player(master, base=player_base)
    master.player_controller = master.player.controller

    master.room_manager = RoomManager(master)
    master.room_manager.setup(num_rooms)
    master.room_manager.parent.create_sprites(0, 0, TerrainBatch, master.player)
    master.room_manager.add_enemies()
    master.room_manager.create_portal()

    master.home = pyglet.sprite.Sprite(
        load_image('home.png'),
        window_width_half, window_height_half, batch=gfx_batch
    )

