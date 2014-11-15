import pygame
from player import *
from map import *

class Game():
    def __init__(self):
        self.player = Player()
        self.map = Map()
        
        self.screen = pygame.display.get_surface()

    def render(self):
        self.player.render(self.screen)
        
        self.map.render(self.screen)
