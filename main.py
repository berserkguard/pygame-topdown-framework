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
        
        # Update & render the game
        screen.fill((0, 0, 0))
        if game.update(delta):
            # Game over!
            game.message_util.render_text(screen, "You died!", Config.width / 2, 300, game.message_util.big_font, (255, 0, 0), True)
            
            timer_text = "Time Lasted: %02d:%02d" % (int(game.timer / 60), int(game.timer) % 60)
            game.message_util.render_text(screen, timer_text, Config.width / 2, 370, game.message_util.big_font, (0, 255, 0), True)
            
            #game.message_util.render_text(screen, "Press Enter to restart!", Config.width / 2, 500, game.message_util.big_font, (255, 255, 255), True)
        else:
            # Clear the screen & render the game
            game.render()
            
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()
