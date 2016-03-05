import math
from utility import play_sound, load_sound

class StatsManager(object):
    def __init__(self, base, gun, armor):
        self.shield_hit = load_sound('shield_hit.wav')
        self.base = base
        self.level = base['level']

        self.extract_gems(armor['gem_slots'])
        self.extract_gems(gun['gem_slots'])

        self._damage = base.get('damage', 0)
        self._damage_min = base.get('damage_min', 0)
        self._damage_max = base.get('damage_max', 0)
        self._damage_perc = base.get('damage_perc', 0)
        self._attack_speed_perc = base.get('attack_speed_perc', 0)

        self._crit = base.get('crit', 0)
        self._crit_damage = base.get('crit_damage', 0)
        self._accuracy = base.get('accuracy', 0)
        self._armor_pierce = base.get('armor_pierce', 0)

        self._shield_max = base.get('shield_max', 0)

        self._shield_max_perc = base.get('shield_max_perc', 0)
        self._shield_regen = base.get('shield_regen', 0)
        self._shield_on_hit = base.get('shield_on_hit', 0)

        self._health_max = base.get('health_max', 0)

        self._health_max_perc = base.get('health_max_perc', 0)
        self._health_regen = base.get('health_regen', 0)
        self._health_on_hit = base.get('health_on_hit', 0)

        self._armor = base.get('armor', 0)
        self._speed = base.get('speed', 0)
        self._evade = base.get('evade', 0)

        self._accuracy_move = 0
        self._evade_move = 0

        self.recoil = 0
        self.shield_cooldown = 0
        self.delayed = []

        self._shield = self._shield_max
        self._health = self._health_max
        self.mods = 0
        self.mod = {
            'damage': 0,
            'damage_min': 0,
            'damage_max': 0,
            'damage_perc': 0,
            'attack_speed_perc': 0,
            'crit': 0,
            'crit_damage': 0,
            'accuracy': 0,
            'armor_pierce': 0,
            'shield_max': 0,
            'shield_max_perc': 0,
            'shield_regen': 0,
            'shield_on_hit': 0,
            'health_max': 0,
            'health_max_perc': 0,
            'health_regen': 0,
            'health_on_hit': 0,
            'armor': 0,
            'evade': 0,
            'speed': 0,
        }
        self.gun = gun

    def update_move(self, mx, my):
        if (abs(mx) + abs(my)) > 0:
            self._evade_move += .1
        else:
            self._evade_move -= .1
        if self._evade_move > 10:
            self._evade_move = 10
        elif self._evade_move <= 0:
            self._evade_move = 0
        self._accuracy_move = 10 - self._evade_move

    def update_delayed(self):
        for p in self.delayed:
            p[0] -= 1
            if p[0] == 0:
                self.mods -= 1
                self.mod[p[1]] -= p[2]
                self.delayed.remove(p)

    def temp_stat_change(self, time, stat, modifier):
        self.mod[stat] += modifier
        self.mods += 1
        self.delayed.append([time, stat, modifier])
        pass

    def update_stats(self):
        if self.shield_cooldown:
            self.shield_cooldown -= 1
        else:
            if self._shield < int(self.shield_max):
                self._shield += float(self.shield_regen) / 60.0
            else:
                self._shield = int(self.shield_max)

        if self._health < int(self.health_max):
            self._health += float(self.health_regen) / 60.0
        else:
            self._health = int(self.health_max)

    def update(self):
        self.update_recoil()
        self.update_stats()
        self.update_delayed()

    def update_recoil(self):
        if self.recoil > 0:
            self.recoil -= math.ceil(self.recoil / 90.0)

    def update_health(self, damage):
        if self._shield > 0:
            play_sound(self.shield_hit)
        self._shield -= damage
        if self._shield == 0:
            self.shield_cooldown = 120
            return 0
        if self._shield <= 0:
            self.shield_cooldown = 120
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
    def shield_regen(self):
        return self._shield_regen + self.mod['shield_regen']

    @property
    def health_max(self):
        return self._health_max + self.mod['health_max']

    @property
    def health(self):
        return self._health

    @property
    def health_regen(self):
        return self._health_regen + self.mod['health_regen']

    @property
    def damage_min(self):
        return self._damage + self._damage_min + self.mod['damage'] + self.mod['damage_min'] # noqa

    @property
    def armor_pierce(self):
        return self._armor_pierce + self.mod['armor_pierce']

    @property
    def damage_max(self):
        return self._damage + self._damage_max + self.mod['damage'] + self.mod['damage_max'] # noqa

    @property
    def damage_perc(self):
        return self._damage_perc + self.mod['damage_perc']

    @property
    def attack_speed_perc(self):
        return self._attack_speed_perc + self.mod['attack_speed_perc']

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

    @property
    def gun_data(self):
        return self.generate_gun(self.gun)

    def extract_gems(self, slots):
        for slot in slots.keys():
            modifier = 1
            if self.base['level'] == slots[slot]['current_gem']['level']:
                modifier += .2
            if slots[slot]['color'] == slots[slot]['current_gem']['color']:
                modifier += .2
            for stat in slots[slot]['current_gem']['stats'].keys():
                self.base[stat] += slots[slot]['current_gem']['stats'][stat]

    def generate_gun(self, gun):
        return {
            'damage_min': (gun['damage_min'] + self.damage_min) * ((100 + self.damage_perc) / 100), # noqa
            'damage_max': (gun['damage_max'] + self.damage_max) * ((100 + self.damage_perc) / 100), # noqa
            'range_max': gun['range_max'],
            'range_min': gun['range_min'],
            'velocity': gun['velocity'],
            'recoil': gun['recoil'],
            'accuracy': gun['accuracy'] + self.accuracy,
            'rof': gun['rof'] * ((100 + self.attack_speed_perc) / 100), # noqa
            'crit': gun['crit'] + self.crit,
            'crit_damage': gun['crit_damage'] + self.crit_damage,
            'armor_pierce': self.armor_pierce,
            'image': gun['image'],
            'gun_fire_sound': gun['gun_fire_sound'],
            'on_hit_sound': gun['on_hit_sound'],
        }
