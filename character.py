from pyglet.gl import * # noqa
from collide import * # noqa
from utility import * # noqa
import pyglet
from gun import * # noqa

class StatsManager(object):
    def __init__(self, base):
        self._shield_max = base.get('shield_max', 0)
        self._shield_regen = base.get('shield_regen', 0)
        self._shield = self._shield_max

        self._health_max = base.get('health', 10)
        self._health_regen = base.get('health_regen', 0)
        self._health = self._health_max

        self._damage_raw = base.get('damage_raw', 0)
        self._damage_percent = base.get('damage_percent', 0)

        self._attack_speed = base.get('attack_speed', 0)
        self._crit = base.get('crit', 5)
        self._crit_damage = base.get('crit_damage', .5)
        self._accuracy = base.get('accuracy', 0)
        self._evade = base.get('evade', 0)
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
            self._health -= max(1, damage)

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
        return self._accuracy + self.mod['accuracy']

    @property
    def armor(self):
        return self._armor + self.mod['armor']

    @property
    def evade(self):
        return self._evade + self.mod['evade']

    @property
    def speed(self):
        return self._speed + self.mod['speed']

class Character(object):
    def __init__(self, master, ability=None, **kwargs):
        self.master = master
        self.spriteeffect = master.spriteeffect
        self.enemies = master.enemies
        self.player = master.player
        self.health_bar = None
        self.target = None
        self.blood_color = [138, 7, 7, 255]
        self.evade = 0
        self.acc = 0

    def update_health_bar(self):
        hw = int(self.sprite.width * 2 * self.stats.health / self.stats.health_max) # noqa
        if hw > 0:
            self.health_bar = pyglet.sprite.Sprite(
                pyglet.image.create(hw, 2, red_sprite),
                self.sprite.x - self.sprite.width,
                self.sprite.y + self.sprite.height, batch=BarBatch)
        else:
            self.health_bar = None

    def move(self, x, y):
        self.sprite.x += (self.stats.speed * x)
        self.sprite.y += (self.stats.speed * y)

    def attack(self):
        if self.target:
            self.gun.fire(self.sprite.x, self.sprite.y, self.target.sprite.x, self.target.sprite.y, self, self.target) # noqa            

    def update_rotation(self):
        if self.target:
            dist_x = self.target.sprite.x - float(self.sprite.x)
            dist_y = self.target.sprite.y - float(self.sprite.y)
            self.sprite.rotation = (math.degrees(math.atan2(dist_y, dist_x)) * -1) + 90

    def update_movement(self):
        if self.target:
            ret = calc_vel_xy(self.target.sprite.x, self.target.sprite.y,
                self.sprite.x, self.sprite.y, self.stats.speed)
            self.sprite.x += ret[0]
            self.sprite.y += ret[1]

    def update_attack(self):
        if math.hypot(abs(self.sprite.x - self.target.sprite.x), abs(self.sprite.y - self.target.sprite.y)) < self.gun.travel: # noqa
            self.attack()

    def death_check(self):
        if self.stats.health <= 0:
            self.on_death()

    def required_updates(self):
        if self.target:  # This should probably be checked more often
            self.update_attack()
            self.update_movement()
        else:
            self.update_target()
        self.update_rotation()
        self.update_guns()
        self.death_check()

    def on_hit(self, bullet):
        self.stats.update_health(bullet.damage)
        self.update_health_bar()
        splatter = min(max(int(bullet.damage / self.stats.health_max) * 10, 3), 50)
        self.spriteeffect.bullet_wound(bullet.vel_x, bullet.vel_y, self.sprite.x, self.sprite.y, splatter, self.blood_color) # noqa

    def on_aoe_hit(self, damage):
        self.update_health(damage)

    def update_guns(self):
        for g in self.guns:
            g.update()

    def closest_object(self):
        closest = None
        min_dist = float('inf')
        x1 = self.sprite.x
        y1 = self.sprite.y
        for o in self.master.objects:
            dist = math.sqrt((o.sprite.x - x1) ** 2 + (o.sprite.y - y1) ** 2)
            if dist < min_dist:
                closest = o
                min_dist = dist
        return closest

    def load_guns(self, guns):
        self.guns = guns
        self.gun = self.guns[0]

    def check_object_collision(self, o):
        if collide(self.collision, o.collision):
            ret = calc_vel_xy(self.sprite.x, self.sprite.y,
            o.sprite.x, o.sprite.y, 1)
            self.sprite.x += ret[0] * self.stats.speed
            self.sprite.y += ret[1] * self.stats.speed

    def build_character(self, base):
        self.sprite = pyglet.sprite.Sprite(base['sprite'], base['coord'][0], base['coord'][1], batch=gfx_batch) # noqa
        self.collision = SpriteCollision(self.sprite)
        self.stats = StatsManager(base)
        self.load_guns(base['guns'])
