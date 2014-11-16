import pygame
import math
import random
from config import *
from spritesheet import *
from message_util import *
from status_indicator import *

class Player():
    def __init__(self, game):
        self.game = game
    
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
        self.x = Config.map_size * Config.tile_size / 2.0
        self.y = Config.map_size * Config.tile_size / 2.0
        
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
        self.part_names = ["antenna", "head", "body", "right arm", "left arm", "right leg", "left leg"]
        
        self.yellow_ailment_descriptions = [
            "Reduced visibility.",
            "Inverted movement controls.",
            "Repair amount reduced by 25%.",
            "Reduces pickup distance by 25% (right arm).",
            "Reduces pickup distance by 25% (left arm).",
            "Reduces movement speed by 25% (right leg).",
            "Reduces movement speed by 25% (left leg)."
        ]
        self.red_ailment_descriptions = [
            "Greatly reduced visibility.",
            "Randomized movement controls (20% chance).",
            "Repair amount reduced by 50%.",
            "Reduces pickup distance by 50% (right arm).",
            "Reduces pickup distance by 50% (left arm).",
            "Reduces movement speed by 50% (right leg).",
            "Reduces movement speed by 50% (left leg)."
        ]
        
        # Variables for player abilities
        self.pickup_radius = Config.tile_size # Scrap pickup radius (in pixels) 
        
        # Time passed since last body part degradation. Chance of degradation increases with time.
        self.time_since_last_degrade = 0
        
    def render(self, screen):
        sprite = self.spritesheet.get_sprite(self.sprite_idx)
        rotated = pygame.transform.rotate(sprite, self.rotation)
        
        rect = rotated.get_rect()
        rect.center = (Config.width / 2, Config.height / 2)
        
        screen.blit(rotated, rect)

    def update(self, delta):
        keys = pygame.key.get_pressed()
        deltaX = 0
        deltaY = 0
        
        modifier = 1;
        
        # Invert controls for yellow head
        if self.get_status(self.head_status) is StatusIndicator.YELLOW:
            modifier = -1
        
        # For red head, random controls!
        if self.get_status(self.head_status) is StatusIndicator.RED:
            val = random.rand_int(1, 25)
            if val is 1:
                deltaX += self.speed * delta
            elif val is 2:
                deltaY += self.speed * delta
            elif val is 3:
                deltaY -= self.speed * delta
            elif val is 4:
                deltaX -= self.speed * delta
            else:
                # Normal controls 80% of the time
                if keys[pygame.K_w]:
                    deltaY -= self.speed * delta
                if keys[pygame.K_s]:
                    deltaY += self.speed * delta
                if keys[pygame.K_a]:
                    deltaX -= self.speed * delta
                if keys[pygame.K_d]:
                    deltaX += self.speed * delta
        else:
            if keys[pygame.K_w]:
                deltaY -= modifier * self.speed * delta
            if keys[pygame.K_s]:
                deltaY += modifier * self.speed * delta
            if keys[pygame.K_a]:
                deltaX -= modifier * self.speed * delta
            if keys[pygame.K_d]:
                deltaX += modifier * self.speed * delta
        
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

        # Leg ailment
        if self.get_status(self.right_leg_status) is StatusIndicator.RED or self.get_status(self.left_leg_status) is StatusIndicator.RED:
            deltaX *= 0.5
            deltaY *= 0.5
        elif self.get_status(self.right_leg_status) is StatusIndicator.YELLOW or self.get_status(self.left_leg_status) is StatusIndicator.YELLOW:
            deltaX *= 0.75
            deltaY *= 0.75
        
        # Now, move the player.
        self.move(deltaX, deltaY)

        # Update degradation counter
        self.time_since_last_degrade += delta
        
        # See if we have a degradation!
        val = random.randint(1, 100)
        
        # Don't ask me where I got this formula from!
        if val < math.pow(1.02, math.pow(math.log(math.floor(self.time_since_last_degrade) + 60.0), 4)) / 3500.0 * 2.0:
            # Degradation!
            part = random.randint(0, len(self.status) - 1)
            self.degrade_part(part, Config.degrade_amount)
            self.time_since_last_degrade = 0
        
        # Check for lose condition (all parts red)
        for i in range(len(self.status) - 1):
            if self.get_status(self.status[i]) != StatusIndicator.RED:
                return False
        return True
        
    def move(self, x, y):
        self.x += x
        self.y += y
    
    # Helper function for getting the status based on amount
    def get_status(self, amount):
        if amount > 0.7:
            return StatusIndicator.GREEN
        elif amount > 0.3:
            return StatusIndicator.YELLOW
        else:
            return StatusIndicator.RED
    
    # Degrades the part by the given amount
    def degrade_part(self, part_idx, amount):
        self.status[part_idx] = max(self.status[part_idx] - Config.degrade_amount, 0)
        
        part_status = self.get_status(self.status[part_idx])
        part_name = self.part_names[part_idx]
        part_durability = int(self.status[part_idx] * 100)
        if part_status is StatusIndicator.YELLOW:
            base_str = "Your %s is mildly damaged! Durability: %d%%"
            self.game.message_util.add_message(Message(base_str % (part_name, part_durability), (255, 0, 0)))
        elif part_status is StatusIndicator.RED:
            base_str = "Your %s is critically damaged! Durability: %d%%"
            self.game.message_util.add_message(Message(base_str % (part_name, part_durability), (255, 0, 0)))
        else:
            base_str = "Your %s has degraded! Current durability: %d%%"
            self.game.message_util.add_message(Message(base_str % (part_name, part_durability), (255, 0, 0)))
        
        self.refresh_ailments()
    
    # Refreshes the ailments
    def refresh_ailments(self):
        self.game.ailment_texts = []
        
        for i in range(len(self.status)):
            part = self.part_names[i]
            status = self.get_status(self.status[i])
            
            # If we have a status ailment, add to game.ailment_texts
            if status is StatusIndicator.YELLOW:
                self.game.ailment_texts.append(self.yellow_ailment_descriptions[i])
            elif status is StatusIndicator.RED:
                self.game.ailment_texts.append(self.red_ailment_descriptions[i])
            
    # Returns true if the player is able to pick up the given scrap.
    def in_scrap_range(self, scrap):
        rad = self.pickup_radius
        
        # Arm ailments
        if self.get_status(self.right_arm_status) is StatusIndicator.RED or self.get_status(self.left_arm_status) is StatusIndicator.RED:
            rad *= 0.5
        elif self.get_status(self.right_arm_status) is StatusIndicator.YELLOW or self.get_status(self.left_arm_status) is StatusIndicator.YELLOW:
            rad *= 0.75

        squareDist = math.pow(self.x - scrap.x, 2) + math.pow(self.y - scrap.y, 2)
        return squareDist < math.pow(rad, 2)
    
    # Handles logic for player picking up a scrap.
    def acquire_scrap(self, scrap):
        scrap_name = self.game.scrap_types.names[scrap.idx]
        part_name = self.game.scrap_types.parts[scrap.idx]
        rep_amt = Config.repair_amount
        
        # Body ailments
        if self.get_status(self.body_status) is StatusIndicator.RED:
            rep_amt *= 0.5
        elif self.get_status(self.body_status) is StatusIndicator.YELLOW:
            rep_amt *= 0.75


        # Prioritize arm & leg with lower durability (also pretty ugly...)
        if part_name is 'arm':
            right_arm_durability = int(self.status[self.part_names.index("right arm")] * 100)
            left_arm_durability = int(self.status[self.part_names.index("left arm")] * 100)
            
            if left_arm_durability < right_arm_durability:
                part_name = "left arm"
            else:
                part_name = "right arm"
        elif part_name is 'leg':
            right_leg_durability = int(self.status[self.part_names.index("right leg")] * 100)
            left_leg_durability = int(self.status[self.part_names.index("left leg")] * 100)
            
            if left_leg_durability < right_leg_durability:
                part_name = "left leg"
            else:
                part_name = "right leg"

        part_idx = self.part_names.index(part_name)
        self.status[part_idx] = min(self.status[part_idx] + Config.repair_amount, 1.0)
        part_durability = int(self.status[part_idx] * 100)
        self.game.message_util.add_message(Message("Scrap acquired: %s [part: %s, durability: %d%%]" % (scrap_name, part_name, part_durability), (0, 255, 0)))
        
        self.refresh_ailments()
        
    
