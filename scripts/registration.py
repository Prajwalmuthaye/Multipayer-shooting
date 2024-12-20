import sys

import mysql.connector
import pygame
from lobby import player_dashboard
from login import login_screen  # Import login screen function

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Registration Page')

# Set up fonts
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)


background = pygame.image.load('reg.jpg')


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
        """Check if the button is clicked and if so, call the action"""
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()

    def check_hover(self, mouse_pos):
        """Change the hover state of the button"""
        self.is_hover = self.rect.collidepoint(mouse_pos)


# Function to handle user registration
def register_user(username, password):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='login_db'
        )

        cursor = connection.cursor()


        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()



        if result:
            return "Username already exists"

        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        connection.commit()

        cursor.close()
        connection.close()

        player_id =result[0]
        if result:
            return player_dashboard(player_id)

        return "Registration successful"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Database error occurred"


def show_registration():
    running = True
    username = ""
    password = ""
    confirm_password = ""
    active_input = None
    error_message = ""

    register_button = Button(300, 410, 200, 50, 'Register', button_font, BLUE, LIGHT_BLUE, None)
    back_button = Button(300, 480, 200, 50, 'Back to Login', button_font, BLUE, LIGHT_BLUE, login_screen)

    while running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))  # Background image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if register_button.rect.collidepoint(mouse_pos):
                    if username and password and confirm_password:
                        if password == confirm_password:
                            error_message = register_user(username, password)
                            if error_message == "Registration successful":
                                login_screen()
                        else:
                            error_message = "Passwords do not match"
                elif back_button.rect.collidepoint(mouse_pos):
                    login_screen()

                if pygame.Rect(250, 150, 300, 50).collidepoint(mouse_pos):
                    active_input = 'username'
                elif pygame.Rect(250, 250, 300, 50).collidepoint(mouse_pos):
                    active_input = 'password'
                elif pygame.Rect(250, 350, 300, 50).collidepoint(mouse_pos):
                    active_input = 'confirm_password'

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
                elif active_input == 'confirm_password':
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password = confirm_password[:-1]
                    else:
                        confirm_password += event.unicode
                elif event.key == pygame.K_RETURN:
                    if username and password and confirm_password:
                        if password == confirm_password:
                            error_message = register_user(username, password)
                            if error_message == "Registration successful":
                                login_screen()
                        else:
                            error_message = "Passwords do not match"

        # Draw input fields
        pygame.draw.rect(screen, GRAY, pygame.Rect(250, 150, 300, 50), border_radius=10)
        pygame.draw.rect(screen, GRAY, pygame.Rect(250, 250, 300, 50), border_radius=10)
        pygame.draw.rect(screen, GRAY, pygame.Rect(250, 350, 300, 50), border_radius=10)

        username_text = font.render(username, True, BLACK)
        screen.blit(username_text, (250 + 10, 150 + 10))

        password_text = font.render('*' * len(password), True, BLACK)
        screen.blit(password_text, (250 + 10, 250 + 10))

        confirm_password_text = font.render('*' * len(confirm_password), True, BLACK)
        screen.blit(confirm_password_text, (250 + 10, 350 + 10))

        # Draw labels
        label = font.render('Username:', True, WHITE)
        screen.blit(label, (250, 100))

        label = font.render('Password:', True, WHITE)
        screen.blit(label, (250, 200))

        label = font.render('Confirm Password:', True, WHITE)
        screen.blit(label, (250, 300))

        register_button.check_hover(pygame.mouse.get_pos())
        register_button.draw(screen)

        back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(screen)

        if error_message:
            error_text = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    show_registration()
