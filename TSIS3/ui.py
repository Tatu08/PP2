import pygame, sys
from persistence import load_settings, save_settings, load_leaderboard

def draw_text(screen, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont("Verdana", size)
    img = font.render(text, True, color)
    screen.blit(img, img.get_rect(center=(x, y)))

class Button:
    def __init__(self, text, x, y, w, h, action_key):
        self.rect = pygame.Rect(x - w // 2, y, w, h)
        self.text = text
        self.action_key = action_key

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 70, 70), self.rect, border_radius=5)
        draw_text(screen, self.text, 20, self.rect.centerx, self.rect.centery)

def input_menu(screen):
    name = ""
    while True:
        screen.fill((30, 30, 30))
        draw_text(screen, "ENTER YOUR NAME:", 25, 200, 200)
        draw_text(screen, name + "_", 30, 200, 260, (255, 215, 0))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name: return name
                elif e.key == pygame.K_BACKSPACE: name = name[:-1]
                else: 
                    if len(name) < 10: name += e.unicode

def main_menu(screen):
    btns = [
        Button("PLAY", 200, 150, 220, 50, "play"),
        Button("LEADERBOARD", 200, 220, 220, 50, "lb"),
        Button("SETTINGS", 200, 290, 220, 50, "set"),
        Button("QUIT", 200, 360, 220, 50, "quit")
    ]
    while True:
        screen.fill((20, 20, 20))
        draw_text(screen, "ADVANCED RACER", 35, 200, 80)
        for b in btns: b.draw(screen)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    for b in btns:
                        if b.rect.collidepoint(e.pos): return b.action_key

def settings_screen(screen):
    s = load_settings()
    back_btn = Button("SAVE & BACK", 200, 450, 200, 50, "back")
    while True:
        screen.fill((40, 40, 40))
        draw_text(screen, "SETTINGS", 35, 200, 80)
        draw_text(screen, f"Sound: {'ON' if s.get('sound') else 'OFF'}", 22, 200, 180)
        draw_text(screen, f"Car Color: {s.get('color')}", 22, 200, 250)
        draw_text(screen, f"Difficulty: {s.get('difficulty')}", 22, 200, 320)
        back_btn.draw(screen)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.rect.collidepoint(e.pos):
                    save_settings(s)
                    return
                if 160 < e.pos[1] < 200: s['sound'] = not s.get('sound', True)
                if 230 < e.pos[1] < 270: s['color'] = "PINK" if s.get('color') == "BLUE" else "BLUE"
                if 300 < e.pos[1] < 340:
                    diffs = ["Easy", "Medium", "Hard"]
                    idx = diffs.index(s.get('difficulty', 'Medium'))
                    s['difficulty'] = diffs[(idx + 1) % 3]

def show_leaderboard(screen):
    scores = load_leaderboard()
    back_btn = Button("BACK", 200, 500, 150, 40, "back")
    while True:
        screen.fill((25, 25, 25))
        draw_text(screen, "TOP 10 SCORES", 30, 200, 60, (255, 215, 0))
        for i, entry in enumerate(scores):
            txt = f"{i+1}. {entry['name']} - {entry['score']}"
            draw_text(screen, txt, 18, 200, 130 + (i * 30))
        back_btn.draw(screen)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.rect.collidepoint(e.pos): return