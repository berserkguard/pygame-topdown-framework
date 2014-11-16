import pygame

class StatusIndicator():
    GREEN = 0
    YELLOW = 1
    RED = 2

    def __init__(self, player, x, y):
        # Helper function for getting the red, yellow, green images for a given body part.
        def get_images(body_part):
            return [
                pygame.image.load('assets/status/' + body_part + '_green.png'),
                pygame.image.load('assets/status/' + body_part + '_yellow.png'),
                pygame.image.load('assets/status/' + body_part + '_red.png')
            ]
    
        # Images for each body part and each status
        self.antenna = get_images('antenna')
        self.head = get_images('head')
        self.body = get_images('body')
        self.right_arm = get_images('right_arm')
        self.left_arm = get_images('left_arm')
        self.right_leg = get_images('right_leg')
        self.left_leg = get_images('left_leg')
        
        self.images = [self.antenna, self.head, self.body, self.right_arm, self.left_arm, self.right_leg, self.left_leg]
        
        # The status indices. 0 = green, 1 = yellow, 2 = red
        self.antenna_status = StatusIndicator.GREEN
        self.head_status = StatusIndicator.GREEN
        self.body_status = StatusIndicator.GREEN
        self.right_arm_status = StatusIndicator.GREEN
        self.left_arm_status = StatusIndicator.GREEN
        self.right_leg_status = StatusIndicator.GREEN
        self.left_leg_status = StatusIndicator.GREEN
        
        self.status = [self.antenna_status, self.head_status, self.body_status, self.right_arm_status, self.left_arm_status, self.right_leg_status, self.left_leg_status]
        
        # Player
        self.player = player
        
        # Position
        self.x = x
        self.y = y
        
    def update(self, delta):
        # Update the StatusIndicator's status to match the player's
        for i in range(len(self.player.status)):
            self.status[i] = self.player.get_status(self.player.status[i])
    
    def render(self, screen, game):
        for i in range(len(self.images)):
            image = self.images[i][self.status[i]]
            image.set_alpha(50)
            rect = image.get_rect()
            rect.topleft = (self.x, self.y)
            
            screen.blit(image, rect)
