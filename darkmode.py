from settings import *
import random

class DarkMode:
    def __init__(self):
        self.active = False
        self.start_time = 0
        self.duration = 5000
        self.dark_image = pygame.image.load(join('assets', 'icons', 'dark.png')).convert_alpha()

    def toggle(self, current_time):
        if not self.active:
            self.active = True
            self.start_time = current_time

    def update(self, current_time):
        if self.active and current_time - self.start_time >= self.duration:
            self.active = False

    def render(self, surface):
        if self.active:
            surface.blit(self.dark_image, (0, 0))
