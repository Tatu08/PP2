import pygame
import os
import time


class MusicPlayer:
    """
    Manages playlist, playback state, and pygame.mixer interactions.
    """

    def __init__(self, music_dir: str = "music"):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.music_dir = music_dir
        self.playlist: list[str] = []
        self.track_names: list[str] = []
        self.current_index: int = 0

        self.is_playing: bool = False
        self.play_start_time: float = 0.0
        self.pause_offset: float = 0.0

        self._load_playlist()

    def _load_playlist(self):
        if not os.path.isdir(self.music_dir):
            return

        supported = (".wav", ".mp3", ".ogg", ".flac", ".m4a")

        files = sorted(
            f for f in os.listdir(self.music_dir)
            if f.lower().endswith(supported)
        )

        self.playlist = [os.path.join(self.music_dir, f) for f in files]
        self.track_names = [os.path.splitext(f)[0] for f in files]

    def has_tracks(self) -> bool:
        return len(self.playlist) > 0

    def play(self):
        """Play or resume"""
        if not self.has_tracks():
            return

        track = self.playlist[self.current_index]

        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play(start=self.pause_offset)
        except Exception as e:
            print("Error loading track:", e)
            return

        self.play_start_time = time.time() - self.pause_offset
        self.is_playing = True

    def pause(self):
        """Pause and save position"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.pause_offset = self.get_position()
            self.is_playing = False

    def stop(self):
        """Full stop (reset)"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_start_time = 0.0
        self.pause_offset = 0.0

    def next_track(self):
        self.stop()
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        self.stop()
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()


    def get_position(self) -> float:
        if not self.is_playing:
            return self.pause_offset
        return time.time() - self.play_start_time

    def get_current_track_name(self) -> str:
        if not self.has_tracks():
            return "No tracks found"
        return self.track_names[self.current_index]

    def get_playlist_info(self) -> str:
        if not self.has_tracks():
            return "0 / 0"
        return f"{self.current_index + 1} / {len(self.playlist)}"

    def update(self):
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.stop()
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def quit(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()