import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.tracks = ["music/track1.wav", "music/track2.wav"]
        self.current = 0
        self.playing = False
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)

    def play(self):
        if not self.playing:
            pygame.mixer.music.load(self.tracks[self.current])
            pygame.mixer.music.play()
            self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        self.stop()
        self.current = (self.current + 1) % len(self.tracks)
        self.play()

    def previous_track(self):
        self.stop()
        self.current = (self.current - 1) % len(self.tracks)
        self.play()

    def draw(self, screen):
        status = "▶ PLAYING" if self.playing else "⏹ STOPPED"
        track_name = self.tracks[self.current].split("/")[-1]

        title = self.font.render("Music Player", True, (100, 255, 255))
        track = self.font.render(f"Track: {self.current + 1}/{len(self.tracks)} - {track_name}", True, (255, 255, 255))
        status_txt = self.font.render(status, True, (0, 255, 100) if self.playing else (255, 80, 80))

        pos = pygame.mixer.music.get_pos() / 1000 if self.playing else 0
        progress = self.small_font.render(f"Position: {pos:.1f} sec", True, (220, 220, 220))

        screen.blit(title, (180, 80))
        screen.blit(track, (80, 180))
        screen.blit(status_txt, (80, 240))
        screen.blit(progress, (80, 300))

        # Подсказка по клавишам
        help_txt = self.small_font.render("P=Play  S=Stop  N=Next  B=Prev  Q=Quit", True, (180, 180, 180))
        screen.blit(help_txt, (90, 400))