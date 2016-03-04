from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet
from enemy import * # noqa
from statsmanager import StatsManager
from controller import * # noqa


class Character(object):
    def __init__(self, master, base, **kwargs):
        self.master = master
        self.spriteeffect = master.spriteeffect
        self.friends = self.master.people[base['friends']]
        self.enemies = self.master.people[base['enemies']]
        self.blood_color = base['blood_color']
        self.base = base
        self.acc_mouse_mod = 1
        # self.build = base['build']
        self.target = None
        self.dead = False

        self.hbubble = pyglet.sprite.Sprite(load_image('hbubble.png'), base['coord'][0], base['coord'][1], batch=gfx_batch) # noqa
        self.sbubble = pyglet.sprite.Sprite(load_image('sbubble.png'), base['coord'][0], base['coord'][1], batch=gfx_batch) # noqa

        self.sprite = pyglet.sprite.Sprite(base['sprite'], base['coord'][0], base['coord'][1], batch=gfx_batch) # noqa
        self.collision = SpriteCollision(self.sprite)

        self.controller = base['controller'](self)
        self.stats = StatsManager(base['stats'],
            base['gun'],
            base['armor']
        )
        self.ability = Ability(
            self.master,
            self,
            base['skillset'],
            base['build'],
        )

        self.master.people[base['color']].append(self)

    def update_bars(self):
        # pass
        self.hbubble.x = self.sprite.x
        self.hbubble.y = self.sprite.y
        self.hbubble.scale = max(1 - self.stats.health / (self.stats.health_max + .01), .01)

        self.sbubble.x = self.sprite.x
        self.sbubble.y = self.sprite.y
        self.sbubble.scale = max(1 - self.stats.shield / (self.stats.shield_max + .01), .01)
        if self.sbubble.scale >= .95:
            self.sbubble.scale = .01

    def death_check(self):
        if self.stats.health <= 0:
            self.on_death()

    def generate_loot(self):
        gem = self.master.gem.create_loot_gem(self.stats.level)
        self.master.player.inventory.append(gem)

        return {'resources': {'mon': random.randint(1, 5), 'sci': random.randint(1, 5)}, 'items': []} # noqa

    def on_death(self):
        self.dead = True
        self.master.loot.pack_package(self.generate_loot(), self.sprite.x, self.sprite.y)
        try:
            self.hbubble.delete()
            self.sbubble.delete()
            self.sprite.delete()
            for p in self.ability.packages:
                p.cleanup()
            for t in self.ability.transmissions:
                t.cleanup()
            self.master.people[self.base['color']].remove(self)
        except:
            pass

    def on_hit(self, transmission):
        final_damage = self.stats.update_health(transmission.damage)
        self.controller.on_hit()
        # self.update_bars()
        if final_damage:
            splatter = min(max(int(final_damage / self.stats.health_max) * 30, 5), 20)
            self.spriteeffect.bullet_wound(transmission.ret[0], transmission.ret[0], self.sprite.x, self.sprite.y, splatter, self.blood_color) # noqa
        else:
            self.sbubble.x = self.sprite.x
            self.sbubble.y = self.sprite.y
        transmission.kill = self.stats.health <= 0

    def update(self):
        self.sbubble.x = -100
        self.sbubble.y = -100
        self.update_bars()
        self.stats.update()
        # self.update_bar_position()
        self.controller.update()
        self.ability.update()
        self.death_check()
