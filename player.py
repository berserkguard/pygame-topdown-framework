import pygame
import math
from config import *
from spritesheet import *

class Player():
    def __init__(self):
        # Spritesheet stuff
        self.spritesheet = Spritesheet('assets/robot_top_strip.png', 64, 64)
        self.sprite_idx = 0
        
        # Spritesheet runs at 12 FPS
        self.sprite_frame_rate = 1.0 / 12.0
        
        # Time remaining in animation before changing frames
        self.sprite_frame_time = self.sprite_frame_rate

        # Player's rotation (in degrees)
        self.rotation = 0.0
        
        # Start player in center of map
        self.position = [Config.map_size * Config.tile_size / 2.0, Config.map_size * Config.tile_size / 2.0]
        
        # Maximum speed of the player (in pixels/second)
        self.speed = 200.0
        
    def render(self, screen, game):
        sprite = self.spritesheet.get_sprite(self.sprite_idx)
        rotated = pygame.transform.rotate(sprite, self.rotation)
        
        rect = rotated.get_rect()
        rect.center = (Config.width / 2, Config.height / 2)
        
        screen.blit(rotated, rect)

    def update(self, delta):
        keys = pygame.key.get_pressed()
        deltaX = 0
        deltaY = 0
        if keys[pygame.K_w]:
            deltaY -= self.speed * delta
        if keys[pygame.K_s]:
            deltaY += self.speed * delta
        if keys[pygame.K_a]:
            deltaX -= self.speed * delta
        if keys[pygame.K_d]:
            deltaX += self.speed * delta
        
        # If moving diagonal, divide by sqrt(2) so maximum speed stays the same
        if deltaX is not 0 and deltaY is not 0:
            deltaX /= math.sqrt(2.0)
            deltaY /= math.sqrt(2.0)

        if deltaX is 0 and deltaY is 0:
            # If the player isn't moving, set sprite_idx to standing frame (frame 0)
            self.sprite_idx = 0
        else:
            # Otherwise, set the sprite_idx as needed.
            self.sprite_frame_time -= delta
            if self.sprite_frame_time < 0:
                self.sprite_frame_time += self.sprite_frame_rate
                self.sprite_idx += 1
                self.sprite_idx %= 8
            
         # Also, set the player's rotation based on direction
        if deltaX < 0 and deltaY < 0:
            self.rotation = 45
        elif deltaX < 0 and deltaY > 0:
            self.rotation = 135
        elif deltaX < 0 and deltaY is 0:
            self.rotation = 90
        elif deltaX > 0 and deltaY < 0:
            self.rotation = 315
        elif deltaX > 0 and deltaY > 0:
            self.rotation = 225
        elif deltaX > 0 and deltaY is 0:
            self.rotation = 270
        elif deltaY < 0 and deltaX is 0:
            self.rotation = 0
        elif deltaY > 0 and deltaX is 0:
            self.rotation = 180
        self.move(deltaX, deltaY)

    def move(self, x, y):
        self.position[0] += x
        self.position[1] += y
