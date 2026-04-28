import pygame
import math

def draw_shape(surface, tool, color, start_pos, end_pos, thickness):
    x1, y1 = start_pos
    x2, y2 = end_pos
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    
    if tool == 'rect':
        pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), width, height), thickness)
    elif tool == 'line':
        pygame.draw.line(surface, color, start_pos, end_pos, thickness)
    elif tool == 'square':
        side = min(width, height)
        sx = x1 if x2 > x1 else x1 - side
        sy = y1 if y2 > y1 else y1 - side
        pygame.draw.rect(surface, color, (sx, sy, side, side), thickness)
    elif tool == 'circle':
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, color, start_pos, radius, thickness)
    elif tool == 'right_tri':
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, thickness)
    elif tool == 'eq_tri':
        side = width
        h = side * math.sqrt(3) / 2
        direction = 1 if y2 > y1 else -1
        points = [(x1, y1), (x1 + side, y1), (x1 + side/2, y1 + direction * h)]
        pygame.draw.polygon(surface, color, points, thickness)
    elif tool == 'rhombus':
        points = [(x1 + (x2 - x1) / 2, y1), (x2, y1 + (y2 - y1) / 2), 
                  (x1 + (x2 - x1) / 2, y2), (x1, y1 + (y2 - y1) / 2)]
        pygame.draw.polygon(surface, color, points, thickness)

def flood_fill(surface, x, y, new_color):
    try:
        target_color = surface.get_at((x, y))
    except IndexError: return
    if target_color == new_color: return
    
    stack = [(x, y)]
    while stack:
        curr_x, curr_y = stack.pop()
        if 0 <= curr_x < surface.get_width() and 50 <= curr_y < surface.get_height():
            if surface.get_at((curr_x, curr_y)) == target_color:
                surface.set_at((curr_x, curr_y), new_color)
                stack.append((curr_x + 1, curr_y))
                stack.append((curr_x - 1, curr_y))
                stack.append((curr_x, curr_y + 1))
                stack.append((curr_x, curr_y - 1))