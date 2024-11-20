import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# Set display dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create display
dis = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Enhanced Platformer Game')

# Set clock
clock = pygame.time.Clock()

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False
        self.jump_count = 0  # For double jump

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x

        # Check for collision with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for platform in platform_hit_list:
            if self.change_x > 0:
                self.rect.right = platform.rect.left
            elif self.change_x < 0:
                self.rect.left = platform.rect.right

        self.rect.y += self.change_y

        # Check for collision with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for platform in platform_hit_list:
            if self.change_y > 0:
                self.rect.bottom = platform.rect.top
                self.change_y = 0
                self.on_ground = True
                self.jump_count = 0
            elif self.change_y < 0:
                self.rect.top = platform.rect.bottom
                self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.on_ground = True
            self.jump_count = 0

    def jump(self):
        if self.jump_count < 2:  # Double jump
            self.change_y = -10
            self.jump_count += 1

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

# Define platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define moving platform class
class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, range_x, range_y, speed_x, speed_y):
        super().__init__(x, y, width, height)
        self.start_x = x
        self.start_y = y
        self.range_x = range_x
        self.range_y = range_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction_x = 1
        self.direction_y = 1

    def update(self):
        self.rect.x += self.speed_x * self.direction_x
        self.rect.y += self.speed_y * self.direction_y
        if abs(self.rect.x - self.start_x) > self.range_x:
            self.direction_x *= -1
        if abs(self.rect.y - self.start_y) > self.range_y:
            self.direction_y *= -1

# Define disappearing platform class
class TemporaryPlatform(Platform):
    def __init__(self, x, y, width, height, lifetime):
        super().__init__(x, y, width, height)
        self.lifetime = lifetime

    def update(self):
        self.lifetime -= 1 / 60
        if self.lifetime <= 0:
            self.kill()

# Define spike class
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define rain class
class Rain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((2, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 5
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -10
            self.rect.x = random.randint(0, SCREEN_WIDTH)

# Define portal class
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define level class
class Level:
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.spike_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.weather_list = pygame.sprite.Group()
        self.portal_list = pygame.sprite.Group()
        self.player = player
        self.time_left = 30  # Time limit for each level

        # Add rain effect
        for _ in range(100):
            rain = Rain(random.randint(0, SCREEN_WIDTH), random.randint(-50, SCREEN_HEIGHT))
            self.weather_list.add(rain)

    def update(self):
        self.platform_list.update()
        self.spike_list.update()
        self.coin_list.update()
        self.weather_list.update()
        self.portal_list.update()

    def draw(self, screen):
        screen.fill(WHITE)
        self.platform_list.draw(screen)
        self.spike_list.draw(screen)
        self.coin_list.draw(screen)
        self.weather_list.draw(screen)
        self.portal_list.draw(screen)

        # Draw time left
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time Left: {int(self.time_left)}s", True, BLACK)
        screen.blit(time_text, (10, 10))

# Define specific levels
class Level_01(Level):
    def __init__(self, player):
        super().__init__(player)
        platforms = [
            [200, 500, 100, 20],
            [400, 400, 100, 20],
            [600, 300, 100, 20]
        ]
        for platform in platforms:
            block = Platform(*platform)
            self.platform_list.add(block)

        # Add moving platform
        moving_platform = MovingPlatform(300, 450, 100, 20, 150, 0, 2, 0)
        self.platform_list.add(moving_platform)

        # Add disappearing platform
        disappearing_platform = TemporaryPlatform(500, 350, 100, 20, 5)
        self.platform_list.add(disappearing_platform)

        # Add spikes
        spike = Spike(400, SCREEN_HEIGHT - 40, 40, 40)
        self.spike_list.add(spike)

        # Add coins
        coin = Coin(450, 350)
        self.coin_list.add(coin)

        # Add portal
        portal = Portal(700, 250, 50, 50)
        self.portal_list.add(portal)

class Level_02(Level):
    def __init__(self, player):
        super().__init__(player)
        platforms = [
            [150, 450, 100, 20],
            [350, 350, 100, 20],
            [550, 250, 100, 20]
        ]
        for platform in platforms:
            block = Platform(*platform)
            self.platform_list.add(block)

        # Add moving platform
        moving_platform = MovingPlatform(200, 400, 100, 20, 200, 0, 2, 0)
        self.platform_list.add(moving_platform)

        # Add disappearing platform
        disappearing_platform = TemporaryPlatform(500, 300, 100, 20, 5)
        self.platform_list.add(disappearing_platform)

        # Add spikes
        spike = Spike(300, SCREEN_HEIGHT - 40, 40, 40)
        self.spike_list.add(spike)

        # Add coins
        coin = Coin(350, 300)
        self.coin_list.add(coin)

        # Add portal
        portal = Portal(700, 200, 50, 50)
        self.portal_list.add(portal)

class Level_03(Level):
    def __init__(self, player):
        super().__init__(player)
        platforms = [
            [100, 400, 100, 20],
            [300, 300, 100, 20],
            [500, 200, 100, 20]
        ]
        for platform in platforms:
            block = Platform(*platform)
            self.platform_list.add(block)

        # Add moving platform
        moving_platform = MovingPlatform(150, 350, 100, 20, 250, 0, 2, 0)
        self.platform_list.add(moving_platform)

        # Add disappearing platform
        disappearing_platform = TemporaryPlatform(400, 250, 100, 20, 5)
        self.platform_list.add(disappearing_platform)

        # Add spikes
        spike = Spike(200, SCREEN_HEIGHT - 40, 40, 40)
        self.spike_list.add(spike)

        # Add coins
        coin = Coin(250, 250)
        self.coin_list.add(coin)

        # Add portal
        portal = Portal(700, 150, 50, 50)
        self.portal_list.add(portal)

# Main game loop
def main():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    level_list = [Level_01(player), Level_02(player), Level_03(player)]
    current_level_no = 0
    current_level = level_list[current_level_no]

    player.level = current_level
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_SPACE:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        player.update()
        current_level.update()

        # Check for coin collection
        coin_hit_list = pygame.sprite.spritecollide(player, current_level.coin_list, True)
        for coin in coin_hit_list:
            score += 10

        # Check for spike collision
        if pygame.sprite.spritecollide(player, current_level.spike_list, False):
            player.rect.x = 100
            player.rect.y = SCREEN_HEIGHT - player.rect.height

        # Check for portal collision
        portal_hit_list = pygame.sprite.spritecollide(player, current_level.portal_list, False)
        if portal_hit_list:
            current_level_no += 1
            if current_level_no >= len(level_list):
                current_level_no = 0
            current_level = level_list[current_level_no]
            player.rect.x = 100
            player.rect.y = SCREEN_HEIGHT - player.rect.height
            player.level = current_level

        # Check time limit
        current_level.time_left -= 1 / 60
        if current_level.time_left <= 0:
            print("Time's up! You lose!")
            pygame.quit()
            sys.exit()

        # Draw everything
        current_level.draw(dis)
        all_sprites.draw(dis)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        dis.blit(score_text, (10, 40))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()