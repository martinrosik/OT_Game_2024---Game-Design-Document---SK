import sys
from pytmx.util_pygame import load_pygame
from sprites import *
from player import Player
from groups import *
from enemy import *
from random import choice
from button import Button
from assets.items.healing import Heart
from darkmode import DarkMode
from assets.items.coin import Coin
from assets.items.crystal import Crystal
from assets.items.boots import Boots
from assets.items.book import Book
from assets.items.armor import Armor
import random


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tears of the Lizard King")
        self.all_sprites = AllSprites()
        self.enemy_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.snowball_sprites = pygame.sprite.Group()
        self.snowball_surface = pygame.image.load(join('assets', 'snowball', 'snowball.png')).convert_alpha()
        self.enemy_event = pygame.event.custom_type()
        self.enemy_spawn_delay = 1000
        self.max_enemies = 10
        self.player_has_armor = False
        self.selected_map = 'level1.tmx'
        pygame.time.set_timer(self.enemy_event, self.enemy_spawn_delay)
        self.enemy_spawn_positions = []
        self.enemy_frames = {}

        self.coin_spawn_positions = []
        self.health_spawn_positions = []
        self.armor_spawn_positions = []
        self.boots_spawn_position = []
        self.crystal_spawn_positions = []
        self.book_spawn_positions = []

        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 500

        self.shoot_snowball = pygame.mixer.Sound(join('assets', 'audio', 'snowball.mp3'))
        self.shoot_snowball.set_volume(0.6)
        self.impact_sound = pygame.mixer.Sound(join('assets', 'audio', 'enemy_hit.mp3'))
        self.impact_sound.set_volume(0.3)
        self.being_hit = pygame.mixer.Sound(join('assets', 'audio', 'being_hit.mp3'))
        self.being_hit.set_volume(0.2)
        self.healing_sound = pygame.mixer.Sound(join('assets', 'audio', 'heal.mp3'))
        self.healing_sound.set_volume(0.3)
        self.coin_pickup = pygame.mixer.Sound(join('assets', 'audio', 'coin_pickup.mp3'))
        self.coin_pickup.set_volume(0.1)
        self.crystal_pickup = pygame.mixer.Sound(join('assets', 'audio', 'crystal_pickup.mp3'))
        self.crystal_pickup.set_volume(0.1)
        self.crystal_spawn = pygame.mixer.Sound(join('assets', 'audio', 'crystal_spawn.wav'))
        self.crystal_spawn.set_volume(0.1)
        self.item_spawn = pygame.mixer.Sound(join('assets', 'audio', 'item_spawn.mp3'))
        self.item_spawn.set_volume(0.2)
        self.item_pickup = pygame.mixer.Sound(join('assets', 'audio', 'item_pickup.wav'))
        self.item_pickup.set_volume(0.2)
        self.armor_pickup = pygame.mixer.Sound(join('assets', 'audio', 'armor_pickup.mp3'))
        self.armor_pickup.set_volume(0.2)
        self.background_music = pygame.mixer.Sound(join('assets', 'audio', 'background_music.wav'))
        self.background_music.set_volume(0.01)
        self.background_music.play(loops=-1)

        self.map_enemy_types = {
            'level1.tmx': ['ogre', 'skeleton'],
            'level2.tmx': ['zombie', 'muddy'],
            'level3.tmx': ['demon', 'hellboy'],
            'level4.tmx': ['swampy', 'tree'],
            'level5.tmx': ['devil', 'chort']
        }

        self.setup_map(self.selected_map)
        self.load_enemies()
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_result = None

        self.start_time = pygame.time.get_ticks()
        self.timer_duration = 30 * 1000 * 6

        self.max_hearts = 5
        self.current_hearts = self.max_hearts
        self.heart_images = [
            pygame.image.load(join('assets', 'icons', 'heart_full.png')).convert_alpha()
            for _ in range(self.max_hearts)
        ]

        self.current_armor = 0
        self.max_armor = 1
        self.armor_images = []

        self.collision_cooldown = 2000
        self.last_collision_time = 0

        self.kills = 0
        self.kill_icon = pygame.image.load(join('assets', 'icons', 'kills.png')).convert_alpha()

        self.healing_sprites = pygame.sprite.Group()
        self.heart_surface = pygame.image.load(join('assets', 'icons', 'heart_full.png')).convert_alpha()
        self.healing_event = pygame.event.custom_type()
        self.healing_spawn_delay = 20000
        pygame.time.set_timer(self.healing_event, self.healing_spawn_delay)

        self.armor_sprites = pygame.sprite.Group()
        self.armor_surface = pygame.image.load(join('assets', 'icons', 'armor.png')).convert_alpha()
        self.armor_event = pygame.event.custom_type()
        self.armor_spawn_delay = 40000
        pygame.time.set_timer(self.armor_event, self.armor_spawn_delay)

        self.coin_sprites = pygame.sprite.Group()
        self.coin_surface = pygame.image.load(join('assets', 'icons', 'coin.png')).convert_alpha()
        self.coin_event = pygame.event.custom_type()
        self.coin_spawn_delay = 7000
        pygame.time.set_timer(self.coin_event, self.coin_spawn_delay)

        self.coin_count = 0

        self.crystal_sprites = pygame.sprite.Group()
        self.crystal_surface = pygame.image.load(join('assets', 'icons', 'crystal.png')).convert_alpha()
        self.crystal_event = pygame.event.custom_type()
        self.crystal_spawn_delay = 25000
        pygame.time.set_timer(self.crystal_event, self.crystal_spawn_delay)
        self.crystal_count = 0

        self.book_sprites = pygame.sprite.Group()
        self.book_surface = pygame.image.load(join('assets', 'icons', 'book.png')).convert_alpha()
        self.book_spawned = False
        self.book_spawn_time = random.randint(30 * 1000, 120 * 1000)

        self.boots_sprites = pygame.sprite.Group()
        self.boots_surface = pygame.image.load(join('assets', 'icons', 'boots.png')).convert_alpha()
        self.boots_spawned = False
        self.boots_spawn_time = random.randint(30 * 1000, 120 * 1000)

        self.dark_mode = DarkMode()
        self.dark_mode_event = pygame.event.custom_type()
        self.dark_mode_delay = random.randint(5000, 10000)
        pygame.time.set_timer(self.dark_mode_event, self.dark_mode_delay)

    def setup_map(self, map_file):
        map = load_pygame(join('assets', 'map', map_file))
        self.enemy_spawn_positions.clear()
        self.all_sprites.empty()
        self.collision_sprites.empty()

        for x, y, image in map.get_layer_by_name('terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for item in map.get_layer_by_name('objects non'):
            Sprite((item.x, item.y), item.image, self.all_sprites)
        for item in map.get_layer_by_name('objects'):
            if item.image is not None:
                CollisionSprite((item.x, item.y), item.image, (self.all_sprites, self.collision_sprites))
        for item in map.get_layer_by_name('collisions'):
            CollisionSprite((item.x, item.y), pygame.Surface((item.width, item.height)), self.collision_sprites)
        for item in map.get_layer_by_name('entities'):
            if item.name == 'Player':
                self.player = Player((item.x, item.y), self.all_sprites, self.collision_sprites)
            if item.name == 'Enemy':
                self.enemy_spawn_positions.append((item.x, item.y))
            if item.name == 'Coin':
                self.coin_spawn_positions.append((item.x, item.y))
            if item.name == 'Health':
                self.health_spawn_positions.append((item.x, item.y))
            if item.name == 'Crystal':
                self.crystal_spawn_positions.append((item.x, item.y))
            if item.name == 'Book':
                self.book_spawn_positions.append((item.x, item.y))
            if item.name == 'Boots':
                self.boots_spawn_position.append((item.x, item.y))
            if item.name == 'Armor':
                self.armor_spawn_positions.append((item.x, item.y))

    def load_enemies(self):
        folders = list(walk(join('assets', 'monsters')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            enemy_type = folder.lower()
            self.enemy_frames[enemy_type] = []
            for folder_path, _, file_names in walk(join('assets', 'monsters', folder)):
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surface = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[enemy_type].append(surface)

    def spawn_enemy(self):
        if len(self.enemy_sprites) < self.max_enemies:
            position = choice(self.enemy_spawn_positions)

            current_enemy_types = self.map_enemy_types.get(self.selected_map, [])
            if not current_enemy_types:
                return

            enemy_type_key = choice(current_enemy_types)
            enemy_type_frames = self.enemy_frames.get(enemy_type_key, [])

            if enemy_type_frames:
                Enemy(position, enemy_type_frames, (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

    def spawn_healing(self):
        if self.health_spawn_positions:
            position = choice(self.health_spawn_positions)
            Heart(self.heart_surface, position, (self.all_sprites, self.healing_sprites))

    def spawn_armor(self):
        if self.armor_spawn_positions:
            position = choice(self.armor_spawn_positions)
            Armor(self.armor_surface, position, (self.all_sprites, self.armor_sprites))
            self.item_spawn.play()

    def spawn_coin(self):
        if self.coin_spawn_positions:
            position = choice(self.coin_spawn_positions)
            Coin(self.coin_surface, position, (self.all_sprites, self.coin_sprites))

    def spawn_crystal(self):
        if self.crystal_spawn_positions:
            position = choice(self.crystal_spawn_positions)
            Crystal(self.crystal_surface, position, (self.all_sprites, self.crystal_sprites))
            self.crystal_spawn.play()

    def spawn_book(self):
        if not self.book_spawned and self.book_spawn_positions:
            position = choice(self.book_spawn_positions)
            Book(self.book_surface, position, (self.all_sprites, self.book_sprites))
            self.item_spawn.play()
            self.book_spawned = True

    def spawn_boots(self):
        if not self.boots_spawned and self.boots_spawn_position:
            position = choice(self.boots_spawn_position)
            Boots(self.boots_surface, position, (self.all_sprites, self.boots_sprites))
            self.item_spawn.play()
            self.boots_spawned = True


    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_snowball.play()
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            snowball_direction = (mouse_pos - player_pos).normalize()
            SnowBall(self.snowball_surface, self.player.rect.center, snowball_direction, (self.all_sprites, self.snowball_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def shooter_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.can_shoot = True

    def snowball_collision(self):
        if self.snowball_sprites:
            for snowball in self.snowball_sprites:
                collided_sprites = pygame.sprite.spritecollide(snowball, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collided_sprites:
                    for sprite in collided_sprites:
                        self.impact_sound.play()
                        sprite.destroy()
                        self.kills += 1
                    snowball.kill()

                if pygame.sprite.spritecollide(snowball, self.collision_sprites, False, pygame.sprite.collide_mask):
                    snowball.kill()

    def player_collision(self):
        current_time = pygame.time.get_ticks()
        if (
                pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_rect)
                and current_time - self.last_collision_time > self.collision_cooldown
        ):
            self.last_collision_time = current_time

            if self.current_armor > 0:
                self.current_armor -= 1
                self.armor_images.pop()
                self.being_hit.play()
            elif self.current_hearts > 0:
                self.current_hearts -= 1
                self.being_hit.play()

            if self.current_hearts == 0:
                self.game_result = "loss"
                self.running = False

    def player_pickup_healing(self):
        healing_items = pygame.sprite.spritecollide(self.player, self.healing_sprites, True, pygame.sprite.collide_mask)
        for heart in healing_items:
            if self.current_hearts < self.max_hearts:
                self.healing_sound.play()
                self.current_hearts += 1

    def player_pickup_armor(self):
        armor_items = pygame.sprite.spritecollide(self.player, self.armor_sprites, True, pygame.sprite.collide_mask)
        for armor in armor_items:
            if self.current_armor < self.max_armor:
                self.armor_pickup.play()
                self.current_armor += 1
                self.armor_images.append(pygame.image.load(join('assets', 'icons', 'armor.png')).convert_alpha())
                self.player_has_armor = True

    def player_pickup_coin(self):
        coins_collected = pygame.sprite.spritecollide(self.player, self.coin_sprites, True, pygame.sprite.collide_mask)
        for coin in coins_collected:
            self.coin_pickup.play()
            self.coin_count += 1

    def player_pickup_crystal(self):
        crystals_collected = pygame.sprite.spritecollide(self.player, self.crystal_sprites, True, pygame.sprite.collide_mask)
        for crystal in crystals_collected:
            self.crystal_pickup.play()
            self.crystal_count += 1

    def player_pickup_book(self):
        books_collected = pygame.sprite.spritecollide(self.player, self.book_sprites, True, pygame.sprite.collide_mask)
        for book in books_collected:
            self.item_pickup.play()
            new_timer = random.randint(1 * 60 * 1000, 6 * 60 * 1000)
            self.timer_duration = new_timer
            self.start_time = pygame.time.get_ticks()

    def player_pickup_boots(self):
        boots_collected = pygame.sprite.spritecollide(self.player, self.boots_sprites, True, pygame.sprite.collide_mask)
        for boot in boots_collected:
            self.item_pickup.play()
            self.player.speed = 170

    def draw_hearts(self):
        for i in range(self.current_hearts):
            self.display_surface.blit(self.heart_images[i], (10 + i * 40, 10))

    def draw_armor(self):
        for i in range(self.current_armor):
            self.display_surface.blit(self.armor_images[i], (220 + i * 40, 10))

    def draw_kill_count(self):
        self.display_surface.blit(self.kill_icon, (WINDOW_WIDTH - 160, 10))
        font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 40)
        kill_text = font.render(f"{self.kills}", True, pygame.Color('white'))
        self.display_surface.blit(kill_text, (WINDOW_WIDTH - 100, 30))

    def draw_coin_count(self):
        font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 30)
        coin_text = font.render(f"Coins: {self.coin_count}", True, pygame.Color('yellow'))
        self.display_surface.blit(coin_text, (10, 50))

    def draw_crystal_count(self):
        font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 30)
        crystal_text = font.render(f"Crystals: {self.crystal_count}", True, pygame.Color('purple'))
        self.display_surface.blit(crystal_text, (10, 70))

    def draw_timer(self):
        current_time = pygame.time.get_ticks()
        time_left = max(0, self.timer_duration - (current_time - self.start_time))
        minutes = time_left // 60000
        seconds = (time_left % 60000) // 1000
        timer_text = f"{minutes:02}:{seconds:02}"

        font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 40)
        timer_surface = font.render(timer_text, True, pygame.Color('white'))
        timer_rect = timer_surface.get_rect(center=(WINDOW_WIDTH // 2, 20))
        self.display_surface.blit(timer_surface, timer_rect)

        if time_left == 0 and self.current_hearts > 0:
            self.game_result = "win"
            self.running = False

    def start_screen(self):
        start = True
        font_choose_level = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 40)

        choose_level = font_choose_level.render("Choose level:", True, pygame.Color('white'))

        level1_button = Button(WINDOW_WIDTH // 2 - 260, WINDOW_HEIGHT // 2 - 150, 150, 50, pygame.Color('black'),
                             pygame.Color('green'), 'Level 1', 32)
        level2_button = Button(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 - 150, 150, 50, pygame.Color('black'),
                               pygame.Color('yellow'), 'Level 2', 32)
        level3_button = Button(WINDOW_WIDTH // 2 + 110, WINDOW_HEIGHT // 2 - 150, 150, 50, pygame.Color('black'),
                             pygame.Color('red'), 'Level 3', 32)
        level4_button = Button(WINDOW_WIDTH // 2 - 170, WINDOW_HEIGHT // 2 - 50, 150, 50, pygame.Color('black'),
                               pygame.Color('purple'), 'Level 4', 32)
        level5_button = Button(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 - 50, 150, 50, pygame.Color('black'),
                               pygame.Color('orange'), 'Level 5', 32)

        start_button = Button(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 50, 150, 50, pygame.Color('white'),
                              pygame.Color('grey'), 'Start', 32)


        background_image = pygame.image.load(join('assets', 'menu', 'menu_background.png')).convert()

        mode_selected = False
        mode_text = ''

        while start:
            self.display_surface.blit(background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    self.running = False
                    pygame.quit()
                    sys.exit()

            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if level1_button.is_pressed(mouse_position, mouse_pressed):
                self.max_enemies = 10
                self.enemy_spawn_delay = 1000
                self.selected_map = 'level1.tmx'
                pygame.time.set_timer(self.enemy_event, self.enemy_spawn_delay)
                mode_selected = True
                mode_text = 'You choose level 1'

            if level2_button.is_pressed(mouse_position, mouse_pressed):
                self.max_enemies = 20
                self.enemy_spawn_delay = 500
                self.selected_map = 'level2.tmx'
                pygame.time.set_timer(self.enemy_event, self.enemy_spawn_delay)
                mode_selected = True
                mode_text = 'You choose level 2'

            if level3_button.is_pressed(mouse_position, mouse_pressed):
                self.max_enemies = 30
                self.enemy_spawn_delay = 100
                self.selected_map = 'level3.tmx'
                pygame.time.set_timer(self.enemy_event, self.enemy_spawn_delay)
                mode_selected = True
                mode_text = 'You choose level 3'

            if level4_button.is_pressed(mouse_position, mouse_pressed):
                self.max_enemies = 30
                self.enemy_spawn_delay = 300
                self.selected_map = 'level4.tmx'
                pygame.time.set_timer(self.enemy_event, self.enemy_spawn_delay)
                mode_selected = True
                mode_text = 'You choose level 4'

            if level5_button.is_pressed(mouse_position, mouse_pressed):
                self.max_enemies = 30
                self.enemy_spawn_delay = 300
                self.selected_map = 'level5.tmx'
                pygame.time.set_timer(self.enemy_event, self.enemy_spawn_delay)
                mode_selected = True
                mode_text = 'You choose level 5'

            if start_button.is_pressed(mouse_position, mouse_pressed) and mode_selected:
                self.reset_game_state()
                self.setup_map(self.selected_map)
                start = False

            self.display_surface.blit(choose_level, (WINDOW_WIDTH // 2 - choose_level.get_width() // 2, 110))
            self.display_surface.blit(level1_button.image, level1_button.rect)
            self.display_surface.blit(level2_button.image, level2_button.rect)
            self.display_surface.blit(level3_button.image, level3_button.rect)
            self.display_surface.blit(level4_button.image, level4_button.rect)
            self.display_surface.blit(level5_button.image, level5_button.rect)
            self.display_surface.blit(start_button.image, start_button.rect)

            if mode_selected:
                font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 20)
                mode_message = font.render(mode_text, True, pygame.Color('white'))
                self.display_surface.blit(mode_message,
                                          (WINDOW_WIDTH // 2 - mode_message.get_width() // 2, WINDOW_HEIGHT // 2 + 120))

            pygame.display.update()

        if self.running:
            self.run()

    def game_over_screen(self):
        game_over = True
        font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 60)
        small_font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 40)

        while game_over:
            background_image = pygame.image.load(join('assets', 'menu', 'menu_background.png')).convert()
            self.display_surface.blit(background_image, (0, 0))
            game_over_text = font.render("GAME OVER", True, pygame.Color('red'))
            score_text = small_font.render(f"Score: {self.kills}", True, pygame.Color('white'))
            coin_text = small_font.render(f"Coins: {self.coin_count}", True, pygame.Color('yellow'))
            crystal_text = small_font.render(f"Crystals: {self.crystal_count}", True, pygame.Color('purple'))
            menu_button = Button(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 50, 150, 50, pygame.Color('white'),
                                 pygame.Color('grey'), 'Menu', 32)

            self.display_surface.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 150))
            self.display_surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 250))
            self.display_surface.blit(coin_text, (WINDOW_WIDTH // 2 - coin_text.get_width() // 2, 300))
            self.display_surface.blit(crystal_text, (WINDOW_WIDTH // 2 - crystal_text.get_width() // 2, 350))
            self.display_surface.blit(menu_button.image, menu_button.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if menu_button.is_pressed(mouse_position, mouse_pressed):
                game_over = False
                self.reset_game_state()
                self.running = True
                self.start_screen()

            pygame.display.update()
            self.clock.tick(60)

    def reset_game_state(self):
        self.current_hearts = self.max_hearts
        self.current_armor = 0
        self.kills = 0
        self.coin_count = 0
        self.crystal_count = 0
        self.start_time = pygame.time.get_ticks()
        self.all_sprites.empty()
        self.enemy_sprites.empty()
        self.collision_sprites.empty()
        self.snowball_sprites.empty()
        self.healing_sprites.empty()
        self.armor_images = []
        self.coin_spawn_positions = []
        self.health_spawn_positions = []
        self.armor_spawn_positions = []
        self.boots_spawn_position = []
        self.crystal_spawn_positions = []
        self.book_spawn_positions = []
        self.coin_sprites.empty()
        self.crystal_sprites.empty()
        self.setup_map(self.selected_map)
        self.book_spawned = False
        self.boots_spawned = False
        self.book_spawn_time = random.randint(30 * 1000, 120 * 1000)
        self.boots_spawn_time = random.randint(30 * 1000, 120 * 1000)
        self.timer_duration = 30 * 1000 * 6

    def winner_screen(self):
        winner = True
        font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 60)
        small_font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 40)

        while winner:
            background_image = pygame.image.load(join('assets', 'menu', 'menu_background.png')).convert()
            self.display_surface.blit(background_image, (0, 0))

            winner_text = font.render("WINNER!", True, pygame.Color('green'))
            score_text = small_font.render(f"Score: {self.kills}", True, pygame.Color('white'))
            coin_text = small_font.render(f"Coins: {self.coin_count}", True, pygame.Color('yellow'))
            crystal_text = small_font.render(f"Crystals: {self.crystal_count}", True, pygame.Color('purple'))
            menu_button = Button(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 50, 150, 50, pygame.Color('white'),
                                 pygame.Color('grey'), 'Menu', 32)

            self.display_surface.blit(winner_text, (WINDOW_WIDTH // 2 - winner_text.get_width() // 2, 150))
            self.display_surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 250))
            self.display_surface.blit(coin_text, (WINDOW_WIDTH // 2 - coin_text.get_width() // 2, 300))
            self.display_surface.blit(crystal_text, (WINDOW_WIDTH // 2 - crystal_text.get_width() // 2, 350))
            self.display_surface.blit(menu_button.image, menu_button.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if menu_button.is_pressed(mouse_position, mouse_pressed):
                winner = False
                self.reset_game_state()
                pygame.event.clear()
                self.running = True
                self.start_screen()

            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        while self.running:
            delta = self.clock.tick() / 1000
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == self.enemy_event:
                    self.spawn_enemy()
                if event.type == self.healing_event:
                    self.spawn_healing()
                if event.type == self.armor_event:
                    self.spawn_armor()
                if event.type == self.coin_event:
                    self.spawn_coin()
                if event.type == self.crystal_event:
                    self.spawn_crystal()
                if not self.book_spawned and elapsed_time >= self.book_spawn_time:
                    self.spawn_book()

                if not self.boots_spawned and elapsed_time >= self.boots_spawn_time:
                    self.spawn_boots()

                if event.type == self.dark_mode_event:
                    self.dark_mode.toggle(current_time)
                    pygame.time.set_timer(self.dark_mode_event, random.randint(10000, 160000))

            self.input()
            self.snowball_collision()
            self.player_collision()
            self.player_pickup_healing()
            self.player_pickup_armor()
            self.player_pickup_coin()
            self.player_pickup_crystal()
            self.player_pickup_book()
            self.player_pickup_boots()
            self.shooter_timer()
            self.dark_mode.update(current_time)

            self.display_surface.fill(('lightskyblue4'))
            self.all_sprites.draw(self.player.rect.center)
            self.all_sprites.update(delta)

            self.dark_mode.render(self.display_surface)

            self.draw_hearts()
            self.draw_armor()
            self.draw_coin_count()
            self.draw_crystal_count()
            self.draw_kill_count()
            self.draw_timer()
            pygame.display.update()

        if self.game_result == "win":
            self.winner_screen()
        elif self.game_result == "loss":
            self.game_over_screen()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.start_screen()
