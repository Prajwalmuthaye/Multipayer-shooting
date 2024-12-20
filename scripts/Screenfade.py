import pygame


class ScreenFade:
    def __init__(self, fade_type, color, speed):
        self.fade_type = fade_type  # 1 = fade in, 2 = fade out
        self.color = color  # The color of the fade (e.g., black, pink)
        self.speed = speed  # Speed of the fade (duration in frames)
        self.alpha = 255 if fade_type == 2 else 0  # Fade starts at 255 for fade-out or 0 for fade-in
        self.finished = False  # Flag to check if fade is done

    def update(self):
        if self.fade_type == 1:  # Fade in
            if self.alpha < 255:
                self.alpha += self.speed
            else:
                self.alpha = 255
                self.finished = True
        elif self.fade_type == 2:  # Fade out
            if self.alpha > 0:
                self.alpha -= self.speed
            else:
                self.alpha = 0
                self.finished = True

    def draw(self, screen):
        # Create a surface with the color and alpha value to simulate the fade
        fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
        fade_surface.fill(self.color)
        fade_surface.set_alpha(self.alpha)
        screen.blit(fade_surface, (0, 0))

    def is_finished(self):
        return self.finished
