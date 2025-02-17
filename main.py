import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QFileDialog, QVBoxLayout, QWidget, QLineEdit, QSlider
from PySide6.QtCore import QTimer, Qt
import player
import pygame
from lyrics_handler import LyricsHandler

class LyricsPlayer(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("Lyrics Player")
    self.setGeometry(100, 100, 600, 400)

    self.player = player.MusicPlayer()
    self.lyrics_handler = LyricsHandler()

    self.load_button = QPushButton("音楽を読み込む")
    self.play_button = QPushButton("再生")
    self.stop_button = QPushButton("停止")
    self.file_label = QLabel("ファイルが選択されていません")
    self.current_lyric_label = QLabel("現在の歌詞: なし")
    self.lyrics_display = QTextEdit()
    self.lyrics_display.setReadOnly(True)
    self.new_lyric_input = QLineEdit()
    self.new_lyric_input.setPlaceholderText("歌詞を入力")
    self.timestamp_button = QPushButton("タイムスタンプを追加")
    self.slider = QSlider(Qt.Orientation.Horizontal)
    self.slider.setMinimum(0)
    self.slider.setMaximum(1000)

    self.timer = QTimer()
    self.timer.setInterval(100)

    layout = QVBoxLayout()
    layout.addWidget(self.load_button)
    layout.addWidget(self.file_label)
    layout.addWidget(self.play_button)
    layout.addWidget(self.stop_button)
    layout.addWidget(self.slider)
    layout.addWidget(self.new_lyric_input)
    layout.addWidget(self.timestamp_button)
    layout.addWidget(self.current_lyric_label)
    layout.addWidget(self.lyrics_display)

    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)

    self.load_button.clicked.connect(self.load_music)
    self.play_button.clicked.connect(self.play_music)
    self.stop_button.clicked.connect(self.stop_music)
    self.timestamp_button.clicked.connect(self.add_timestamp)
    self.slider.sliderMoved.connect(self.set_position)
    self.timer.timeout.connect(self.update_lyrics)

  def load_music(self):
    file_name, _ = QFileDialog.getOpenFileName(
        self, "Load Music File", "", "Audio Files (*.mp3 *.wav)")
    if file_name:
      self.player.load(file_name)
      self.file_label.setText(f"Loaded: {file_name.split('/')[-1]}")
      self.lyrics_handler.load_lyrics(file_name.replace('.mp3', '.lrc'))
      self.slider.setValue(0)

  def play_music(self):
    self.player.play()
    self.timer.start()

  def stop_music(self):
    self.player.stop()
    self.timer.stop()

  def add_timestamp(self):
    if self.player.is_loaded():
      current_time = self.player.get_pos()
      new_lyric = self.new_lyric_input.text().strip()
      if new_lyric:
        self.lyrics_handler.add_timestamp(current_time, new_lyric)
        self.new_lyric_input.clear()
        self.update_display()

  def update_display(self):
    display_text = "\n".join(
        [f"[{int(ts // 60):02}:{ts % 60:05.2f}] {lyric}" for ts, lyric in
         zip(self.lyrics_handler.timestamps, self.lyrics_handler.lyrics)]
    )
    self.lyrics_display.setText(display_text)

  def update_lyrics(self):
    current_time = self.player.get_pos()
    current_lyric = self.lyrics_handler.get_current_lyric(current_time)
    self.current_lyric_label.setText("Current Lyric: " + current_lyric)

    if self.player.current_song:
      song_length = pygame.mixer.Sound(
          self.player.current_song).get_length()
      if song_length > 0:
        slider_position = int((current_time / song_length) * 1000)
        self.slider.setValue(slider_position)

  def set_position(self, position):
    if self.player.is_loaded():
      song_length = pygame.mixer.Sound(
          self.player.current_song).get_length()
      new_time = (position / 1000.0) * song_length
      self.player.set_pos(new_time)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = LyricsPlayer()
  window.show()
  sys.exit(app.exec())
