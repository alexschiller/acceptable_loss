class Bullet(object):
    def __init__(self, base, start_x, start_y, target_x, target_y, chips=[]):
        # Base stats
        self.base = base
        self.damage = self.base['damage']
        self.travel = self.base['travel']
        self.velocity = self.base['velocity']
        self.spread = self.base['spread']
        self.accuracy = self.base['accuracy']
        self.knockback = self.base['knockback']
        self.pierce = self.base['pierce']

        x_dist = target_x - float(start_x)
        y_dist = target_y - float(start_y)

        self.calc_acc = float(1 - self.accuracy) * self.velocity
        self.calc_travel = self.travel - random.randint(
            0, int(float(1 - self.accuracy) * self.travel)
        )
        # Updated Stats
        self.travelled = 0
        self.sprite = pyglet.sprite.Sprite(base['image'],
            start_x, start_y, batch=BulletBatch)
        self.sprite.rotation = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90
        self.sprite.scale = 1
        self.collision = SpriteCollision(self.sprite)
        # compute directions

        ret = calc_vel_xy(target_x, target_y,
            start_x, start_y, self.velocity)

        self.vel_x = ret[0] + (random.gauss(0, self.spread) * self.velocity)
        self.vel_y = ret[1] + (random.gauss(0, self.spread) * self.velocity)

    def update(self):
        self.sprite.x += self.vel_x
        self.sprite.y += self.vel_y
        self.travelled += math.hypot(self.vel_x, self.vel_y)


class Gun(object):
    def __init__(self, master, base, hits, chips=[]): # noqa
        self.base = base
        self.rof = 60 / self.base['rof']
        self.rofl = 0
        self.bullets = []
        self.hits = hits
        self.master = master
        self.travel = self.base['travel']
        self.energy_cost = self.base['energy_cost']
        self.gun_fire_sound = self.base['gun_fire_sound']
        self.on_hit_sound = self.base['on_hit_sound']

        if hits == "enemies":
            self.bullet_checks = self.hits_bad
        else:
            self.bullet_checks = self.hits_good

    def fire(self, start_x, start_y, target_x, target_y):
        if self.rofl == self.rof:
            self.rofl -= self.rof
        # if len(self.bullets) > 30 or player.energy < self.energy_cost:
            # return True
        # player.energy -= self.energy_cost
            play_sound(self.gun_fire_sound)
            for b in range(self.base['bullets']):
                self.bullets.append(Bullet(self.base, start_x, start_y, target_x, target_y)) # noqa
            return True

    def delete_bullet(self, bullet):
        try:
            bullet.sprite.delete()
            self.bullets.remove(bullet)
        except:
            pass

    def update_pierce(self, bullet):
        bullet.pierce -= 1
        if bullet.pierce < 0:
            self.delete_bullet(bullet)

    def closest_object(self, bullet, obj_group):
        closest = None
        min_dist = float('inf')
        x1 = bullet.sprite.x
        y1 = bullet.sprite.y
        for o in obj_group:
            dist = math.sqrt((o.sprite.x - x1) ** 2 + (o.sprite.y - y1) ** 2)
            if dist < min_dist:
                closest = o
                min_dist = dist
        return closest

    def hits_good(self, bullet):
        if collide(bullet.collision, self.master.player.collision):
            play_sound(self.on_hit_sound)
            self.master.player.on_hit(bullet)
            self.update_pierce(bullet)

        try:
            o = self.closest_object(bullet, self.master.objects)
            if collide(bullet.collision, o.collision):
                self.update_pierce(bullet)
                return True
        except:
            pass

    def hits_bad(self, bullet):
        try:
            e = self.closest_object(bullet, self.master.enemies)
            if collide(bullet.collision, e.collision):
                play_sound(self.on_hit_sound)
                e.on_hit(bullet)
                self.update_pierce(bullet)
                return True
        except:
            pass
        try:
            o = self.closest_object(bullet, self.master.objects)
            if collide(bullet.collision, o.collision):
                self.update_pierce(bullet)
                return True
        except:
            pass

    def update(self):
        if self.rofl < self.rof:
            self.rofl += 1
        for bullet in self.bullets:
            bullet.update()
            self.bullet_checks(bullet)
            if bullet.travelled > bullet.calc_travel:
                self.delete_bullet(bullet)

    def select_target(self, bullet):
        try:
            min_dist = float("inf")
            coord = (0, 0)
            x1 = bullet.sprite.x
            y1 = bullet.sprite.y
            for e in self.master.enemies:
                dist = abs(math.hypot(x1 - e.sprite.x, y1 - e.sprite.y))
                if dist < min_dist:
                    min_dist = dist
                    coord = (e.sprite.x, e.sprite.y)
            return coord
        except:
            print "snail fail"
            return [bullet.sprite.x, bullet.sprite.y]

