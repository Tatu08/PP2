import pygame
import random

WIDTH, HEIGHT = 600, 400
BLOCK = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

def game_loop():
    while True: 
        x, y = WIDTH // 2, HEIGHT // 2
        snake = [[x, y]]
        dx, dy = BLOCK, 0
        
        food_x = random.randrange(0, WIDTH, BLOCK)
        food_y = random.randrange(0, HEIGHT, BLOCK)
        
        score = 0
        level = 1
        speed = 10
        game_over = False

        while not game_over:
            screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -BLOCK
                    if event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, BLOCK
                    if event.key == pygame.K_LEFT and dx == 0: dx, dy = -BLOCK, 0
                    if event.key == pygame.K_RIGHT and dx == 0: dx, dy = BLOCK, 0

            x += dx
            y += dy

            if x >= WIDTH: x = 0
            elif x < 0: x = WIDTH - BLOCK
            if y >= HEIGHT: y = 0
            elif y < 0: y = HEIGHT - BLOCK

            new_head = [x, y]
            
            if new_head in snake:
                game_over = True
                
            snake.insert(0, new_head)

            if x == food_x and y == food_y:
                score += 1
                food_x = random.randrange(0, WIDTH, BLOCK)
                food_y = random.randrange(0, HEIGHT, BLOCK)
                if score % 3 == 0:
                    level += 1
                    speed += 2
            else:
                snake.pop()

            for segment in snake:
                pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], BLOCK-2, BLOCK-2))
            pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, BLOCK, BLOCK))
            
            txt = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
            screen.blit(txt, (10, 10))

            pygame.display.flip()
            clock.tick(speed)

        while game_over:
            screen.fill((50, 0, 0)) 
            msg = font.render("Game Over! Press C-Play Again or Q-Quit", True, (255, 255, 255))
            screen.blit(msg, (WIDTH // 6, HEIGHT // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit(); return
                    if event.key == pygame.K_c: 
                        game_over = False 
game_loop()