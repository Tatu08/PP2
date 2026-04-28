import pygame, sys, random
from racer import Enemy, Obstacle, PowerUp
from ui import main_menu, input_menu, draw_text
from persistence import load_settings, save_score
from ui import main_menu, input_menu, draw_text, settings_screen, show_leaderboard
pygame.init()
SCREEN = pygame.display.set_mode((400, 600))
CLOCK = pygame.time.Clock()

def game_loop():
    set_data = load_settings()
    username = input_menu(SCREEN) 
    
    base_speed = {"Easy": 3, "Medium": 5, "Hard": 7}.get(set_data.get('difficulty', 'Medium'), 5)
    speed = base_speed
    score, distance = 0, 0
    active_pw, pw_timer = None, 0
    shielded = False
    
    player = pygame.Rect(180, 500, 40, 70)
    p_color = (0, 0, 255) if set_data.get('color') == "BLUE" else (200, 0, 200)
    
    enemies = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, 1500)
    SPAWN_PW = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_PW, 7000)

    while True:
        SCREEN.fill((50, 50, 50))
        dt = CLOCK.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == SPAWN_ENEMY:
                new_e = Enemy(speed)
                if not new_e.rect.colliderect(player.inflate(0, 200)):
                    enemies.add(new_e)
                if random.random() > 0.6:
                    obstacles.add(Obstacle(speed))
            
            if event.type == SPAWN_PW:
                powerups.add(PowerUp(random.choice(['nitro', 'shield', 'shield', 'repair'])))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0: player.x -= 6
        if keys[pygame.K_RIGHT] and player.right < 400: player.x += 6

        enemies.update(); obstacles.update(); powerups.update()
        
        distance += speed / 60
        speed = base_speed + int(distance // 20)

        if pw_timer > 0:
            pw_timer -= dt
            if pw_timer <= 0:
                if active_pw == 'nitro': speed -= 4
                active_pw = None
        
        for e in enemies:
            if player.colliderect(e.rect):
                if shielded: shielded = False; e.kill() 
                else: save_score(username, int(distance + score)); return
        
        for o in obstacles:
            if player.colliderect(o.rect):
                if o.type == 'oil': speed = 2 
                elif not shielded: save_score(username, int(distance + score)); return

        for p in powerups:
            if player.colliderect(p.rect):
                active_pw = p.p_type
                if active_pw == 'nitro': speed += 4; pw_timer = 4000
                elif active_pw == 'shield': shielded = True
                elif active_pw == 'repair': score += 20
                p.kill()

        pygame.draw.rect(SCREEN, p_color, player)
        if shielded: pygame.draw.rect(SCREEN, (0, 255, 255), player, 3)
        enemies.draw(SCREEN); obstacles.draw(SCREEN); powerups.draw(SCREEN)
        
        draw_text(SCREEN, f"Score: {int(distance + score)}", 18, 70, 30)
        if active_pw: draw_text(SCREEN, f"PW: {active_pw} ({pw_timer//1000}s)", 15, 70, 60, (255, 255, 0))
        
        pygame.display.update()

def start():
    while True:
        choice = main_menu(SCREEN)
        
        if choice == "play":
            game_loop() 
        elif choice == "lb":
            show_leaderboard(SCREEN) 
        elif choice == "set":
            settings_screen(SCREEN) 
        elif choice == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    start()