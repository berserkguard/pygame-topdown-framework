import pygame
import sys
import os
from game import *
from config import *

def main():
    # initialize pygame
    pygame.init()

    # create the window
    screen = pygame.display.set_mode((Config.width, Config.height))

    # set the window title
    pygame.display.set_caption("The Last Robot")


    clock = pygame.time.Clock()

    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            # quit if the user closes the window
            if event.type == pygame.QUIT:
                running = False
                
        game.render()
        
        pygame.display.flip()
            

if __name__ == '__main__':
    main()
