from os import supports_fd

from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 6
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft=position)
        self.hitbox_rect = self.rect.inflate(-10, -30)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2(0, 0)
        self.speed = 80
        self.death_time = 0
        self.death_duration = 200

    def animate(self, delta):
        self.frame_index += self.animation_speed * delta
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def move(self, delta):
        player_position = pygame.Vector2(self.player.rect.center)
        enemy_position = pygame.Vector2(self.rect.center)
        self.direction = (player_position - enemy_position).normalize()
        self.hitbox_rect.x += self.direction.x * self.speed * delta
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    def update(self, delta):
        if self.death_time == 0:
            self.move(delta)
            self.animate(delta)
        else:
            self.death_timer()

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        surface = pygame.mask.from_surface(self.frames[0]).to_surface()
        surface.set_colorkey('black')
        self.image = surface