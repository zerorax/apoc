#!/usr/bin/python3.6

import pygame
import pygame.display as Display
import pygame.image as Image
import pygame.event as Event
import os
from random import randint


class Weapon:
    def __init__(self, rate, speed, bullet_type):
        self.bullet_type = bullet_types[bullet_type]
        self.rate = rate
        self.speed = speed


class Projectile:
    def __init__(self, player, bullettype, speed, posx, posy, xstart, xend, ystart, yend):
        self.player = player
        self.type = bullettype
        self.posx = posx
        self.posy = posy
        self.trajectory = get_bullet_traj(xstart, xend, ystart, yend, speed)


class GroundSpace:
    def __init__(self, name, imagefile, buildings=None):
        self.name = name
        self.image = Image.load(os.path.join("images", imagefile))
        self.buildings = buildings
        ground_spaces[name] = self


class GameInstance:
    def __init__(self):
        numpass, numfail = pygame.init()
        if numfail > 0:
            raise pygame.exception("A pygame module failed to initalize.")
        else:
            print("pygame submodules loaded")

        Display.set_mode((640,480), flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        LoadGround()
        self.surface = Display.get_surface()
        self.groundmap = []
        self.player = Player()
        self.projectiles = []
        self.clock = pygame.time.Clock()
        for x in range(16):  # 640/40
            groundmap = []
            for y in range(12):  # 480/40
                groundmap.append("grass%d" % randint(1, 3))
            self.groundmap.append(groundmap)
        self.draw_screen()

    def player_step(self):
        if self.player.k_up:
            self.player.posy -= 2
        if self.player.k_down:
            self.player.posy += 2
        if self.player.k_left:
            self.player.posx += 2
        if self.player.k_right:
            self.player.posx -= 2
        if self.player.k_lctrl:
            self.player_fire()

    def player_fire(self):
        if self.player.mg_wait > 0:
            self.player.mg_wait -= 1
        else:
            self.player.mg_wait = weapons["minigun"].rate
            bullets.append(Projectile(True, "minigun", 6, self.player.posx+28,
                                      self.player.posy+20, self.player.posx+25,
                                      self.player.posx+25, self.player.posy+20,
                                      self.player.posy+21))
            bullets.append(Projectile(True, "minigun", 6, self.player.posx-28,
                                      self.player.posy+20, self.player.posx+25,
                                      self.player.posx+25, self.player.posy+20,
                                      self.player.posy+21))

    def loop(self):
        self.clock = pygame.time.Clock()
        self.poll_input()
        self.player_step()
        self.draw_screen()
        self.clock.tick(60)

    def draw_screen(self):
        self.draw_ground()
        self.draw_player()
        Display.flip()

    def draw_player(self):  # 50*60
        x = 640 - self.player.posx - 25
        y = 480 - self.player.posy - 30
        self.surface.blit(ship_image, dest=(x, y))

    def draw_ground(self):
        for x in range(16):
            for y in range(12):
                self.surface.blit(ground_spaces[self.groundmap[x][y]].image, dest=(x * 40, y * 40))

    def poll_input(self):
        for event in Event.get():
            if event.type == pygame.QUIT:
                exit(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)
                if event.key == pygame.K_DOWN:
                    self.player.k_up = True
                elif event.key == pygame.K_UP:
                    self.player.k_down = True
                elif event.key == pygame.K_LEFT:
                    self.player.k_left = True
                elif event.key == pygame.K_RIGHT:
                    self.player.k_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.k_up = False
                elif event.key == pygame.K_UP:
                    self.player.k_down = False
                elif event.key == pygame.K_LEFT:
                    self.player.k_left = False
                elif event.key == pygame.K_RIGHT:
                    self.player.k_right = False

    def projectile_iter(self):
        for projectile in self.projectiles:
            if projectile.diry == 1:
                projectile.posy += projectile.speed

class Player:
    def __init__(self, health=80, weapons=[]):
        self.health = health
        self.posx = 320
        self.posy = 50
        self.weapon = None
        self.weapons = weapons
        self.k_up = False
        self.k_down = False
        self.k_left = False
        self.k_right = False
        self.k_lctrl = False
        self.k_lalt = False
        self.k_space = False


def LoadGround():
    for item in ground_tiles:
        ground_spaces[item] = GroundSpace(item, "%s.png" % item)


def get_bullet_traj(xstart,xend, ystart, yend, speed):
    distance = [xend - xstart, yend - ystart]
    norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    direction = [distance[0] / norm, distance[1] / norm]
    return([direction[0]*speed, direction[1]*speed])


ground_tiles = ["grass1", "grass2", "grass3"]
ground_buildings = []
ground_spaces = {}
ship_image = Image.load(os.path.join("images", "ship.png"))
bullet_types = {"minigun":1}
weapon_dict = {"minigun": Weapon(6, 8, "minigun")}
bullets = []

instance = GameInstance()
while True:
    instance.loop()
