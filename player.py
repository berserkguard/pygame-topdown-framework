import pygame
import math
import random
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
        
        # The body part status (1.0 to 0.0)
        self.antenna_status = 1.0
        self.head_status = 1.0
        self.body_status = 1.0
        self.right_arm_status = 1.0
        self.left_arm_status = 1.0
        self.right_leg_status = 1.0
        self.left_leg_status = 1.0
        
        self.status = [self.antenna_status, self.head_status, self.body_status, self.right_arm_status, self.left_arm_status, self.right_leg_status, self.left_leg_status]
        
        # Time passed since last body part degradation. Chance of degradation increases with time.
        self.time_since_last_degrade = 0
        
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
            
         # Set the player's rotation based on direction (lolbadcode)
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
            
        # Now, move the player.
        self.move(deltaX, deltaY)

        # Update degradation counter
        self.time_since_last_degrade += delta
        
        # See if we have a degradation!
        val = random.randint(1, 100)
        
        # Don't ask me where I got this formula from!
        if val < math.pow(1.02, math.pow(math.log(math.floor(self.time_since_last_degrade) + 60.0), 4)) / 3500.0:
            # Degradation!
            part = random.randint(0, len(self.status) - 1)
            self.status[part] -= 0.4
            print "Degradation!"
            self.time_since_last_degrade = 0
            
    def move(self, x, y):
        self.position[0] += x
        self.position[1] += y