class MissileLauncher(Gun):
    def __init__(self, *args, **kwargs):
        super(MissileLauncher, self).__init__(*args, **kwargs)
        self.gun = Gun(master, hits=self.hits, base=self.base['effect_gun'])
        self.master.guns.append(self.gun)

    def delete_bullet(self, bullet):
        for i in range(10):
            self.gun.fire(bullet.sprite.x, bullet.sprite.y,
            bullet.sprite.x + random.randint(-4, 4),
            bullet.sprite.y + random.randint(-4, 4))
        try:
            bullet.sprite.delete()
            self.bullets.remove(bullet)
        except:
            pass

class Shrap(Gun):
    def __init__(self, *args, **kwargs):
        super(Shrap, self).__init__(*args, **kwargs)
        self.gun = Gun(master, hits=self.hits, base=self.base['effect_gun'])
        self.master.guns.append(self.gun)
        self.sprite = None
        self.red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))

    def update(self):
        if self.rofl < self.rof:
            self.rofl += 1
        self.sprite = None
        while len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update()
                self.bullet_checks(bullet)
                if bullet.travelled > bullet.calc_travel:
                    self.delete_bullet(bullet)

    def delete_bullet(self, bullet):
        red_line = pyglet.image.create(1, int(bullet.travelled), self.red_sprite)

        x_dist = bullet.sprite.x - float(master.player.sprite.x)
        y_dist = bullet.sprite.y - float(master.player.sprite.y)
        deg = (math.degrees(math.atan2(y_dist, x_dist)) * -1) + 90
        self.sprite = pyglet.sprite.Sprite(red_line, self.master.player.sprite.x, self.master.player.sprite.y, batch=gfx_batch) # noqa
        self.sprite.rotation = deg

        for i in range(10):
            self.gun.fire(bullet.sprite.x, bullet.sprite.y,
            bullet.sprite.x + random.randint(-4, 4),
            bullet.sprite.y + random.randint(-4, 4))
        try:
            bullet.sprite.delete()
            self.bullets.remove(bullet)
        except:
            pass

class MouseBoom(Gun):
    def __init__(self, *args, **kwargs):
        super(MouseBoom, self).__init__(*args, **kwargs)
        # self.gun = Gun(master, hits=self.hits, base=self.base['effect_gun'])
        # self.master.guns.append(self.gun)

    def fire(self, start_x, start_y, target_x, target_y):
        if self.rofl == self.rof:
            self.rofl -= self.rof
            play_sound(self.gun_fire_sound)
            for b in range(self.base['bullets']):
                self.bullets.append(Bullet(self.base, target_x, target_y, target_x + random.randint(-5,5), target_y + random.randint(-5,5))) # noqa
            return True

class Trail(Gun):
    def __init__(self, *args, **kwargs):
        super(Trail, self).__init__(*args, **kwargs)
        self.gun = Gun(master, hits=self.hits, base=self.base['effect_gun'])
        self.master.guns.append(self.gun)

    def update(self):
        if self.rofl < self.rof:
            self.rofl += 1
        for bullet in self.bullets:
            bullet.update()
            self.bullet_checks(bullet)
            self.gun.fire(bullet.sprite.x, bullet.sprite.y, bullet.sprite.x + random.randint(-5,5), bullet.sprite.y + random.randint(-5,5)) # noqa
            if bullet.travelled > bullet.calc_travel:
                self.delete_bullet(bullet)

class Flame(Gun):
    def __init__(self, *args, **kwargs):
        super(Flame, self).__init__(*args, **kwargs)
        # self.gun = Gun(master, hits=self.hits, base=self.base['effect_gun'])
        # self.master.guns.append(self.gun)

    def update(self):
        if self.rofl < self.rof:
            self.rofl += 1
        for bullet in self.bullets:
            bullet.update()
            bullet.sprite.scale = bullet.travelled / bullet.calc_travel + .1
            self.bullet_checks(bullet)
            if bullet.travelled > bullet.calc_travel:
                self.delete_bullet(bullet)


class Laser(Gun):
    def __init__(self, *args, **kwargs):
        super(Laser, self).__init__(*args, **kwargs)
        # self.gun = Gun(master, hits='enemies', base=self.base['effect_gun'])
        # self.master.guns.append(self.gun)

    def update_pierce(self, bullet):
        roll = random.randint(0, 100)
        if roll > 70:
            bullet.vel_x = bullet.vel_x * -1
        if roll < 30:
            bullet.vel_y = bullet.vel_y * -1
        if roll >= 30 and roll <= 70:
            bullet.vel_x = bullet.vel_x * -1
            bullet.vel_y = bullet.vel_y * -1

        bullet.pierce -= 1
        if bullet.pierce < 0:
            self.delete_bullet(bullet)


class Strafe(Gun):
    def __init__(self, *args, **kwargs):
        super(Strafe, self).__init__(*args, **kwargs)
        self.gun = Gun(master, hits=self.hits, base=self.base['effect_gun'])
        self.master.guns.append(self.gun)

    def update(self):
        if self.rofl < self.rof:
            self.rofl += 1
        for bullet in self.bullets:
            if random.randint(0, 100) >= 80:
                coord = self.select_target(bullet)
                self.gun.fire(bullet.sprite.x, bullet.sprite.y, coord[0], coord[1])
            bullet.update()
            self.bullet_checks(bullet)
            if bullet.travelled > bullet.calc_travel:
                self.delete_bullet(bullet)


