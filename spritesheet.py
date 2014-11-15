import pygame
import math

class Spritesheet():
    def __init__(self, filename, sprite_width, sprite_height):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.num_cols = self.sheet.get_width() / self.sprite_width
        self.num_rows = self.sheet.get_height() / self.sprite_height
        
    # Returns the sprite at the given frame index.
    def get_sprite(self, idx):
        x_idx = idx % self.num_cols 
        y_idx = math.floor(idx / self.num_cols)
        start_x = x_idx * self.sprite_width
        start_y = y_idx * self.sprite_height
        rect = pygame.Rect((start_x, start_y, self.sprite_width, self.sprite_height))
        image = pygame.Surface((self.sprite_width, self.sprite_height), flags=pygame.SRCALPHA, depth=32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image;
