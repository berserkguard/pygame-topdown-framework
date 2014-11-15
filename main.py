import pygame
import sys
import os
from game import *
from config import *

def main():
    # Initialize Pygame
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((Config.width, Config.height))
    pygame.display.set_caption("The Last Robot")

    clock = pygame.time.Clock()

    game = Game()

    running = True
    while running:
        # Time since last frame (in seconds)
        delta = clock.tick() / 1000.0
        
        # Handle Pygame events
        for event in pygame.event.get():
            # Quit if the user closed the window
            if event.type == pygame.QUIT:
                running = False
        
        # Update the game
        game.update(delta)
        
        # Clear the screen & render the game
        screen.fill((0, 0, 0))
        game.render()
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()
