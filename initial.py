from gun import * # noqa
from character import * # noqa
from utility import * # noqa

shotgun = {
    'damage': 1,
    'travel': 300,
    'velocity': 10,
    'accuracy': .85,
    'spread': .10,
    'energy_cost': 20,
    'bullets': 50,
    'pierce': 0,
    'rof': 1,
    'knockback': 20.0,
    'image': load_image('shotgun.png'),
    'recoil': 10,
    'summon': None,
}

lineshot = {
    'damage': 1,
    'travel': 300,
    'velocity': 10,
    'accuracy': .85,
    'spread': .10,
    'energy_cost': 20,
    'bullets': 50,
    'pierce': 0,
    'rof': 1,
    'knockback': 20.0,
    'image': load_image('lineshot.png'),
    'recoil': 10,
    'summon': None,
}

red_laser = {
    'damage': 1,
    'travel': 600,
    'velocity': 10,
    'accuracy': .85,
    'spread': .02,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 0,
    'rof': 60,
    'knockback': 10.0,
    'image': load_image('red_laser.png'),
    'recoil': 1,
    'summon': None,
}


slimegun = {
    'damage': 1,
    'travel': 300,
    'velocity': 8,
    'accuracy': .85,
    'spread': .3,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 20,
    'rof': 10,
    'knockback': 10.0,
    'image': load_image('slimeball.png'),
    'recoil': 10,
    'summon': None,
}

def summon_jet():

    return Jet(player, enemy, jet_gun, spriteeffect)


tracker = {
    'damage': 0,
    'travel': 900,
    'velocity': 15,
    'accuracy': .85,
    'spread': .01,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 0,
    'rof': .5,
    'knockback': 0.0,
    'image': load_image('tracker.png'),
    'recoil': 0,
    'summon': summon_jet,
}

spriteeffect = SpriteEffect()
player = Player(spriteeffect)

enemy = []
pg = [tracker]
player_gun = Gun(enemy, base=random.choice(pg))
cannon_gun = Gun(enemy, base=shotgun)
jet_gun = Gun(enemy, base=shotgun)
enemy_gun = Gun(player, base=slimegun)

guns = [player_gun, cannon_gun, enemy_gun]
for i in range(4):
    enemy.append(Enemy(player, enemy, spriteeffect, enemy_gun))

grenade = Grenade()

friends = []
friends.append(Healer(player, enemy, cannon_gun, spriteeffect, friends,))
