import pygame, random

class Snake:
    def __init__(self, color):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.dir = "RIGHT"
        self.color = color

    def move(self):
        head = list(self.body[0])
        if self.dir == "RIGHT": head[0] += 10
        elif self.dir == "LEFT": head[0] -= 10
        elif self.dir == "UP": head[1] -= 10
        elif self.dir == "DOWN": head[1] += 10
        self.body.insert(0, head)

class Food:
    def __init__(self, f_type="normal", obstacles=[]):
        self.type = f_type
        self.spawn(obstacles)
        self.spawn_time = pygame.time.get_ticks()

    def spawn(self, obstacles):
        while True:
            self.pos = [random.randrange(0, 39)*10, random.randrange(0, 39)*10]
            if self.pos not in obstacles: break