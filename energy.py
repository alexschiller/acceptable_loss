
def teleport(master, mouse_position):
    master.player.energy -= 100
    master.spriteeffect.teleport(master.player.sprite.x, master.player.sprite.y)
    master.player.sprite.x = mouse_position[0]
    master.player.sprite.y = mouse_position[1]
    master.spriteeffect.teleport(master.player.sprite.x, master.player.sprite.y)


def heal(master, mouse_position):
    master.player.energy -= 100
    master.player.health += 50
    if master.player.health > master.player.max_health:
        master.player.health = master.player.max_health

# def push(master, mouse_position):
# def

    # master.player.energy -= 100
    # master.player.health += 50
    # if master.player.health > master.player.max_health:
    #     master.player.health = master.player.max_health

    # master.spriteeffect.teleport(master.player.sprite.x, master.player.sprite.y)
    # master.player.sprite.x = mouse_position[0]
    # master.player.sprite.y = mouse_position[1]
    # master.spriteeffect.teleport(master.player.sprite.x, master.player.sprite.y)