# Prefab guns for now, belong elsewhere

fire = {
    'damage': 1,
    'travel': 300,
    'velocity': 15,
    'accuracy': .85,
    'spread': .10,
    'energy_cost': 20,
    'bullets': 20,
    'pierce': 0,
    'rof': 1,
    'knockback': 20.0,
    'image': load_image('tracker.png'),
    'recoil': 10,
    'effect_gun': None,
    'gun_fire_sound': load_sound('shotgun.wav'),
    'on_hit_sound': load_sound('on_hit_2.wav'),
}

exgun = {
    'damage': 1,
    'travel': 500,
    'velocity': 15,
    'accuracy': .85,
    'spread': .15,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 0,
    'rof': 5,
    'knockback': 1.0,
    'image': load_image('snipe.png'),
    'recoil': 1,
    'effect_gun': None,
    'gun_fire_sound': None,
    'on_hit_sound': load_sound('on_hit.wav'),
}

sniper = {
    'damage': 5,
    'travel': 700,
    'velocity': 15,
    'accuracy': .85,
    'spread': .01,
    'energy_cost': 20,
    'bullets': 3,
    'pierce': 0,
    'rof': 2,
    'knockback': 1.0,
    'image': load_image('star.png'),
    'recoil': 1,
    'effect_gun': None,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
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
    'effect_gun': None,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}

jet_laser = {
    'damage': 1,
    'travel': 500,
    'velocity': 10,
    'accuracy': .85,
    'spread': .05,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 2,
    'rof': 20,
    'knockback': 10.0,
    'image': load_image('red_laser.png'),
    'recoil': 0,
    'effect_gun': fire,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}

splode = {
    'damage': 1,
    'travel': 500,
    'velocity': 20,
    'accuracy': .85,
    'spread': 0,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 0,
    'rof': 300,
    'knockback': 10.0,
    'image': load_image('jet.png'),
    'recoil': 50,
    'effect_gun': None,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
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
    'effect_gun': None,
    'gun_fire_sound': None,
    'on_hit_sound': load_sound('on_hit.wav'),
}

tracker = {
    'damage': 1,
    'travel': 300,
    'velocity': 10,
    'accuracy': .85,
    'spread': .15,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 99,
    'rof': 99,
    'knockback': 0.0,
    'image': load_image('tracker.png'),
    'recoil': 0,
    'effect_gun': True,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}

rocket = {
    'damage': 2,
    'travel': 150,
    'velocity': 20,
    'accuracy': .85,
    'spread': .15,
    'energy_cost': 20,
    'bullets': 1,
    'pierce': 0,
    'rof': 10,
    'knockback': 0.0,
    'image': load_image('missile.png'),
    'recoil': 0,
    'effect_gun': fire,
    'gun_fire_sound': load_sound('laser.wav'),
    'on_hit_sound': load_sound('on_hit.wav'),
}

# missile = {
#     'damage': 2,
#     'travel': 800,
#     'velocity': 5,
#     'accuracy': .85,
#     'spread': 0,
#     'energy_cost': 20,
#     'bullets': 1,
#     'pierce': 0,
#     'rof': 5,
#     'knockback': 0.0,
#     'image': load_image('missile.png'),
#     'recoil': 0,
#     'effect_gun': fire,
#     'gun_fire_sound': load_sound('laser.wav'),
#     'on_hit_sound': load_sound('on_hit.wav'),
# }

# trail = {
#     'damage': 2,
#     'travel': 800,
#     'velocity': 8,
#     'accuracy': .85,
#     'spread': 0,
#     'energy_cost': 20,
#     'bullets': 1,
#     'pierce': 0,
#     'rof': 1,
#     'knockback': 0.0,
#     'image': load_image('missile.png'),
#     'recoil': 0,
#     'effect_gun': fire,
#     'gun_fire_sound': load_sound('laser.wav'),
#     'on_hit_sound': load_sound('on_hit.wav'),
# }

# shrap = {
#     'damage': 1,
#     'travel': 200,
#     'velocity': 10,
#     'accuracy': .85,
#     'spread': .5,
#     'energy_cost': 20,
#     'bullets': 10,
#     'pierce': 0,
#     'rof': 100,
#     'knockback': 1.0,
#     'image': load_image('burr.png'),
#     'recoil': 5,
#     'effect_gun': None,
#     'gun_fire_sound': load_sound('shotgun.wav'),
#     'on_hit_sound': load_sound('on_hit_2.wav'),
# }

# shrapnel = {
#     'damage': 1,
#     'travel': 400,
#     'velocity': 8,
#     'accuracy': .85,
#     'spread': .06,
#     'energy_cost': 20,
#     'bullets': 1,
#     'pierce': 0,
#     'rof': 1,
#     'knockback': 20.0,
#     'image': load_image('ball.png'),
#     'recoil': 10,
#     'effect_gun': shrap,
#     'gun_fire_sound': load_sound('shotgun.wav'),
#     'on_hit_sound': load_sound('on_hit_2.wav'),
# }