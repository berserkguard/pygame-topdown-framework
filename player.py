import pygame

class Player(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # create 50px by 50px surface
        self.image = pygame.Surface((50, 50))
        # color the surface cyan
        self.image.fill((0, 205, 205))
        self.rect = self.image.get_rect()
        self.speed = [0, 0]

    def left(self):
        self.speed[0] -= 8

    def right(self):
        self.speed[0] += 8

    def up(self):
        self.speed[1] -= 8

    def down(self):
        self.speed[1] += 8

    def move(self):
        # move the rect by the displacement ("speed")
        self.rect = self.rect.move(self.speed)

