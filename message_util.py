import pygame
from config import *

class Message():
    def __init__(self, msg_text, color):
        self.msg_text = msg_text
        self.color = color # 4-tuple (r, g, b, a)
        self.x = Config.message_x
        self.y = Config.message_y
        self.time_passed = 0
    
    # Updates message. Returns true when message should be removed. 
    def update(self, delta):
        self.time_passed += delta
        self.y -= Config.message_scroll_speed * delta
        
        return self.time_passed >= Config.message_duration

class MessageUtil():
    def __init__(self):
        self.font = pygame.font.Font("assets/booterzz.ttf", 36)
        self.big_font = pygame.font.Font("assets/booterzz.ttf", 60)
        self.messages = []
    
    def add_message(self, message):
        if message not in self.messages:
            self.messages.append(message)
        
    def update(self, delta):
        messages_to_remove = []
        for message in self.messages:
            if message.update(delta):
                messages_to_remove.append(message)
        
        for message in messages_to_remove:
            self.messages.remove(message)
    
    def render_text(self, screen, text, x_pos, y_pos, font, color):
        label_width, label_height = font.size(text)

        # Render outline
        outline = font.render(text, 1, (0, 0, 0))
        screen.blit(outline, (x_pos - 2, y_pos - 2))
        screen.blit(outline, (x_pos - 2, y_pos))
        screen.blit(outline, (x_pos + 2, y_pos))
        screen.blit(outline, (x_pos + 2, y_pos + 2))
        screen.blit(outline, (x_pos + 2, y_pos - 2))
        screen.blit(outline, (x_pos - 2, y_pos + 2))
        screen.blit(outline, (x_pos, y_pos + 2))
        screen.blit(outline, (x_pos, y_pos - 2))
        
        # Render message
        label = font.render(text, 1, color)
        screen.blit(label, (x_pos, y_pos))
    
    def render(self, screen):
        for message in self.messages:
            label_width, label_height = self.font.size(message.msg_text)
            
            x_pos = message.x - label_width / 2
            y_pos = message.y - label_height / 2
            
            self.render_text(screen, message.msg_text, x_pos, y_pos, self.font, message.color)
