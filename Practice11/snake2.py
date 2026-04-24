import pygame
import random

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 102)
PURPLE = (155, 48, 255) 

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake - Counter & Wrap')
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.reset_game()

    def reset_game(self):
        self.snake_pos = [WIDTH / 2, HEIGHT / 2]
        self.snake_body = [[WIDTH / 2, HEIGHT / 2]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.total_eaten = 0 # Қанша тамақ жегені (счетчик)
        self.level = 1
        self.speed = 10
        self.food_timer = 0  
        self.food_lifetime = 5000  
        self.generate_food()
        self.game_over = False

    def generate_food(self):
        while True:
            x = random.randrange(0, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE
            y = random.randrange(0, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE
            if [x, y] not in self.snake_body:
                self.food_pos = [x, y]
                break
        self.food_weight = random.randint(1, 3)
        self.food_color = RED if self.food_weight == 1 else YELLOW if self.food_weight == 2 else PURPLE
        self.food_timer = pygame.time.get_ticks() 

    def display_score(self):
        # Экрандағы жазулар: Ұпай, Деңгей және Жеген саны (Weight)
        score_val = self.font_style.render(f"Score: {self.score}", True, WHITE)
        weight_val = self.font_style.render(f"Weight (Eaten): {self.total_eaten}", True, YELLOW)
        level_val = self.font_style.render(f"Level: {self.level}", True, WHITE)
        
        self.screen.blit(score_val, [10, 10])
        self.screen.blit(weight_val, [10, 40])
        self.screen.blit(level_val, [10, 70])

    def run(self):
        while not self.game_over:
            if pygame.time.get_ticks() - self.food_timer > self.food_lifetime:
                self.generate_food()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
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

            # Қабырғадан өту
            self.snake_pos[0] %= WIDTH
            self.snake_pos[1] %= HEIGHT

            for block in self.snake_body[1:]:
                if self.snake_pos == block:
                    self.game_over = True

            self.snake_body.insert(0, list(self.snake_pos))

            if self.snake_pos == self.food_pos:
                self.score += self.food_weight 
                self.total_eaten += 1 # Тамақ жеген сайын +1 қосады
                if self.score // 5 >= self.level:
                    self.level += 1
                    self.speed += 2
                self.generate_food()
            else:
                self.snake_body.pop()

            self.screen.fill(BLACK)
            for pos in self.snake_body:
                pygame.draw.rect(self.screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, self.food_color, pygame.Rect(self.food_pos[0], self.food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
            self.display_score()
            pygame.display.flip()
            self.clock.tick(self.speed)

        self.reset_screen()

    def reset_screen(self):
        self.screen.fill(BLACK)
        msg = self.font_style.render("Game Over! Q-Quit or C-Play Again", True, RED)
        self.screen.blit(msg, [WIDTH/4, HEIGHT/2])
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: pygame.quit(); return
                    if event.key == pygame.K_c: self.reset_game(); self.run(); return

if __name__ == "__main__":
    game = SnakeGame()
    game.run()