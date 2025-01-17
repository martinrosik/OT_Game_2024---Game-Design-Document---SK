from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites):
        super().__init__(groups)

        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        self.load_images()
        self.state = 'down'
        self.frame_index = 0
        self.image = pygame.image.load(join('assets', 'player', self.state, '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=position)
        self.hitbox_rect = self.rect.inflate(-40, -40)

        self.direction = pygame.Vector2(0, 0)
        self.speed = 150
        self.collision_sprites = collision_sprites

        self.animation_speed = 0.2
        self.animation_timer = 0

    def load_images(self):
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('assets', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surface = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surface)

    def animate(self, delta):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.animation_timer += delta
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.state])

        self.image = self.frames[self.state][int(self.frame_index)]

    def move(self, delta):
        self.hitbox_rect.x += self.direction.x * delta * self.speed
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * delta * self.speed
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

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s])-int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def update(self, delta):
        self.input()
        self.move(delta)
        self.animate(delta)




