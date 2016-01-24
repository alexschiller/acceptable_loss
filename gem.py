import random

class Gem(object):
    def __init__(self):
        self.rarity_dict = { # noqa
            '0': {'rarity_color': 'gray', 'stats': 2, 'special': 0, },
            '1': {'rarity_color': 'blue', 'stats': 3, 'special': 0, },
            '2': {'rarity_color': 'purple', 'stats': 4, 'special': 0, },
            '3': {'rarity_color': 'green', 'stats': 5, 'special': 0, },
            '4': {'rarity_color': 'yellow', 'stats': 6, 'special': 0, },
            '5': {'rarity_color': 'orange', 'stats': 6, 'special': 1, },
        }

        self.stats_dict = {
            'damage': [2, 3, 1],
            'damage_min': [2, 4, 1],
            'damage_max': [4, 6, 1],
            'damage_perc': [5, 10, 1],
            'attack_speed_perc': [5, 10, 1],
            'crit': [1, 6, 0],
            'crit_damage': [5, 10, 1],
            'accuracy': [5, 10, 0],
            'armor_pierce': [1, 3, 1],
            'shield_max': [5, 10, 1],
            'shield_max_perc': [5, 10, 1],
            'shield_regen': [1, 2, 1],
            'shield_on_hit': [1, 3, 0],
            'health_max': [10, 20, 1],
            'health_max_perc': [5, 10, 1],
            'health_regen': [1, 2, 1],
            'health_on_hit': [1, 3, 0],
            'armor': [1, 3, 1],
        }

    def roll_rarity(self):
        rarity = 0
        while random.choice([0, 0, 0, 0, 1]):
            rarity += 1
            if rarity == 5:
                break
        return rarity

    def get_weapon_list(self):
        return ['damage'] * 5 + \
            ['damage_min'] * 3 + \
            ['damage_max'] * 3 + \
            ['damage_perc'] * 4 + \
            ['attack_speed_perc'] * 4 + \
            ['crit'] * 5 + \
            ['crit_damage'] * 3 + \
            ['accuracy'] * 5 + \
            ['armor_pierce'] * 5 + \
            ['shield_max'] * 2 + \
            ['shield_max_perc'] * 2 + \
            ['shield_regen'] * 1 + \
            ['shield_on_hit'] * 1 + \
            ['health_max'] * 2 + \
            ['health_max_perc'] * 2 + \
            ['health_regen'] * 1 + \
            ['health_on_hit'] * 1 + \
            ['armor'] * 1

    def get_armor_list(self):
        return ['damage'] * 2 + \
            ['damage_min'] * 1 + \
            ['damage_max'] * 1 + \
            ['damage_perc'] * 1 + \
            ['attack_speed_perc'] * 1 + \
            ['crit'] * 2 + \
            ['crit_damage'] * 1 + \
            ['accuracy'] * 1 + \
            ['armor_pierce'] * 1 + \
            ['shield_max'] * 5 + \
            ['shield_max_perc'] * 5 + \
            ['shield_regen'] * 5 + \
            ['shield_on_hit'] * 3 + \
            ['health_max'] * 5 + \
            ['health_max_perc'] * 3 + \
            ['health_regen'] * 5 + \
            ['health_on_hit'] * 3 + \
            ['armor'] * 5

    def roll_stats(self, prob_list, rolls):
        stats = []
        for i in range(rolls):
            chosen = random.choice(prob_list)
            stats.append(chosen)
            prob_list = filter(lambda a: a != chosen, prob_list)
        return stats

    def roll_stat_level(self, enemy_level):
        chances = 1 * [enemy_level - 4] + \
            3 * [enemy_level - 3] + \
            6 * [enemy_level - 2] + \
            10 * [enemy_level - 1] + \
            6 * [enemy_level] + \
            3 * [enemy_level + 1] + \
            1 * [enemy_level + 2]
        return max(random.choice(chances), 1)

    def create_loot_gem(self, enemy_level):
        gem_out = {}
        gem_out['rarity'] = self.roll_rarity()
        gem_out['color'] = random.choice(['sapphire', 'ruby', 'emerald', 'diamond']) # noqa
        gem_out['stats'] = {}

        prob_stats = random.choice([self.get_weapon_list(), self.get_armor_list()])
        num_stats = self.rarity_dict[str(gem_out['rarity'])]['stats']

        stats = self.roll_stats(prob_stats, num_stats)
        stats_levels = 0
        for stat in stats:
            level = self.roll_stat_level(enemy_level)
            stats_levels += level
            base = self.stats_dict[stat]
            if base[2]:
                gem_out['stats'][stat] = random.randint(base[0] * base[2], base[1] * base[2]) # noqa
            else:
                gem_out['stats'][stat] = random.randint(base[0], base[1])
        gem_out['level'] = stats_levels / num_stats
        print gem_out
