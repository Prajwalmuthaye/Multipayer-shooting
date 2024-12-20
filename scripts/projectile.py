import pygame


class Projectile:
    facing = 1

    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
    
    def move(self):
        self.x += self.facing * 10  # Update x position based on facing direction
        self.rect.x = self.x  # Update rect position for collision detection

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)