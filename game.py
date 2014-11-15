import pygame
import random
from player import *
from map import *
from status_indicator import *
from scrap import *

class Game():
    def __init__(self):
        self.player = Player()
        self.map = Map()
        
        self.screen = pygame.display.get_surface()
        self.status_indicator = StatusIndicator(self.player, 10, 350)

        self.scrap_types = ScrapTypes()

        self.scraps = []
        
        num_scraps = Config.map_size * Config.map_size * Config.scrap_density
        for i in range(int(num_scraps)):
            x_pos = random.randint(0, Config.map_size * Config.tile_size)
            y_pos = random.randint(0, Config.map_size * Config.tile_size)
            scrap_idx = random.randint(0, len(self.scrap_types.images) - 1)
            
            self.scraps.append(Scrap(self.scrap_types, scrap_idx, x_pos, y_pos))
        
    def render(self):
        self.map.render(self.screen, self)
        
        for scrap in self.scraps:
            scrap.render(self.screen, self)
        
        self.player.render(self.screen, self)
        
        # Render UI
        self.status_indicator.render(self.screen, self)
        
        
    def update(self, delta):
        self.player.update(delta)
        self.status_indicator.update(delta)
