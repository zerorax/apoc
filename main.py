#!/usr/bin/python3.6

import pygame
import pygame.display as Display
import pygame.image as Image
from time import sleep
from random import randint


ground_tiles = ["grass1", "grass2", "grass3"]
ground_buildings = []
ground_spaces = {}
ship_image = Image.load("ship.png")


class GroundSpace:
    def __init__(self, name, imagefile, buildings=None):
        self.name = name
        self.image = Image.load(imagefile)
        self.buildings = buildings
        ground_spaces[name] = self


def LoadGround():
    for item in ground_tiles:
        ground_spaces[item] = GroundSpace(item, "%s.png" % item)


class GameInstance:
    def __init__(self):
        numpass, numfail = pygame.init()
        if numfail > 0:
            raise pygame.exception("A pygame module failed to initalize.")
        else:
            print("pygame submodules loaded")

        Display.set_mode((640,480), flags=pygame.FULLSCREEN | pygame.HWSURFACE)
        LoadGround()
        self.surface = Display.get_surface()
        self.groundmap = []
        self.player = Player()
        for x in range(16):  # 640/40
            groundmap = []
            for y in range(12):  # 480/40
                groundmap.append("grass%d" % randint(1,3))
            self.groundmap.append(groundmap)
        self.draw_screen()
        sleep(10)

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
        Display.flip()


class Player:
    def __init__(self, health=80, weapons=[]):
        self.health = health
        self.posx = 320
        self.posy = 50
        self.weapon = None
        self.weapons = weapons

    def CheckKeyInput(self):
        pass


instance = GameInstance()
pygame.quit()
