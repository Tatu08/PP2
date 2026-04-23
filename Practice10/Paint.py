import pygame

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
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l: tool = 'line'
                if event.key == pygame.K_r: tool = 'rect'
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
                    if tool == 'rect':
                        drawRect(canvas, current_color, start_pos, event.pos)
                    elif tool == 'circle':
                        drawCircle(canvas, current_color, start_pos, event.pos)
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
            if tool == 'rect':
                drawRect(screen, current_color, start_pos, curr_pos)
            elif tool == 'circle':
                drawCircle(screen, current_color, start_pos, curr_pos)

        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 800, 50)) 
        pygame.draw.rect(screen, COLORS['RED'], (10, 10, 30, 30))
        pygame.draw.rect(screen, COLORS['GREEN'], (50, 10, 30, 30))
        pygame.draw.rect(screen, COLORS['BLUE'], (90, 10, 30, 30))
        pygame.draw.rect(screen, COLORS['WHITE'], (130, 10, 30, 30))
        
        font = pygame.font.SysFont("Arial", 18)
        img = font.render(f"Tool: {tool} | Color: {current_color}", True, COLORS['WHITE'])
        screen.blit(img, (200, 15))

        pygame.display.flip()
        clock.tick(60)

def drawRect(surface, color, start_pos, end_pos):
    x = min(start_pos[0], end_pos[0])
    y = min(start_pos[1], end_pos[1])
    width = abs(start_pos[0] - end_pos[0])
    height = abs(start_pos[1] - end_pos[1])
    if width > 0 and height > 0:
        pygame.draw.rect(surface, color, (x, y, width, height), 2)

def drawCircle(surface, color, start_pos, end_pos):
    radius = int(((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5)
    if radius > 0:
        pygame.draw.circle(surface, color, start_pos, radius, 2)

main()