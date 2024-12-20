import sys

import mysql.connector
import pygame
from lobby import player_dashboard

#from lobby import player_dashboard

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Login Page')

# Set up fonts
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Background Image
background = pygame.image.load('reg.jpg')

# Define a button class
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
        pygame.draw.rect(screen, color, self.rect, border_radius=10) 
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2))

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()

    def check_hover(self, mouse_pos):
        self.is_hover = self.rect.collidepoint(mouse_pos)


# Function to handle user login
def login_user(username, password):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='login_db'
        )
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        player_id= result[0]
        
        if result:
            return player_dashboard(player_id)
        else:
            return "Invalid username or password"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Database error occurred"


def login_screen():
    running = True
    username = ""
    password = ""
    active_input = None
    error_message = ""

    login_button = Button(300, 400, 200, 50, 'Login', button_font, BLUE, LIGHT_BLUE, None)

    while running:
        screen.fill(WHITE)
        screen.blit(background, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if login_button.rect.collidepoint(mouse_pos):
                    # Process login
                    if username and password:
                        error_message = login_user(username, password)
                        print(error_message)
                if pygame.Rect(250, 150, 300, 50).collidepoint(mouse_pos):
                    active_input = 'username'
                elif pygame.Rect(250, 250, 300, 50).collidepoint(mouse_pos):
                    active_input = 'password'

            elif event.type == pygame.KEYDOWN:
                if active_input == 'username':
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif active_input == 'password':
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode
                elif event.key == pygame.K_RETURN:
                    if username and password:
                        player_id=login_user(username, password)
                        if player_id:
                            player_dashboard(player_id)


        pygame.draw.rect(screen, GRAY, pygame.Rect(250, 150, 300, 50), border_radius=10)
        pygame.draw.rect(screen, GRAY, pygame.Rect(250, 250, 300, 50), border_radius=10)


        username_text = font.render(username, True, BLACK)
        screen.blit(username_text, (250 + 10, 150 + 10))

        password_text = font.render('*' * len(password), True, BLACK) 
        screen.blit(password_text, (250 + 10, 250 + 10))

        # Draw labels
        label = font.render('Username:', True, WHITE)
        screen.blit(label, (250, 100))

        label = font.render('Password:', True, WHITE)
        screen.blit(label, (250, 210))


        login_button.check_hover(pygame.mouse.get_pos())
        login_button.draw(screen)

        if error_message:
            error_text = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    login_screen()
