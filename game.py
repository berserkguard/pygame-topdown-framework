import pygame
from player import *
from map import *
from status_indicator import *

class Game():
    def __init__(self):
        self.player = Player()
        self.map = Map()
        
        self.screen = pygame.display.get_surface()
        self.status_indicator = StatusIndicator(10, 350)

    def render(self):
        self.map.render(self.screen, self)
        
        self.player.render(self.screen, self)
        
        # Render UI
        self.status_indicator.render(self.screen, self)
        
        
    def update(self, delta):
        self.player.update(delta)
