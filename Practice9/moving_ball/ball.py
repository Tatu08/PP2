import pygame

class Ball:
    def __init__(self, x, y, screen_w, screen_h):
        self.x = x
        self.y = y
        self.radius = 25
        self.step = 20
        self.w = screen_w
        self.h = screen_h

    def move(self, direction):
        if direction == "up":
            if self.y - self.radius - self.step >= 0:
                self.y -= self.step
        elif direction == "down":
            if self.y + self.radius + self.step <= self.h:
                self.y += self.step
        elif direction == "left":
            if self.x - self.radius - self.step >= 0:
                self.x -= self.step
        elif direction == "right":
            if self.x + self.radius + self.step <= self.w:
                self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)