import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    COLORS = {
        'RED': (255, 0, 0),
        'GREEN': (0, 255, 0),
        'BLUE': (0, 0, 255),
        'WHITE': (255, 255, 255),
        'BLACK': (0, 0, 0)
    }
    
    current_color = COLORS['BLUE']
    tool = 'line'  
    radius = 5
    
    canvas = pygame.Surface((800, 600))
    canvas.fill(COLORS['BLACK'])
    
    drawing = False
    start_pos = None

    while True:
        screen.fill(COLORS['BLACK'])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l: tool = 'line'
                if event.key == pygame.K_r: tool = 'rect'
                if event.key == pygame.K_s: tool = 'square'      
                if event.key == pygame.K_t: tool = 'right_tri'  
                if event.key == pygame.K_i: tool = 'eq_tri'     
                if event.key == pygame.K_h: tool = 'rhombus'    
                if event.key == pygame.K_c: tool = 'circle'
                if event.key == pygame.K_e: tool = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < 50:
                    if 10 <= event.pos[0] <= 40: current_color = COLORS['RED']
                    elif 50 <= event.pos[0] <= 80: current_color = COLORS['GREEN']
                    elif 90 <= event.pos[0] <= 120: current_color = COLORS['BLUE']
                    elif 130 <= event.pos[0] <= 160: current_color = COLORS['WHITE']
                else:
                    drawing = True
                    start_pos = event.pos
                
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    draw_shape(canvas, tool, current_color, start_pos, event.pos)
                start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing and event.pos[1] > 50: 
                    if tool == 'line':
                        pygame.draw.circle(canvas, current_color, event.pos, radius)
                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, COLORS['BLACK'], event.pos, radius + 10)

        screen.blit(canvas, (0, 0))
        
        if drawing and start_pos:
            curr_pos = pygame.mouse.get_pos()
            draw_shape(screen, tool, current_color, start_pos, curr_pos)

        # Интерфейс (Панель)
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 800, 50)) 
        pygame.draw.rect(screen, COLORS['RED'], (10, 10, 30, 30))
        pygame.draw.rect(screen, COLORS['GREEN'], (50, 10, 30, 30))
        pygame.draw.rect(screen, COLORS['BLUE'], (90, 10, 30, 30))
        pygame.draw.rect(screen, COLORS['WHITE'], (130, 10, 30, 30))
        
        font = pygame.font.SysFont("Arial", 16)
        txt = f"Tool: {tool} (L:line, R:rect, S:square, T:right_tri, I:eq_tri, H:rhombus, C:circle, E:eraser)"
        img = font.render(txt, True, COLORS['WHITE'])
        screen.blit(img, (180, 15))

        pygame.display.flip()
        clock.tick(60)

def draw_shape(surface, tool, color, start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    
    if tool == 'rect':
        pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), width, height), 2)
    
    elif tool == 'square':
        side = min(width, height)
        sx = x1 if x2 > x1 else x1 - side
        sy = y1 if y2 > y1 else y1 - side
        pygame.draw.rect(surface, color, (sx, sy, side, side), 2)
        
    elif tool == 'right_tri':
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, 2)
        
    elif tool == 'eq_tri':
        side = width
        h = side * math.sqrt(3) / 2
        direction = 1 if y2 > y1 else -1
        points = [(x1, y1), (x1 + side, y1), (x1 + side/2, y1 + direction * h)]
        pygame.draw.polygon(surface, color, points, 2)
        
    elif tool == 'rhombus':
        points = [
            (x1 + (x2 - x1) / 2, y1), 
            (x2, y1 + (y2 - y1) / 2), 
            (x1 + (x2 - x1) / 2, y2), 
            (x1, y1 + (y2 - y1) / 2)  
        ]
        pygame.draw.polygon(surface, color, points, 2)
        
    elif tool == 'circle':
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, color, start_pos, radius, 2)

if __name__ == "__main__":
    main()