from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)

class SnowBall(pygame.sprite.Sprite):
    def __init__(self, surface, position, direction, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.direction = direction
        self.speed = 300
        self.lifetime = 1000
        self.spawn_time = pygame.time.get_ticks()

    def update(self, delta):
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        self.rect.center += self.direction * self.speed * delta



