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
from button import * # noqa


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


def start_state_buttons(image_dict, func_dict, button_batch, label_batch):
    dictt = [ # noqa
        "blank.png", "down_all_down.png",
        "down_all_up.png", "down_down.png",
        "down_more_down.png", "down_more_up.png",
        "down_up.png", "locked_down.png",
        "locked_up.png", "side_down.png",
        "side_up.png", "up.png", "up_all_down.png",
        "up_all_up.png", "up_more_down.png",
        "up_more_up.png", "up_up.png"
    ]
    buttons = [
        Button(
            image_dict['side_up.png'], image_dict['side_up.png'], image_dict['side_down.png'], 2 * window_width / 3,
            window_height / 2 - image_dict['side_up.png'].height / 2, func_dict['enter_game'], button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['down_all_up.png'], image_dict['down_all_up.png'], image_dict['down_all_down.png'], 2 * window_width / 3 - image_dict['side_up.png'].width,
            window_height / 2 - 2.5 * image_dict['side_up.png'].height / 2, func_dict['decrease_all'], button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['up_all_up.png'], image_dict['up_all_up.png'], image_dict['up_all_down.png'], 2 * window_width / 3 - image_dict['side_up.png'].width,
            window_height / 2 + .5 * image_dict['side_up.png'].height / 2, func_dict['increase_all'], button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['up_more_up.png'], image_dict['up_more_up.png'], image_dict['up_more_down.png'], 2 * window_width / 3 - 2 * image_dict['side_up.png'].width,
            window_height / 2 + .5 * image_dict['side_up.png'].height / 2, func_dict['increase_five'], button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['down_more_up.png'], image_dict['down_more_up.png'], image_dict['down_more_down.png'], 2 * window_width / 3 - 2 * image_dict['side_up.png'].width,
            window_height / 2 - 2.5 * image_dict['side_up.png'].height / 2, func_dict['decrease_five'], button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['down_up.png'], image_dict['down_up.png'], image_dict['down_down.png'], 2 * window_width / 3 - 3 * image_dict['side_up.png'].width,
            window_height / 2 - 2.5 * image_dict['side_up.png'].height / 2, func_dict['decrease'], button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['up_up.png'], image_dict['up_up.png'], image_dict['up.png'], 2 * window_width / 3 - 3 * image_dict['side_up.png'].width,
            window_height / 2 + .5 * image_dict['side_up.png'].height / 2, func_dict['increase'], button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['blank.png'], image_dict['blank.png'], image_dict['blank.png'], 2 * window_width / 3 - 7 * image_dict['side_up.png'].width / 2,
            window_height / 2 - image_dict['side_up.png'].height / 2, None, button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['blank.png'], image_dict['blank.png'], image_dict['blank.png'], 2 * window_width / 3 - 9 * image_dict['side_up.png'].width / 2,
            window_height / 2 - image_dict['side_up.png'].height / 2, None, button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['blank.png'], image_dict['blank.png'], image_dict['blank.png'], 2 * window_width / 3 - 11 * image_dict['side_up.png'].width / 2,
            window_height / 2 - image_dict['side_up.png'].height / 2, None, button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['blank.png'], image_dict['blank.png'], image_dict['blank.png'], 2 * window_width / 3 - 1 * image_dict['side_up.png'].width,
            window_height / 2 + 3 * image_dict['side_up.png'].height / 2, None, button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['blank.png'], image_dict['blank.png'], image_dict['blank.png'], 2 * window_width / 3 - 2 * image_dict['side_up.png'].width,
            window_height / 2 + 3 * image_dict['side_up.png'].height / 2, None, button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['blank.png'], image_dict['blank.png'], image_dict['blank.png'], 2 * window_width / 3 - 3 * image_dict['side_up.png'].width,
            window_height / 2 + 3 * image_dict['side_up.png'].height / 2, None, button_batch, None, labelbatch=label_batch
        ),
        Button(
            image_dict['locked_up.png'], image_dict['locked_up.png'], image_dict['locked_down.png'], 2 * window_width / 3,
            window_height / 2 + 3 * image_dict['side_up.png'].height / 2, None, button_batch, None, labelbatch=label_batch
        ),


    ]
    return buttons
