from settings import *

class Achievement:
    def __init__(self, name, description, image_path, condition):
        self.name = name
        self.description = description
        self.image = pygame.image.load(image_path).convert_alpha()
        self.unlocked = False
        self.condition = condition

class AchievementSystem:
    def __init__(self, game):
        self.game = game
        self.achievements = []
        self.notification_duration = 3000
        self.notification_start_time = None
        self.current_notification = None

        self.add_achievement(
            "First Blood", "Kill your first enemy.", join('assets', 'achievements', 'first_blood.png'),
            lambda game: game.kills >= 1
        )
        self.add_achievement(
            "Coin Collector", "Collect 20 coins.", join('assets', 'achievements', 'coin_collector.png'),
            lambda game: game.coin_count >= 20
        )
        self.add_achievement(
            "Crystal Master", "Collect 10 crystals.", join('assets', 'achievements', 'crystal_master.png'),
            lambda game: game.crystal_count >= 10
        )
        self.add_achievement(
            "Armor Up", "Collect your first piece of armor.", join('assets', 'achievements', 'armor_up.png'),
            lambda game: game.armor_picked_up
        )
        self.add_achievement(
            "Speedster", "Pick up the boots.", join('assets', 'achievements', 'speedster.png'),
            lambda game: game.boots_picked_up
        )
        self.add_achievement(
            "Torchbearer", "Pick up the torch.", join('assets', 'achievements', 'torchbearer.png'),
            lambda game: game.torch_picked_up
        )
        self.add_achievement(
            "Bookworm", "Collect the magic book.", join('assets', 'achievements', 'bookworm.png'),
            lambda game: game.book_picked_up
        )
        self.add_achievement(
            "Survivor", "Survive for 7 minutes.", join('assets', 'achievements', 'survivor.png'),
            lambda game: pygame.time.get_ticks() - game.start_time >= 7 * 60 * 1000
        )
        self.add_achievement(
            "Killer", "Defeat 250 enemies.", join('assets', 'achievements', 'killer.png'),
            lambda game: game.kills >= 250
        )
        self.add_achievement(
            "Champion", "Win the game.", join('assets', 'achievements', 'champion.png'),
            lambda game: game.game_result == "win"
        )

    def add_achievement(self, name, description, image_path, condition):
        self.achievements.append(Achievement(name, description, image_path, condition))

    def check_achievements(self):
        for achievement in self.achievements:
            if not achievement.unlocked and achievement.condition(self.game):
                achievement.unlocked = True
                self.notify(achievement)

    def notify(self, achievement):
        self.current_notification = achievement
        self.notification_start_time = pygame.time.get_ticks()

    def draw_notification(self, surface):
        if self.current_notification:
            current_time = pygame.time.get_ticks()
            if current_time - self.notification_start_time < self.notification_duration:
                image_rect = self.current_notification.image.get_rect(center=(surface.get_width() // 2, 80))
                surface.blit(self.current_notification.image, image_rect)
            else:
                self.current_notification = None

    def show_achievements_menu(self, surface, clock):
        menu_open = True
        font = pygame.font.Font(join('assets', 'fonts', 'game_font.ttf'), 30)
        background_image = pygame.image.load(join('assets', 'menu', 'menu_background.png')).convert()

        while menu_open:
            surface.blit(background_image, (0, 0))
            title_text = font.render("Achievements", True, pygame.Color('gold'))
            surface.blit(title_text, (surface.get_width() // 2 - title_text.get_width() // 2, 50))

            y_offset = 120
            for achievement in self.achievements:
                status = "Unlocked" if achievement.unlocked else "Locked"
                status_color = pygame.Color('green') if achievement.unlocked else pygame.Color('red')
                name_text = font.render(achievement.name, True, status_color)
                desc_text = font.render(achievement.description, True, pygame.Color('white'))
                surface.blit(name_text, (100, y_offset))
                surface.blit(desc_text, (400, y_offset))
                y_offset += 50

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_open = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_open = False

            pygame.display.update()
            clock.tick(60)
