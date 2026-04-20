"""
Music Player with Keyboard Controller
======================================
Controls:
  P  — Play / Resume
  S  — Stop
  N  — Next track
  B  — Back (previous track)
  Q  — Quit
"""

import pygame
import sys
import math
import time
from player import MusicPlayer

WIDTH, HEIGHT = 620, 400
FPS = 60

BG        = (10, 10, 18)
PANEL     = (20, 20, 35)
ACCENT    = (0, 210, 150) 
ACCENT2   = (0, 140, 100)
DIM       = (60, 60, 90)
WHITE     = (230, 230, 240)
GREY      = (120, 120, 150)
RED       = (220, 60, 80)
DARK_GREY = (35, 35, 55)

def fmt_time(secs: float) -> str:
    secs = max(0, int(secs))
    m, s = divmod(secs, 60)
    return f"{m:02d}:{s:02d}"


def draw_rounded_rect(surface, color, rect, radius=12):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_progress_bar(surface, x, y, w, h, progress: float, radius=6):
    """Draw a rounded progress bar (0.0–1.0)."""
    draw_rounded_rect(surface, DARK_GREY, (x, y, w, h), radius)
    filled = max(0, min(1, progress))
    if filled > 0:
        draw_rounded_rect(surface, ACCENT, (x, y, int(w * filled), h), radius)
    kx = x + int(w * filled)
    pygame.draw.circle(surface, WHITE, (kx, y + h // 2), h)


def draw_waveform(surface, x, y, w, h, t: float, playing: bool):
    """Animated waveform decoration."""
    bars = 32
    bar_w = w // bars - 1
    for i in range(bars):
        phase = i / bars * math.pi * 2
        if playing:
            amp = 0.4 + 0.6 * abs(math.sin(t * 3 + phase))
        else:
            amp = 0.15
        bar_h = int(h * amp)
        bx = x + i * (bar_w + 1)
        by = y + (h - bar_h) // 2
        alpha_ratio = 0.5 + 0.5 * amp
        col = tuple(int(c * alpha_ratio) for c in ACCENT)
        pygame.draw.rect(surface, col, (bx, by, bar_w, bar_h), border_radius=2)


def draw_key_hint(surface, font_sm, shortcuts, start_x, y):
    """Draw keyboard shortcut badges."""
    x = start_x
    for key, label in shortcuts:
        tw, th = font_sm.size(key)
        badge_rect = (x, y, tw + 14, th + 8)
        draw_rounded_rect(surface, DARK_GREY, badge_rect, radius=6)
        pygame.draw.rect(surface, DIM, badge_rect, width=1, border_radius=6)
        surface.blit(font_sm.render(key, True, ACCENT), (x + 7, y + 4))
        x += tw + 16

        lsurf = font_sm.render(label, True, GREY)
        surface.blit(lsurf, (x, y + 4))
        x += lsurf.get_width() + 22


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎵 Music Player")
    clock = pygame.time.Clock()

    font_title  = pygame.font.SysFont("couriernew", 13, bold=True)
    font_track  = pygame.font.SysFont("couriernew", 22, bold=True)
    font_info   = pygame.font.SysFont("couriernew", 13)
    font_sm     = pygame.font.SysFont("couriernew", 12)
    font_status = pygame.font.SysFont("couriernew", 14, bold=True)

    player = MusicPlayer(music_dir="music")
    start_wall = time.time()
    flash_msg: str = ""
    flash_until: float = 0.0

    shortcuts = [
        ("P", "Play"),
        ("S", "Stop"),
        ("N", "Next"),
        ("B", "Back"),
        ("Q", "Quit"),
    ]

    running = True
    while running:
        now = time.time()
        t = now - start_wall

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                key = event.key

                if key == pygame.K_q:
                    running = False

                elif key == pygame.K_p:
                    if player.has_tracks():
                        player.play()
                        flash_msg, flash_until = "▶  PLAYING", now + 1.5

                elif key == pygame.K_s:
                    player.stop()
                    flash_msg, flash_until = "■  STOPPED", now + 1.5

                elif key == pygame.K_n:
                    if player.has_tracks():
                        player.next_track()
                        flash_msg, flash_until = "⏭  NEXT TRACK", now + 1.5

                elif key == pygame.K_b:
                    if player.has_tracks():
                        player.prev_track()
                        flash_msg, flash_until = "⏮  PREV TRACK", now + 1.5

        player.update()

        screen.fill(BG)

       
        draw_rounded_rect(screen, PANEL, (0, 0, WIDTH, 56), radius=0)
        title_surf = font_title.render("◈  MUSIC PLAYER  ◈", True, ACCENT)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 10))
        ver_surf = font_sm.render("keyboard controller", True, DIM)
        screen.blit(ver_surf, (WIDTH // 2 - ver_surf.get_width() // 2, 30))

        
        draw_waveform(screen, 20, 68, WIDTH - 40, 48, t, player.is_playing)

       
        panel_y = 130
        draw_rounded_rect(screen, PANEL, (20, panel_y, WIDTH - 40, 110), radius=14)

        
        pos_surf = font_info.render(f"Track {player.get_playlist_info()}", True, GREY)
        screen.blit(pos_surf, (38, panel_y + 12))

       
        if player.is_playing:
            status_text, status_col = "● PLAYING", ACCENT
        else:
            status_text, status_col = "■ STOPPED", RED
        st_surf = font_status.render(status_text, True, status_col)
        screen.blit(st_surf, (WIDTH - 40 - st_surf.get_width(), panel_y + 12))

       
        name = player.get_current_track_name()
        if len(name) > 30:
            name = name[:28] + "…"
        name_surf = font_track.render(name, True, WHITE)
        screen.blit(name_surf, (38, panel_y + 38))

        
        pos_secs = player.get_position()
        time_surf = font_info.render(fmt_time(pos_secs), True, GREY)
        screen.blit(time_surf, (38, panel_y + 80))

      
        DEMO_DURATION = 180.0
        progress = (pos_secs % DEMO_DURATION) / DEMO_DURATION if player.is_playing else 0.0
        draw_progress_bar(screen, 38, panel_y + 97, WIDTH - 76, 8, progress)

    
        if now < flash_until:
            alpha_fade = min(1.0, (flash_until - now) * 2)
            col = tuple(int(c * alpha_fade) for c in ACCENT)
            flash_surf = font_status.render(flash_msg, True, col)
            fx = WIDTH // 2 - flash_surf.get_width() // 2
            screen.blit(flash_surf, (fx, 258))

       
        if not player.has_tracks():
            warn = font_info.render(
                "⚠  No audio files found in ./music/  — add .wav or .mp3 files",
                True, RED
            )
            screen.blit(warn, (WIDTH // 2 - warn.get_width() // 2, 260))

        
        pygame.draw.line(screen, DIM, (20, 288), (WIDTH - 20, 288), 1)

        
        draw_key_hint(screen, font_sm, shortcuts, 22, 298)

        
        footer = font_sm.render(
            f"{'Playing' if player.is_playing else 'Idle'}  •  {len(player.playlist)} track(s) loaded",
            True, DIM
        )
        screen.blit(footer, (20, HEIGHT - 22))

        pygame.display.flip()
        clock.tick(FPS)

    player.quit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()