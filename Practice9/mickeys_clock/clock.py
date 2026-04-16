import pygame
import time

def blit_rotate(surface, image, pos, origin_pos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - origin_pos[0], pos[1] - origin_pos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surface.blit(rotated_image, rotated_image_rect)

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.center = (300, 300)
        self.hand = pygame.image.load("images/mickey_hand.png").convert_alpha()
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 36)

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), self.center, 260, 20)
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 250, 8)

        now = time.localtime()
        minutes = now.tm_min
        seconds = now.tm_sec

        min_angle = minutes * 6 + seconds * 0.1
        sec_angle = seconds * 6

        origin_pos = (self.hand.get_width() // 2, self.hand.get_height())  

        blit_rotate(self.screen, self.hand, self.center, origin_pos, -min_angle)   
        blit_rotate(self.screen, self.hand, self.center, origin_pos, -sec_angle)   

        time_text = self.font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 220, 100))
        self.screen.blit(time_text, (210, 520))

        label = self.small_font.render("Mickey's Clock", True, (200, 200, 200))
        self.screen.blit(label, (220, 30))