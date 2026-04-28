import pygame, random

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_color, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.color = image_color
        pygame.draw.rect(self.image, self.color, (0, 0, width, height))
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600: self.kill()

class Enemy(GameObject):
    def __init__(self, speed):
        super().__init__((255, 0, 0), 40, 70, speed)
        self.rect.x = random.randint(50, 310)
        self.rect.y = -100

class Obstacle(GameObject):
    def __init__(self, speed):
        self.type = random.choice(['oil', 'barrier', 'pothole'])
        color = (50, 50, 50) if self.type == 'oil' else (139, 69, 19)
        super().__init__(color, 35, 35, speed)
        self.rect.x = random.randint(50, 310)
        self.rect.y = -100

class PowerUp(GameObject): 
    def __init__(self, p_type):
        self.p_type = p_type
        colors = {'nitro': (255, 69, 0), 'shield': (0, 191, 255), 'repair': (50, 255, 50)}
        super().__init__(colors[p_type], 30, 30, 5)
        self.rect.x = random.randint(50, 310)
        self.rect.y = -100
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        super().update()
        if pygame.time.get_ticks() - self.spawn_time > 5000: self.kill() 