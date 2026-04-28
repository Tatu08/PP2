import pygame
import random
import sys
from db import save_score, get_personal_best 

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

# Түстер
WHITE = (255, 255, 255)
RED = (213, 50, 80)     
DARK_RED = (100, 0, 0)   
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)   

class SnakeGame:
    def __init__(self, username):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake TSIS 4 - Full Integration')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("bahnschrift", 25)
        
        self.username = username
        self.personal_best = get_personal_best(username) 
        self.reset_game()

    def reset_game(self):
        self.snake_pos = [WIDTH / 2, HEIGHT / 2]
        self.snake_body = [[WIDTH / 2, HEIGHT / 2]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        
        self.score = 0
        self.level = 1
        self.speed = 10
        self.obstacles = [] 
        
        self.generate_food()
        self.generate_poison() 
        self.game_over = False

    def generate_food(self):
        while True:
            x = random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE
            y = random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE
            pos = [x, y]
            if pos not in self.snake_body and pos not in self.obstacles:
                self.food_pos = pos
                break
        self.food_weight = random.randint(1, 3)

    def generate_poison(self): 
        while True:
            x = random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE
            y = random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE
            pos = [x, y]
            if pos not in self.snake_body and pos != self.food_pos and pos not in self.obstacles:
                self.poison_pos = pos
                break

    def display_ui(self):
        value = self.font.render(f"Score: {self.score}  Level: {self.level}  Best: {self.personal_best}", True, WHITE)
        self.screen.blit(value, [10, 10])

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != 'DOWN': self.change_to = 'UP'
                    if event.key == pygame.K_DOWN and self.direction != 'UP': self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT and self.direction != 'RIGHT': self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT and self.direction != 'LEFT': self.change_to = 'RIGHT'

            self.direction = self.change_to

            if self.direction == 'UP': self.snake_pos[1] -= BLOCK_SIZE
            if self.direction == 'DOWN': self.snake_pos[1] += BLOCK_SIZE
            if self.direction == 'LEFT': self.snake_pos[0] -= BLOCK_SIZE
            if self.direction == 'RIGHT': self.snake_pos[0] += BLOCK_SIZE

            if (self.snake_pos[0] >= WIDTH or self.snake_pos[0] < 0 or 
                self.snake_pos[1] >= HEIGHT or self.snake_pos[1] < 0 or 
                list(self.snake_pos) in self.snake_body[1:] or 
                list(self.snake_pos) in self.obstacles):
                self.game_over = True

            self.snake_body.insert(0, list(self.snake_pos))

            if self.snake_pos == self.food_pos:
                self.score += self.food_weight 
                if self.score // 5 >= self.level:
                    self.level += 1
                    self.speed += 2
                    if self.level >= 3: 
                        new_obs = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE, 
                                   random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
                        self.obstacles.append(new_obs)
                self.generate_food()
                self.generate_poison() 
            elif self.snake_pos == self.poison_pos: 
                if len(self.snake_body) > 2:
                    self.snake_body.pop(); self.snake_body.pop() 
                    self.generate_poison()
                else:
                    self.game_over = True
            else:
                self.snake_body.pop()

            self.screen.fill(BLACK)
            for pos in self.snake_body:
                pygame.draw.rect(self.screen, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            for obs in self.obstacles:
                pygame.draw.rect(self.screen, GRAY, (obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))
            
            pygame.draw.rect(self.screen, RED, (self.food_pos[0], self.food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, DARK_RED, (self.poison_pos[0], self.poison_pos[1], BLOCK_SIZE, BLOCK_SIZE))

            self.display_ui()
            pygame.display.flip()
            self.clock.tick(self.speed)

        save_score(self.username, self.score, self.level)
        self.show_game_over_screen()

    def show_game_over_screen(self):
        self.screen.fill(BLACK)
        msg = self.font.render(f"GAME OVER! Score: {self.score}. Press C to Restart or Q to Quit", True, RED)
        self.screen.blit(msg, [WIDTH/8, HEIGHT/2])
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit(); sys.exit()
                    if event.key == pygame.K_c:
                        self.reset_game(); self.run(); return

if __name__ == "__main__":
    name = input("Enter username: ") 
    game = SnakeGame(name)
    game.run()