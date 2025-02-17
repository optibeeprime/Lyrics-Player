class LyricsHandler:
  def __init__(self):
    self.timestamps = []
    self.lyrics = []

  def load_lyrics(self, file_path):
    try:
      with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
          if line.strip():
            # LRCファイルは [mm:ss.xx] Lyric 形式
            time_str, lyric = line.strip().split(' ', 1)
            minutes, seconds = time_str[1:-1].split(':')
            time_in_seconds = int(minutes) * 60 + float(seconds)
            self.timestamps.append(time_in_seconds)
            self.lyrics.append(lyric)
    except FileNotFoundError:
      print("Lyrics file not found, starting fresh")
      self.timestamps = []
      self.lyrics = []

  def add_timestamp(self, time, lyric):
    self.timestamps.append(time)
    self.lyrics.append(lyric)

  def get_current_lyric(self, current_time):
    if not self.timestamps:
      return ""

    for i in range(len(self.timestamps) - 1, -1, -1):
      if current_time >= self.timestamps[i]:
        return self.lyrics[i]

    return ""

  def save_lyrics(self, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
      for time, lyric in zip(self.timestamps, self.lyrics):
        minutes = int(time // 60)
        seconds = time % 60
        file.write(f"[{minutes:02}:{seconds:05.2f}] {lyric}\n")
