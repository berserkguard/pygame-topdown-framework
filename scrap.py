import pygame
from config import *

class ScrapTypes():
    def __init__(self):
        files = ["antenna", "claw", "cylinder", "metal_crate", "plate_metal", "spring"]
        self.images = [pygame.image.load('assets/scrap/' + files[idx] + '.png').convert_alpha() for idx in range(len(files))]
     

class Scrap():
    def __init__(self, scrap_types, idx, x, y):
        self.sprite = scrap_types.images[idx]
        self.x = x
        self.y = y
        
    def render(self, screen, game):
        # Offset map's center by the player's position
        x_pos = self.x - game.player.position[0] + Config.width / 2
        y_pos = self.y - game.player.position[1] + Config.height / 2
        
        # Don't render scraps that are off screen
        if x_pos + Config.scrap_size < 0 or x_pos - Config.scrap_size > Config.width:
            if y_pos + Config.scrap_size < 0 or y_pos - Config.scrap_size > Config.height:
                return;

        rect = self.sprite.get_rect()
        rect.center = (x_pos, y_pos)
        
        screen.blit(self.sprite, rect)
