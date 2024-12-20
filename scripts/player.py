
import pygame
from projectile import Projectile
from tile_collision import load_tile_map

idleimage=[pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\Idle\0.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\Idle\1.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\Idle\2.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\Idle\3.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\Idle\4.png')]
runRight = [pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\rightRun\0.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\rightRun\1.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\rightRun\2.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\rightRun\3.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\rightRun\4.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\rightRun\5.png')]
runLeft =[pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\LeftRun\0.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\LeftRun\1.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\LeftRun\2.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\LeftRun\3.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\LeftRun\4.png'),pygame.image.load(r'C:\Users\fools\PycharmProjects\multiplayershooter\scripts\img\player\LeftRun\5.png')]

# Load the tile map from the CSV file
tile_map = load_tile_map()

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 3
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, 18, 40)
        self.score = 0
        self.bullets = []
        self.health = 10
        self.visible = True
        self.gravity = 0.75
        self.jump = False
        self.in_air = True
        self.vel_y=0
        self.dead =False
        self.position =(self.x,self.y)


    def playerHealth(self,win):
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
    
    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >= len(runRight) * 3:
                self.walkCount = 0
            if not self.standing:
                if self.right:
                    win.blit(runRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                elif self.left:
                    win.blit(runLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(runRight[0], (self.x, self.y))
                else:
                    win.blit(runLeft[0], (self.x, self.y))
            self.playerHealth(win)
            self.hitbox = (self.x, self.y, 28, 40)  # Update hitbox size for collisions

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.right = False
            self.left = True
            self.standing = False
        elif keys[pygame.K_RIGHT] and self.x < 775:
            self.x += self.vel
            self.left = False
            self.right = True
            self.standing = False
        else:
            self.standing = True
            self.walkCount = 0

        if keys[pygame.K_UP] and self.y > self.vel:
            self.vel_y = -12
            self.in_air = True
            self.y -= self.vel

        if keys[pygame.K_DOWN]and self.y < 575:
            self.y += self.vel

        """
        # Apply gravity
        if self.in_air:
            self.vel_y += self.gravity
            if self.vel_y > 10:
                self.vel_y = 10
        else:
            self.vel_y = 0

        # Update Y position with gravity and jumping
        self.y += self.vel_y
        if self.y >= 575:
            self.y = 575
            self.in_air = False
        """

        if keys[pygame.K_SPACE]:
            if self.left:
                Projectile.facing = -1
            else:
                Projectile.facing = 1
            
            if len(self.bullets) < 5:
                self.bullets.append(Projectile(self.x + self.width-16, self.y + ((self.height//2)-8), 2, (0, 255, 0), Projectile.facing))

    def update(self):
        self.move()
