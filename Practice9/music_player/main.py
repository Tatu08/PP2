import pygame
import sys
from player import MusicPlayer

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Music Player")
clock = pygame.time.Clock()

player = MusicPlayer()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:      
                player.play()
            elif event.key == pygame.K_s:    
                player.stop()
            elif event.key == pygame.K_n:    
                player.next_track()
            elif event.key == pygame.K_b:    
                player.previous_track()
            elif event.key == pygame.K_q:    
                running = False

    screen.fill((20, 20, 40))
    player.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()