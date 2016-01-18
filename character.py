from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet
from gun import * # noqa
from plasmaslinger import * # noqa

class Controller(object):
    def __init__(self, puppet):
        self.puppet = puppet

    def move(self, mx, my):
        if mx and my:
            mx = mx / 1.41
            my = my / 1.41
        self.puppet.stats.update_move(mx, my)
        self.puppet.sprite.x += (self.puppet.stats.speed * mx)
        self.puppet.sprite.y += (self.puppet.stats.speed * my)

    ## Controls
    def rotate(self, x, y):
        x_dist = x - float(self.puppet.sprite.x)
        y_dist = y - float(self.puppet.sprite.y)
        self.puppet.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90

    def attack(self):  # necessary?
        pass
        # if self.target:
            # self.gun.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target) # noqa                    

    def auto_attack():
        pass

    def switch_auto_attack():
        pass

    def slot_one_fire():
        pass

    def slot_two_fire():
        pass

    def slot_three_fire():
        pass

    def slot_four_fire():
        pass

    def slot_five_fire():
        pass

    def slot_six_fire():
        pass

    def update(self):
        pass

    ## AI Commands

    def target_closest_enemy(self):
        try:
            min_dist = float("inf")
            x1 = self.puppet.sprite.x
            y1 = self.puppet.sprite.y
            if len(self.puppet.enemies) == 0:
                return False
            for e in self.puppet.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    self.puppet.target = e
        except:
            self.puppet.target = None

    def update_movement(self):
        if self.puppet.target:
            ret = calc_vel_xy(self.puppet.target.sprite.x, self.puppet.target.sprite.y,
                self.puppet.sprite.x, self.puppet.sprite.y, self.puppet.stats.speed)
            self.puppet.sprite.x += ret[0]
            self.puppet.sprite.y += ret[1]

    def update_attack(self):
        pass
        # if math.hypot(abs(self.puppet.sprite.x - self.puppet.target.sprite.x), abs(self.puppet.sprite.y - self.puppet.target.sprite.y)) < self.puppet.gun.travel: # noqa
        # self.attack()


class PlayerController(Controller):
    def __init__(self, *args, **kwargs):
        super(PlayerController, self).__init__(*args, **kwargs)
        self.master = master
        self.black_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 150))
        self.black_dot = pyglet.image.create(10, 10, self.black_sprite)

        self.sprite = pyglet.sprite.Sprite(self.black_dot,
                    0, 0, batch=gfx_batch)

        self.collision = SpriteCollision(self.sprite)

        red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
        self.red_dot = pyglet.image.create(5, 5, red_sprite)
        self.marker = []

    def update_target(self):
        for e in self.puppet.enemies:
            if collide(self.collision, e.collision):
                self.build_target(e)
                break

    def build_target(self, e):
        bar = 2
        self.puppet.target = e
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

    def check_target(self):
        self.marker = []
        if self.puppet.target:
            try:
                self.rotate(self.puppet.target.sprite.x, self.puppet.target.sprite.y)
                self.build_target(self.puppet.target)
                self.puppet.ability.auto_attack()
            except:
                self.puppet.target = None
        else:
            self.rotate(self.sprite.x, self.sprite.y)

    def update(self):
        # self.puppet.update_bars()
        self.check_target()


class StatsManager(object):
    def __init__(self, base):
        self._shield_max = base.get('shield_max', 0)
        self._shield_regen = base.get('shield_regen', 0)
        self._shield = self._shield_max

        self._health_max = base.get('health', 10)
        self._health_regen = base.get('health_regen', 0)
        self._health = self._health_max

        self._damage_raw = base.get('damage_raw', 0)
        self._damage_percent = base.get('damage_percent', 100)

        self._attack_speed = base.get('attack_speed', 0)
        self._crit = base.get('crit', 5)
        self._crit_damage = base.get('crit_damage', .5)
        self._accuracy = base.get('accuracy', 0)
        self._accuracy_move = 0

        self._evade = base.get('evade', 0)
        self._evade_move = 0

        self._armor = base.get('armor', 0)
        self._speed = base.get('speed', 0)
        self.delayed = []

        self.mod = {
            'shield_max': 0,
            'shield_regen': 0,
            'shield': 0,
            'health_max': 0,
            'health_regen': 0,
            'health': 0,
            'damage_raw': 0,
            'damage_percent': 0,
            'attack_speed': 0,
            'crit': 0,
            'crit_damage': 0,
            'accuracy': 0,
            'evade': 0,
            'armor': 0,
            'speed': 0,
        }

    def update_move(self, mx, my):
        if (abs(mx) + abs(my)) > 0:
            self._evade_move += .1
        else:
            self._evade_move -= .1
        if self._evade_move > 10:
            self._evade_move = 10
        elif self._evade_move <= 0:
            self._evade_move = 0
        self._accuraccy_move = 10 - self._evade_move

    def update_delayed(self):
        for p in self.delayed:
            p[0] -= 1
            if p[0] == 0:
                self.mod[p[1]] -= p[2]
                self.delayed.remove(p)

    def temp_stat_change(self, time, stat, modifier):
        self.mod[stat] += modifier
        self.delayed.append([time, stat, modifier])
        pass

    def update_stats(self):
        if self.shield < self.shield_max:
            self._shield += self._shield_regen / 60
        if self.health < self.health_max:
            self._health += self._health_regen / 60

    def update(self):
        self.update_stats()
        self.update_delayed()

    def update_health(self, damage):
        self._shield -= damage
        if self._shield <= 0:
            damage = self._shield * -1
            self._shield = 0
            damage -= self.armor
            x = max(1, damage)
            self._health -= x
            return x
        return 0

    @property
    def shield_max(self):
        return self._shield_max + self.mod['shield_max']

    @property
    def shield(self):
        return self._shield

    @property
    def health_max(self):
        return self._health_max + self.mod['health_max']

    @property
    def health(self):
        return self._health

    @property
    def damage_raw(self):
        return self._damage_raw + self.mod['damage_raw']

    @property
    def damage_percent(self):
        return self._damage_percent + self.mod['damage_percent']

    @property
    def attack_speed(self):
        return self._attack_speed + self.mod['attack_speed']

    @property
    def crit(self):
        return self._crit + self.mod['crit']

    @property
    def crit_damage(self):
        return self._crit_damage + self.mod['crit_damage']

    @property
    def accuracy(self):
        return self._accuracy + self._accuracy_move + self.mod['accuracy']

    @property
    def armor(self):
        return self._armor + self.mod['armor']

    @property
    def evade(self):
        return self._evade + self._evade_move + self.mod['evade']

    @property
    def evade_move(self):
        return self._evade_move

    @property
    def speed(self):
        return self._speed + self.mod['speed']

