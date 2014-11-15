import pygame
from config import *

class Player():
    def __init__(self):
        self.sprite = pygame.image.load('assets/player.png')
        self.rotation = 360

    def render(self, screen):
        rotated = pygame.transform.rotate(self.sprite, self.rotation)
        
        rect = rotated.get_rect()
        rect.center = (Config.width / 2, Config.height / 2)
        
        screen.blit(rotated, rect)

