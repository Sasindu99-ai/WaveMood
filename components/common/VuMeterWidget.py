from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QLinearGradient
from PyQt6.QtWidgets import QWidget
from vvecon.qt.util import ui

__all__ = ['VuMeterWidget']


class VuMeterWidget(QWidget):
    """
    VuMeterWidget

    Description:
        Simple horizontal jumping bars VU meter (main-thread only).

    Attributes:
        num_bars: Number of bars to display.
        levels: Current levels for each bar.
        decay: Decay rate for each bar.

    Methods:
        update_levels: Update levels for each bar.
    """
    def __init__(self, parent=None, num_bars=2):
        super().__init__(parent)
        self.num_bars = max(1, int(num_bars))
        self.levels = [0.0] * self.num_bars
        self.decay = 0.06
        # visual tuning
        self._corner_radius = 8
        self._padding = 10
        self.setMinimumHeight(ui.dp(56))
        self.setStyleSheet("background: transparent;")
        self.setContentsMargins(0, 0, 0, 0)

    def update_levels(self, levels):
        # Called on main thread via QTimer
        if len(levels) != self.num_bars:
            levels = levels[:self.num_bars] + [0.0] * max(0, self.num_bars - len(levels))
        for i in range(self.num_bars):
            new = float(levels[i])
            self.levels[i] = max(new, max(0.0, self.levels[i] - self.decay))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            w = self.width()
            h = self.height()

            # draw rounded card-like background with subtle border
            bg_color = QColor('#2A2F36')
            border_color = QColor('#353A42')
            painter.setPen(QPen(border_color))
            painter.setBrush(QBrush(bg_color))
            rect = self.rect().adjusted(0, 0, 0, 0)
            painter.drawRoundedRect(rect, self._corner_radius, self._corner_radius)

            # inner drawing area
            inner_x = self._padding
            inner_w = max(8, w - 2 * self._padding)
            inner_y = self._padding
            inner_h = max(8, h - 2 * self._padding)

            # spacing between stacked horizontal bars
            spacing = max(6, int(inner_h * 0.12))
            total_spacing = spacing * (self.num_bars + 1)
            bar_h = max(6, int((inner_h - total_spacing) / max(1, self.num_bars)))

            for i, lvl in enumerate(self.levels):
                level = float(min(1.0, max(0.0, lvl)))
                y = inner_y + spacing + i * (bar_h + spacing)
                length = int(round(inner_w * level))

                # color by thresholds and soft gradient
                if level < 0.6:
                    start_col = QColor(98, 200, 120)
                    end_col = QColor(60, 180, 100)
                elif level < 0.85:
                    start_col = QColor(255, 214, 102)
                    end_col = QColor(255, 190, 40)
                else:
                    start_col = QColor(250, 120, 120)
                    end_col = QColor(220, 60, 60)

                # draw filled portion with subtle gradient
                if length > 0:
                    grad_rect = QRectF(inner_x, y, length, bar_h)
                    grad = QLinearGradient(grad_rect.topLeft(), grad_rect.topRight())
                    grad.setColorAt(0.0, start_col)
                    grad.setColorAt(1.0, end_col)
                    painter.setBrush(QBrush(grad))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRoundedRect(grad_rect, bar_h / 2, bar_h / 2)

                # draw track for remaining area
                track_rect = QRectF(inner_x + length, y, max(0, inner_w - length), bar_h)
                painter.setBrush(QBrush(QColor(80, 86, 92, 140)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(track_rect, bar_h / 2, bar_h / 2)
        finally:
            painter.end()