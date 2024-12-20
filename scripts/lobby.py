import sys

import mysql.connector
import pygame
from client import client_main

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Player Dashboard')

# Set up fonts
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)

# Background Image (Replace with your background image)
background = pygame.image.load('bg.jpg')  # Ensure you have an image named 'background.jpg'

bg_image = pygame.transform.scale(background, (WIDTH, HEIGHT)) 
# Define Button Class
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hover = False

    def draw(self, screen):
        color = self.hover_color if self.is_hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)  # Rounded corners
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2))

    def check_click(self, mouse_pos):
        """Check if the button is clicked and if so, call the action"""
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()

    def check_hover(self, mouse_pos):
        """Change the hover state of the button"""
        self.is_hover = self.rect.collidepoint(mouse_pos)


# Function to fetch the player's username from the database
def get_player_info(player_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='login_db'
        )
        cursor = connection.cursor()

        cursor.execute('SELECT username FROM users WHERE id = %s', (player_id,))
        player = cursor.fetchone()
        
        cursor.close()
        connection.close()

    
        return player if player else None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# Function to start the game (or lobby)
def start_game():
    client_main()
    # This could be a function that takes you to the game screen or a lobby.


# Function to handle player logout
def logout():
    print("Logging out...")
    pygame.quit()
    sys.exit()


# Player Dashboard Page after successful login
def player_dashboard(player_id):
    running = True
    username = get_player_info(player_id)

    if not username:
        print("Player not found!")
        pygame.quit()
        sys.exit()

    # Create buttons for Play and Logout
    play_button = Button(20, 575, 200, 50, 'Play', button_font, BLUE, LIGHT_BLUE, start_game)
    logout_button = Button(580, 575, 200, 50, 'Logout', button_font, BLUE, LIGHT_BLUE, logout)

    while running:
        screen.fill(WHITE)
        screen.blit(bg_image, (0, 0))  # Background image

        # Display the player's username
        username_text = font.render(f'Welcome {username}', True, WHITE)
        screen.blit(username_text, (WIDTH // 2 - username_text.get_width() // 2, 100))

        # Handle button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                play_button.check_click(mouse_pos)
                logout_button.check_click(mouse_pos)

            # Hover state handling
            play_button.check_hover(pygame.mouse.get_pos())
            logout_button.check_hover(pygame.mouse.get_pos())

        # Draw the Play and Logout buttons
        play_button.draw(screen)
        logout_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Simulate a successful login and redirect to player dashboard
    player_id = 1  # Assume the player_id is 1 after successful login
    player_dashboard(player_id)
