import pygame
import datetime
import os
from tools import draw_shape, flood_fill

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 700))
    pygame.display.set_caption("TSIS 2: Paint with Text Tool")
    clock = pygame.time.Clock()
    
    canvas = pygame.Surface((900, 600))
    canvas.fill((0, 0, 0))
    
    COLORS = {'RED': (255, 0, 0), 'GREEN': (0, 255, 0), 'BLUE': (0, 0, 255), 'WHITE': (255, 255, 255)}
    TOOLS = {'pencil': 'P', 'rect': 'R', 'circle': 'C', 'fill': 'F', 'eraser': 'E', 'line': 'L', 'text': 'T'}
    
    current_color = COLORS['WHITE']
    tool, thickness = 'pencil', 2
    drawing, start_pos, last_pos = False, None, None
    
    text_active = False
    text_input = ""
    text_pos = (0, 0)
    
    main_font = pygame.font.SysFont("Verdana", 14, bold=True)
    canvas_font = pygame.font.SysFont("Arial", 24) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            
            if text_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        txt_surf = canvas_font.render(text_input, True, current_color)
                        canvas.blit(txt_surf, text_pos)
                        text_active = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode 
                continue 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: tool = 'pencil'
                if event.key == pygame.K_f: tool = 'fill'
                if event.key == pygame.K_r: tool = 'rect'
                if event.key == pygame.K_c: tool = 'circle'
                if event.key == pygame.K_t: tool = 'text' 
                if event.key == pygame.K_l: tool = 'line'
                if event.key == pygame.K_e: tool = 'eraser'
                if event.key == pygame.K_1: thickness = 2
                if event.key == pygame.K_2: thickness = 5
                if event.key == pygame.K_3: thickness = 10

                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    if not os.path.exists(ASSETS_DIR): os.makedirs(ASSETS_DIR)
                    name = f"save_{datetime.datetime.now().strftime('%H%M%S')}.png"
                    pygame.image.save(canvas, os.path.join(ASSETS_DIR, name))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > 100:
                    y_adj = event.pos[1] - 100
                    if tool == 'text':
                        text_active = True
                        text_pos = (event.pos[0], y_adj)
                        text_input = ""
                    elif tool == 'fill': 
                        flood_fill(canvas, event.pos[0], y_adj, current_color)
                    else:
                        drawing = True
                        start_pos = (event.pos[0], y_adj)
                        last_pos = start_pos
                else:
                    for i, col in enumerate(COLORS.values()):
                        if 10 + i*45 <= event.pos[0] <= 45 + i*45 and 10 <= event.pos[1] <= 45:
                            current_color = col

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and tool not in ['pencil', 'eraser', 'text']:
                    draw_shape(canvas, tool, current_color, start_pos, (event.pos[0], event.pos[1]-100), thickness)
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                curr = (event.pos[0], event.pos[1]-100)
                if tool == 'pencil':
                    pygame.draw.line(canvas, current_color, last_pos, curr, thickness)
                    last_pos = curr
                elif tool == 'eraser':
                    pygame.draw.circle(canvas, (0, 0, 0), curr, thickness + 10)

        screen.fill((30, 30, 30))
        screen.blit(canvas, (0, 100))
        
        if text_active:
            preview_txt = canvas_font.render(text_input + "|", True, current_color)
            screen.blit(preview_txt, (text_pos[0], text_pos[1] + 100))

        if drawing and tool not in ['pencil', 'eraser', 'text']:
            curr = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]-100)
            temp_surf = pygame.Surface((900, 600), pygame.SRCALPHA)
            draw_shape(temp_surf, tool, current_color, start_pos, curr, thickness)
            screen.blit(temp_surf, (0, 100))

        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 900, 100))
        for i, (name, col) in enumerate(COLORS.items()):
            pygame.draw.rect(screen, col, (10 + i*45, 10, 35, 35))
            if current_color == col: pygame.draw.rect(screen, (220, 220, 220), (10 + i*45, 10, 35, 35), 3)

        for i, t in enumerate(TOOLS.keys()):
            x, y = 220 + i*60, 10
            bg = (100, 100, 100) if tool == t else (70, 70, 70)
            pygame.draw.rect(screen, bg, (x, y, 50, 55), border_radius=5)
            screen.blit(main_font.render(TOOLS[t], True, (255, 255, 255)), (x+18, y+10))
            
            s_font = pygame.font.SysFont("Arial", 10)
            screen.blit(s_font.render(t.upper(), True, (200, 200, 200)), (x+5, y+35))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__": main()