import pygame
import random
import math
from config import *

class Laser():
    def __init__(self, turret_images, x, y, rot):
        self.sprite = turret_images.laser_sprite
        self.x = x
        self.y = y
        self.rotation = rot
    
    def update(self, delta, game):
        self.x += -math.sin(self.rotation * math.pi / 180) * 300 * delta;
        self.y += -math.cos(self.rotation * math.pi / 180) * 300 * delta;
        
        squareDist = math.pow(self.x - game.player.x, 2) + math.pow(self.y - game.player.y, 2)
        if squareDist < 400:
            # Collides with player
            part = random.randint(0, len(game.player.status) - 1)
            game.player.degrade_part(part, Config.degrade_amount / 2)
            
            return True
        
        # Destroy laser if it goes outside the map
        if self.x < 0 or self.x > Config.map_size * Config.tile_size:
            return True
        if self.y < 0 or self.y > Config.map_size * Config.tile_size:
            return True
        
        return False
    
    def render(self, screen, game):
        rotated = pygame.transform.rotate(self.sprite, self.rotation)
        
        # Offset lasers's center by the player's position
        x_pos = self.x - game.player.x + Config.width / 2
        y_pos = self.y - game.player.y + Config.height / 2

        # Skip lasers that are off screen
        if x_pos + Config.turret_size < 0 or x_pos - Config.turret_size > Config.width:
            if y_pos + Config.turret_size < 0 or y_pos - Config.turret_size > Config.height:
                return;
        
        rect = rotated.get_rect()
        rect.center = (x_pos, y_pos)
        
        screen.blit(rotated, rect)
        

class TurretImages():
    def __init__(self):
        self.turret_sprite = pygame.image.load('assets/turret.png')
        self.laser_sprite = pygame.image.load('assets/laser.png') 

class Turret():
    def __init__(self, turret_images, x, y):
        self.turret_images = turret_images
        self.sprite = turret_images.turret_sprite
        
        self.x = x
        self.y = y
        
        # Have turret start pointed in a random direction
        self.rotation = random.randint(0, 359)
        
        # Sight range of cone (in degrees)
        # TODO: move to config if time
        self.sight_range = 45
        self.fire_delay = 0.75
        self.next_fire = self.fire_delay
    
    def update(self, delta, game):
        squareDist = math.pow(self.x - game.player.x, 2) + math.pow(self.y - game.player.y, 2)
        if squareDist < math.pow(Config.turret_track_distance, 2):
            # Turret is in range; check if turret is facing player
            
            #angle = (math.atan2(-(self.x - game.player.x), -(self.y - game.player.y)) + math.pi) * 180 / math.pi
            angle = math.atan2(self.x - game.player.x, self.y - game.player.y) * 180 / math.pi
                        
            delta_angle = angle - self.rotation
            
            # LOL DOESN'T WORK, TOO TIRED TO FIGURE OUT WHY
            amt = math.fabs(math.fabs(angle) - math.fabs(self.rotation)) 
            if amt < self.sight_range:
                # Player is in sight; start tracking!
                rot_amount = 135
                self.rotation += min(delta_angle, rot_amount * delta)
                
                # If we're within 10 degrees, fire laser
                if amt < 10:
                    self.next_fire -= delta
                    if self.next_fire <= 0:
                        game.lasers.append(Laser(self.turret_images, self.x, self.y, self.rotation))
                        self.next_fire = self.fire_delay
                else:
                    self.next_fire = self.fire_delay

    def render(self, screen, game):
        rotated = pygame.transform.rotate(self.sprite, self.rotation)
        
        # Offset turrets's center by the player's position
        x_pos = self.x - game.player.x + Config.width / 2
        y_pos = self.y - game.player.y + Config.height / 2

        # Skip turrets that are off screen
        if x_pos + Config.turret_size < 0 or x_pos - Config.turret_size > Config.width:
            if y_pos + Config.turret_size < 0 or y_pos - Config.turret_size > Config.height:
                return;
        
        rect = rotated.get_rect()
        rect.center = (x_pos, y_pos)
        
        screen.blit(rotated, rect)
