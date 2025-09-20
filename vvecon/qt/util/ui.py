import platform
from typing import Optional

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QSizePolicy

__all__ = ['ui']


class UI:
    _logicalDpi: int = 96

    @staticmethod
    def pixmap(
        file_name: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        aspect_ratio_mode: Qt.AspectRatioMode = Qt.AspectRatioMode.IgnoreAspectRatio,
        transform_mode: Qt.TransformationMode = Qt.TransformationMode.FastTransformation
    ) -> QPixmap:
        pixmap = QPixmap()
        pixmap.load(file_name)
        if width is None and height is not None:
            pixmap.scaled(width, height, aspect_ratio_mode, transform_mode)
        return pixmap

    @staticmethod
    def icon(
        file_name: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        aspect_ratio_mode: Qt.AspectRatioMode = Qt.AspectRatioMode.IgnoreAspectRatio,
        transform_mode: Qt.TransformationMode = Qt.TransformationMode.FastTransformation
    ) -> QIcon:
        return QIcon(
            UI.pixmap(file_name, width, height, aspect_ratio_mode,
                      transform_mode))

    def setLogicalDpi(self, dpi: int):
        self._logicalDpi = dpi

    @property
    def dpiFactor(self) -> float:
        return self._logicalDpi / (72 if platform.system() == 'Darwin' else 96)

    def dp(self, unit: int) -> int:
        return int(unit * self.dpiFactor)

    def sp(self, unit: int) -> int:
        return int(unit * self.dpiFactor)

    @staticmethod
    def colorHex(color: tuple) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*color)

    @staticmethod
    def sizePolicy(horizontal: QSizePolicy.Policy, vertical: QSizePolicy.Policy) -> QSizePolicy:
        return QSizePolicy(horizontal, vertical)

    def size(self, width: int, height: int) -> QSize:
        return QSize(self.dp(width), self.dp(height))


ui = UI()
