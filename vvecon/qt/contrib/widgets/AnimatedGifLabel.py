from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QSize, Qt


class AnimatedGifLabel(QLabel):
    def __init__(self, gif_path, parent=None):
        super().__init__(parent)
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.movie.setSpeed(300)
        self.setStyleSheet("background: transparent; border: none;")
        self.setMinimumSize(QSize(48, 48))  # Increase minimum size
        self._defaultSize = QSize(48, 48)
        self.movie.frameChanged.connect(self._resizeFrame)
        self._lastSize = self._defaultSize

    def start(self):
        self.movie.start()

    def stop(self):
        self.movie.stop()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._lastSize = self.size() if self.size().width() > 0 else self._defaultSize
        self._resizeFrame()

    def _resizeFrame(self):
        if self.movie.currentPixmap().isNull():
            return
        pixmap = self.movie.currentPixmap().scaled(
            QSize(int(self._lastSize.width()*1.168), int(self._lastSize.height()*1.168)),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(pixmap)
