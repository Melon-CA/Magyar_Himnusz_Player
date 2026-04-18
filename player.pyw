import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QSlider, QLabel
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class HimnuszPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Magyar Himnusz Player")

        # === FIX MÉRET + GOMBOK ===
        self.setFixedSize(420, 150)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )

        # === PLAYER ===
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.player.setSource(QUrl("http://magyarhimnyusz.infora.hu/himnusz/himnusz.mp3"))

        # === GOMBOK ===
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")

        self.play_button.clicked.connect(self.play_music)
        self.stop_button.clicked.connect(self.stop_music)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)

        # === HANGERŐ ===
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)

        self.volume_label = QLabel("80%")

        self.audio_output.setVolume(0.8)
        self.volume_slider.valueChanged.connect(self.change_volume)

        volume_layout = QHBoxLayout()
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_label)

        # === STÁTUSZ ===
        self.status_label = QLabel("Státusz: Leállítva")

        # === IDŐ ===
        self.time_label = QLabel("Idő: 00:00 / 00:00")

        # === FŐ LAYOUT ===
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        layout.addLayout(button_layout)
        layout.addLayout(volume_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.time_label)

        self.setLayout(layout)

        # === SIGNALOK ===
        self.player.positionChanged.connect(self.update_time)
        self.player.durationChanged.connect(self.update_time)

    def play_music(self):
        self.player.play()
        self.status_label.setText("Státusz: Lejátszás...")

    def stop_music(self):
        self.player.stop()
        self.status_label.setText("Státusz: Leállítva")

    def change_volume(self, value):
        self.audio_output.setVolume(value / 100)
        self.volume_label.setText(f"{value}%")

    def format_time(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_time(self):
        position = self.player.position()
        duration = self.player.duration()

        pos_text = self.format_time(position)
        dur_text = self.format_time(duration)

        self.time_label.setText(f"Idő: {pos_text} / {dur_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HimnuszPlayer()
    window.show()
    sys.exit(app.exec())
