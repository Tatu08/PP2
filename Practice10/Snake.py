import pygame
import random
import time

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 102)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Practice 10')
        self.clock = pygame.time.Clock()
        
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.reset_game()

    def reset_game(self):
        self.snake_pos = [WIDTH / 2, HEIGHT / 2]
        self.snake_body = [[WIDTH / 2, HEIGHT / 2]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        
        self.score = 0
        self.level = 1
        self.speed = 10
        self.food_pos = self.generate_food()
        self.game_over = False

    def generate_food(self):
        while True:
            x = random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE
            y = random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE
            pos = [x, y]
            
            if pos not in self.snake_body:
                return pos

    def display_score(self):
        value = self.font_style.render(f"Score: {self.score}  Level: {self.level}", True, YELLOW)
        self.screen.blit(value, [10, 10])

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != 'DOWN':
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN and self.direction != 'UP':
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                        self.change_to = 'RIGHT'

            self.direction = self.change_to

            if self.direction == 'UP': self.snake_pos[1] -= BLOCK_SIZE
            if self.direction == 'DOWN': self.snake_pos[1] += BLOCK_SIZE
            if self.direction == 'LEFT': self.snake_pos[0] -= BLOCK_SIZE
            if self.direction == 'RIGHT': self.snake_pos[0] += BLOCK_SIZE

            if (self.snake_pos[0] >= WIDTH or self.snake_pos[0] < 0 or 
                self.snake_pos[1] >= HEIGHT or self.snake_pos[1] < 0):
                self.game_over = True

            for block in self.snake_body[1:]:
                if self.snake_pos == block:
                    self.game_over = True

            self.snake_body.insert(0, list(self.snake_pos))

            if self.snake_pos == self.food_pos:
                self.score += 1
                self.food_pos = self.generate_food()
                
               
                if self.score % 3 == 0:
                    self.level += 1
                    self.speed += 2
            else:
                self.snake_body.pop()

            self.screen.fill(BLACK)
            for pos in self.snake_body:
                pygame.draw.rect(self.screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            
            pygame.draw.rect(self.screen, RED, pygame.Rect(self.food_pos[0], self.food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
            
            self.display_score()
            pygame.display.flip()
            self.clock.tick(self.speed)

        self.screen.fill(BLACK)
        msg = self.font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
        self.screen.blit(msg, [WIDTH/6, HEIGHT/2])
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return
                    if event.key == pygame.K_c:
                        self.reset_game()
                        self.run()
                        return

if __name__ == "__main__":
    game = SnakeGame()
    game.run()