enemy_soldier_base = {
    'sprite': load_image('soldier.png'),
    # 'coord': random.choice([[-50, random.randint(0, window_height)], [random.randint(0, window_width), -50]]),  # noqa
    'coord': [500, 500],  # noqa
    'weapon_slot_one': pm_magnum,
    'weapon_slot_two': pm_carbine,
    'ability': Ability,
    'ability_build': None,
    'color': 'red',
    'friends': 'red',
    'enemies': 'blue',
    'blood_color': (255, 10, 10, 255),
    'controller': Controller,
    'stats': {
        'shield_max': 5,
        'shield_regen': 1,
        'shield': 5,
        'health_max': 10,
        'health_regen': 0,
        'health': 10,
        'damage_raw': 0,
        'damage_percent': 1,
        'attack_speed': 1,
        'crit': 0,
        'crit_damage': 0,
        'accuracy': 0,
        'evade': 0,
        'armor': 1,
        'speed': 2
    },
}

player_base = {
    'sprite': load_image('dreadnaught.png'),
    'coord': [window_width / 2, window_height / 2],
    'weapon_slot_one': pm_magnum,
    'weapon_slot_two': pm_carbine,
    'ability': Ability,
    'ability_build': None,
    'color': 'blue',
    'friends': 'blue',
    'enemies': 'red',
    'blood_color': (30, 30, 30, 255),
    'controller': PlayerController,
    'stats': {
        'shield_max': 10,
        'shield_regen': 1,
        'shield': 10,
        'health_max': 50,
        'health_regen': 0,
        'health': 50,
        'damage_raw': 0,
        'damage_percent': 1,
        'attack_speed': 1,
        'crit': 0,
        'crit_damage': 0,
        'accuracy': 0,
        'evade': 0,
        'armor': 4,
        'speed': 3
    },
}

class Character(object):
    def __init__(self, master, base, **kwargs):
        self.master = master
        self.spriteeffect = master.spriteeffect
        self.friends = self.master.people[base['friends']]
        self.enemies = self.master.people[base['enemies']]
        self.blood_color = base['blood_color']
        self.base = base
        self.target = None
        self.bars = []

        self.sprite = pyglet.sprite.Sprite(base['sprite'], base['coord'][0], base['coord'][1], batch=gfx_batch) # noqa
        self.collision = SpriteCollision(self.sprite)

        self.master.people[base['color']].append(self)

        self.controller = base['controller'](self)
        self.stats = StatsManager(base['stats'])
        self.ability = base['ability'](
            base['ability_build'],
            self,
            base['weapon_slot_one'],
            base['weapon_slot_two']
        )

    def update_bars(self):
        self.bars = []
        hw = int(self.sprite.width * 2 * self.stats.health / self.stats.health_max) # noqa
        sw = int(self.sprite.width * 2 * self.stats.shield / (self.stats.shield_max + .01)) # noqa
        if hw > 0:
            self.bars.append(pyglet.sprite.Sprite(
                pyglet.image.create(hw, 2, red_sprite),
                self.sprite.x - self.sprite.width,
                self.sprite.y + self.sprite.height, batch=BarBatch))

        if sw > 0:
            self.bars.append(pyglet.sprite.Sprite(
                pyglet.image.create(sw, 2, blue_sprite),
                self.sprite.x - self.sprite.width,
                self.sprite.y + self.sprite.height + 5, batch=BarBatch))

    def death_check(self):
        if self.stats.health <= 0:
            self.on_death()

    def generate_loot(self):
        return {'resources': {'mon': random.randint(1, 5), 'sci': random.randint(1, 5)}, 'items': []} # noqa

    def on_death(self):
        self.master.loot.pack_package(self.generate_loot(), self.sprite.x, self.sprite.y)
        try:
            self.sprite.delete()
            self.master.people[self.base['color']].remove(self)
        except:
            pass

    def on_hit(self, bullet):
        final_damage = self.stats.update_health(bullet.damage)
        self.update_bars()
        if final_damage:
            splatter = min(max(int(final_damage / self.stats.health_max) * 30, 5), 50)
            self.spriteeffect.bullet_wound(bullet.vel_x, bullet.vel_y, self.sprite.x, self.sprite.y, splatter, self.blood_color) # noqa

    def update(self):
        self.update_bars()
        self.controller.update()
        self.ability.update()
        self.death_check()
