import pygame
import sys
from clock import MickeyClock

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

mickey_clock = MickeyClock(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))          
    mickey_clock.draw()
    pygame.display.flip()
    clock.tick(60)                     
pygame.quit()
sys.exit()