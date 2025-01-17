from settings import *

class Armor(pygame.sprite.Sprite):
    def __init__(self, surface, position, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 60000

    def update(self, delta):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
