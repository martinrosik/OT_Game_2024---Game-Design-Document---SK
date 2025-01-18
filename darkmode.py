from settings import *
import random

class DarkMode:
    def __init__(self):
        self.active = False
        self.start_time = 0
        self.duration = 5000
        self.dark_image = pygame.image.load(join('assets', 'icons', 'dark.png')).convert_alpha()
        self.dark_image_torch = pygame.image.load(join('assets', 'icons', 'dark_torch.png')).convert_alpha()
        self.torch_active = False

    def toggle(self, current_time):
        if not self.active:
            self.active = True
            self.start_time = current_time

    def update(self, current_time):
        if self.active and not self.torch_active and current_time - self.start_time >= self.duration:
            self.active = False

    def render(self, surface):
        if self.active:
            if self.torch_active:
                surface.blit(self.dark_image_torch, (0, 0))
            else:
                surface.blit(self.dark_image, (0, 0))

