import sys

import pygame
from registration import show_registration

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Home Page')

# Set up fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load background image
bg_image = pygame.image.load('bg.jpg')  # Replace with your background image path
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  # Resize to fit screen



# Define a button class
class Button:
    def __init__(self, x, y, width, height, text, font, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2))

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()

# Action when button is clicked
def start_game():
    show_registration()

    # Here, you can add code to transition to the game screen

# Create button
start_button = Button(300, 400, 200, 50, 'Start Game', button_font, BLUE, start_game) 

# Main loop
running = True
while running:
    # Draw background image
    screen.blit(bg_image, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            start_button.check_click(mouse_pos)

    # Draw text
    #title_text = font.render('Welcome to the Game!', True, BLACK)
    #screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    # Draw button
    start_button.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
