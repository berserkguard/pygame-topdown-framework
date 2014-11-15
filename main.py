import pygame
import sys
import os
from game import *

def main():
    # initialize pygame
    pygame.init()

    clock = pygame.time.Clock()

    game = Game()

    # create the window
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    # set the window title
    pygame.display.set_caption("The Last Robot")

    running = True
    while running:
        for event in pygame.event.get():
            # quit if the user closes the window
            if event.type == pygame.QUIT:
                running = False
            
        pygame.display.flip()
            

if __name__ == '__main__':
    main()
