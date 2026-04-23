import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 400, 600
SPEED = 5
COIN_SCORE = 0

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Racer Practice 10')
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH-40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy_group):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.enemy_group = enemy_group 
        self.spawn()

    def spawn(self):
        """Тиынды бос орынға қою функциясы"""
        while True:
            self.rect.center = (random.randint(40, WIDTH-40), -50)
            if not pygame.sprite.spritecollideany(self, self.enemy_group):
                break

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > HEIGHT):
            self.spawn() 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 70))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:        
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)


E1 = Enemy()
enemies = pygame.sprite.Group()
enemies.add(E1)

C1 = Coin(enemies)
coins = pygame.sprite.Group()
coins.add(C1)

P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    
    scores = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    screen.blit(scores, (WIDTH - 110, 10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += 1
        C1.spawn() 

    if pygame.sprite.spritecollideany(P1, enemies):
        screen.fill(RED)
        msg = font_big.render("GAME OVER", True, BLACK)
        screen.blit(msg, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(60)