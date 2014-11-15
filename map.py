import pygame
from config import *

class Map():
    def __init__(self):
        self.textures = [pygame.image.load('assets/sand.png')]
        
    def render(self, screen, game):
        for x in range(Config.map_size):
            for y in range(Config.map_size):
                
                # Offset map's center by the player's position
                x_pos = Config.tile_size * x - game.player.position[0] + Config.width / 2
                y_pos = Config.tile_size * y - game.player.position[1] + Config.height / 2

                # Skip tiles that are off screen
                if x_pos + Config.tile_size < 0 or x_pos - Config.tile_size > Config.width:
                    if y_pos + Config.tile_size < 0 or y_pos - Config.tile_size > Config.height:
                        continue;
            
                tile_type = self.textures[0]
                rect = tile_type.get_rect()
                rect.center = (x_pos, y_pos)
                
                screen.blit(tile_type, rect)
