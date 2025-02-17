import pygame

class MusicPlayer:
  def __init__(self):
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    self.current_song = None
    self.is_playing = False

  def load(self, filename):
    self.current_song = filename
    pygame.mixer.music.load(filename)
    self.is_playing = False

  def play(self):
    if self.current_song:
      pygame.mixer.music.play()
      self.is_playing = True

  def stop(self):
    pygame.mixer.music.stop()
    self.is_playing = False

  def get_pos(self):
    # 現在の再生時間をミリ秒単位で返す
    return pygame.mixer.music.get_pos() / 1000.0

  def set_pos(self, time):
    if self.current_song:
      pygame.mixer.music.play(start=time)  # 直接指定した位置から再生
      self.is_playing = True

  def is_loaded(self):
    return self.current_song is not None
