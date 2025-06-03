import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_tracks = {}
        self.sfx = {}
        self.current_music = None
    def load_music(self, zone, path):
        self.music_tracks[zone] = path
    def play_music(self, zone, fade_ms=1000):
        if self.current_music != zone:
            if self.current_music:
                pygame.mixer.music.fadeout(fade_ms)
            pygame.mixer.music.load(self.music_tracks[zone])
            pygame.mixer.music.play(-1, fade_ms=fade_ms)
            self.current_music = zone
    def load_sfx(self, name, path):
        self.sfx[name] = pygame.mixer.Sound(path)
    def play_sfx(self, name):
        if name in self.sfx:
            self.sfx[name].play()
    def stop_music(self):
        pygame.mixer.music.stop() 