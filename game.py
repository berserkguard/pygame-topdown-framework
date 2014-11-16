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

        # A list of scraps on the map
        self.scraps = []
        
        # A list of scraps that have been picked up and are animating
        self.scrap_pickups = []
        
        num_scraps = Config.map_size * Config.map_size * Config.scrap_density
        for i in range(int(num_scraps)):
            x_pos = random.randint(0, Config.map_size * Config.tile_size)
            y_pos = random.randint(0, Config.map_size * Config.tile_size)
            scrap_idx = random.randint(0, len(self.scrap_types.images) - 1)
            
            self.scraps.append(Scrap(self.scrap_types, scrap_idx, x_pos, y_pos))
        
    def render(self):
        self.map.render(self.screen, self)
        
        # Render scraps
        for scrap in self.scraps:
            scrap.render(self.screen, self)
        
        for scrap in self.scrap_pickups:
            scrap.render(self.screen, self)
        
        self.player.render(self.screen, self)
        
        # Render UI
        self.status_indicator.render(self.screen, self)
        
        
    def update(self, delta):
        self.player.update(delta)
        self.status_indicator.update(delta)
        
        # Update scraps, making sure to remove any scraps that the player picked up.
        scraps_to_remove = []
        for scrap in self.scraps:
            if scrap.update(delta, self.player):
                scraps_to_remove.append(scrap)
                self.scrap_pickups.append(scrap)
        
        for scrap in scraps_to_remove:
            self.scraps.remove(scrap)
        
        # Animate picked-up scraps by having them gravitate to the player
        scraps_to_remove = []
        for scrap in self.scrap_pickups:
            x_delta = self.player.x - scrap.x
            y_delta = self.player.y - scrap.y
            if x_delta > 0:
                scrap.x += min(x_delta, Config.scrap_gravitation_speed * delta)
            elif x_delta < 0:
                scrap.x -= min(math.fabs(x_delta), Config.scrap_gravitation_speed * delta)
            
            if y_delta > 0:
                scrap.y += min(y_delta, Config.scrap_gravitation_speed * delta)
            elif y_delta < 0:
                scrap.y -= min(math.fabs(y_delta), Config.scrap_gravitation_speed * delta)
       
            if math.fabs(x_delta) < Config.scrap_size and math.fabs(y_delta) < Config.scrap_size:
                scraps_to_remove.append(scrap)
       
        for scrap in scraps_to_remove:
            self.player.acquire_scrap(scrap)
            self.scrap_pickups.remove(scrap)
      
