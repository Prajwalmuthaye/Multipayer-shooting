import csv
import time

import button
import pygame
from game import World
from network import Network
from player import Player
from pygame import mixer
from Screenfade import ScreenFade
from tile_collision import check_tile_collision, draw_tile_map, load_tile_map

mixer.init()
pygame.font.init()

width = 800
height = 640
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
#background
pine1_img = pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\background\pine1.png').convert_alpha()
pine2_img = pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\background\pine2.png').convert_alpha()
mountain_img = pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\background\mountain.png').convert_alpha()
sky_img = pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\background\sky_cloud.png').convert_alpha()



shot_fx = pygame.mixer.Sound(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\audio\shot.wav')
shot_fx.set_volume(0.05)

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
# Tile size
TILE_SIZE = 32
bg_scroll = 0
TILE_TYPES = 21


grass_tile = pygame.image.load(r"C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\tile\21.png")  
water_tile = pygame.image.load(r"C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\tile\2.png") 
box=pygame.image.load(r"C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\tile\12.png") 

# Resize images to the tile size (32x32)
grass_tile = pygame.transform.scale(grass_tile, (TILE_SIZE, TILE_SIZE))
water_tile = pygame.transform.scale(water_tile, (TILE_SIZE, TILE_SIZE))
box = pygame.transform.scale(box, (TILE_SIZE, TILE_SIZE))


# Function to check if the player collides with a solid tile
def check_collision(x, y):
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE

    # Ensure we're within bounds of the tile map
    if 0 <= tile_x < len(tile_map[0]) and 0 <= tile_y < len(tile_map):
        if tile_map[tile_y][tile_x] == 2:  # 1 means solid tile
            return True
    return False


# Load the tile map from the CSV file
tile_map = load_tile_map()

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


def waiting_for_player(win):
    win.fill(BLACK)
    font = pygame.font.SysFont("", 40)
    text1 = font.render('Waiting for Player 2 to join...', 1, WHITE)
    win.blit(text1, (300, 300))
    pygame.display.update()


def draw_bg():
	win.fill(BG)
	width = sky_img.get_width()
	for x in range(5):
		win.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
		win.blit(mountain_img, ((x * width) - bg_scroll * 0.6, height - mountain_img.get_height() - 300))
		win.blit(pine1_img, ((x * width) - bg_scroll * 0.7, height - pine1_img.get_height() - 150))
		win.blit(pine2_img, ((x * width) - bg_scroll * 0.8, height - pine2_img.get_height()))


def redrawWindow(win,player, player2,timer_minutes,timer_seconds):
    win.fill((255,255,255))
	# Draw the tile map
    
    draw_bg()
    draw_tile_map(tile_map,win, water_tile, box)
    player.draw(win)
    player2.draw(win)
    for bullet in player.bullets:
            bullet.draw(win)
                
    font = pygame.font.SysFont("", 40)

    text1 = font.render('Score:'+ str(player.score),1,(0,0,0))
    text2 = font.render(':'+ str(player2.score),1,(0,0,0))
    win.blit(text1,(320,10))
    win.blit(text2,(420,10))

    
    # Display timer in minutes:seconds format
    timer_text = font.render(f'Time: {timer_minutes:02}:{timer_seconds:02}', 1, (0, 0, 0))
    win.blit(timer_text, (width - 150, 10))

    pygame.display.update()

def take_damage(player,damage):
        player.health -= damage
        print(f"Player health: {player.health}")
        print("hit")
        if player.health < 0:
            player.health = 0
            player.score +=1
            player.visible =False
            player.dead = True


#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

def respawn_player(player,x,y):
    if player.dead:  # Check if the player is dead
        player.dead = False
        player.health = 10  # Reset health
        player.visible = True
        player.x=100
        player.y =100



    
def display_win_screen(winner):
    
    button_font = pygame.font.Font(None, 36)
    font = pygame.font.SysFont("", 60)
    win_message = font.render(f"you loss!", 1, WHITE)
    youwin = font.render(f"you Win!", 1, WHITE)
    # Create the "Return to Lobby" button
    return_button = Button(
        x=300, y=400, width=200, height=50, text="back to Lobby",
        font=button_font, color=PINK, hover_color=RED, action= ''
    )

    # Create the fade screen effect (fade out to black initially)
    fade = ScreenFade(2, BLACK, 4)
    
    # Draw the fade effect before displaying the win screen
    while not fade.is_finished():
        fade.update()
        fade.draw(win)
        pygame.display.update()
        pygame.time.delay(10)
        
    # Display win or lose message
    if winner == 1:
        win.blit(youwin, (250, height // 2 - 100))
    elif winner == 2:
        win.blit(youwin, (250, height // 2 - 100))
    else:
        win.blit(win_message, (250, height // 2 - 100))
        
    # Draw the "Return to Lobby" button
    return_button.draw(win)
        
    print("game over")
    pygame.display.update()
    pygame.time.wait(3000)



def client_main():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()
    
    # Initialize game timer
    start_ticks = pygame.time.get_ticks() # Starting time in milliseconds
    time_limit = 300000

    respawn_delay = 3000  # Respawn delay in milliseconds (3 seconds)
    last_death_time = 0  # To track when the player last died
    winner = None

    

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    
        # Calculate the elapsed time
        elapsed_time = pygame.time.get_ticks() - start_ticks
        remaining_time = time_limit - elapsed_time
        
        # Calculate minutes and seconds
        minutes = remaining_time // 60000  # Convert milliseconds to minutes
        seconds = (remaining_time % 60000) // 1000  # Get the remaining seconds

        # Check if the timer has ended
        if remaining_time <= 0:
            # Game over or round end
            font = pygame.font.SysFont("", 60)
            game_over_text = font.render('Time is up! Game Over!', 1, (255, 0, 0))
            win.blit(game_over_text, (250, height // 2))
            pygame.display.update()
            pygame.time.wait(3000)  # Wait for 3 seconds before exiting
            run = False
            pygame.quit()
            


        for bullet in p.bullets[:]:
            player2_rect = pygame.Rect(p2.hitbox)
            if bullet.rect.colliderect( player2_rect):
                take_damage(p2, 1)
                print(f"Player 2 health after hit: {p2.health}")
                p.bullets.pop(p.bullets.index(bullet))
            if bullet.x < 0 or bullet.x > width or bullet.y < 0 or bullet.y > height:
                p.bullets.remove(bullet)
            else:
                bullet.move()
                shot_fx.play()
        
        for bullet in p2.bullets[:]:
            player2_rect = pygame.Rect(p.hitbox)
            if bullet.rect.colliderect( player2_rect):
                take_damage(p, 1)
                print(f"Player 2 health after hit: {p.health}")
                p2.bullets.pop(p2.bullets.index(bullet))

            if bullet.x < 0 or bullet.x > width or bullet.y < 0 or bullet.y > height:
                p2.bullets.remove(bullet)
            else:
                bullet.move()
                shot_fx.play()

        


        # Check if Player 1 or Player 2 won
        if p.score >= 2 and winner is None:  # Player 1 wins
            winner = 1
            display_win_screen(winner)  # Show Player 1's win screen
            
        if p2.score >= 2 and winner is None:  # Player 2 wins
            winner = 2
            display_win_screen(winner)  # Show Player 2's win screen
            
        # If player is dead and respawn delay has passed, respawn them
        if p.dead and pygame.time.get_ticks() - last_death_time > respawn_delay:
            respawn_player(p,0,575)
            pygame.time.get_ticks()  # Update last death time

        if p2.dead and pygame.time.get_ticks() - last_death_time > respawn_delay:
            respawn_player(p2,775,575)
            pygame.time.get_ticks()  # Update last death time


        if p:
            check_tile_collision(p,tile_map)
            p.move()
            
        else:
            p2.move()
        
        
        redrawWindow(win, p, p2,minutes, seconds)
        
        



