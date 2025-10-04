from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from enums import TopBarMode
from vvecon.qt.contrib.widgets import Margin, Button, Padding
from vvecon.qt.contrib.styles.Button import transparentButton
from vvecon.qt.logger import logger
from vvecon.qt.res import Icons
from vvecon.qt.util import ui

__all__ = ['TopBar']


class TopBar(QWidget):
    mode: TopBarMode = TopBarMode.EMPTY

    def __init__(self, parent):
        super(TopBar, self).__init__(parent)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(Margin(0))
        self.setLayout(self.layout)

        self.backBtn = Button(
            '', icon=Icons.Filled.Rounded.arrow_left_alt.update(color='#FFFFFF', background='transparent'),
            iconSize=ui.size(24, 24), padding=Padding(horizontal=ui.dp(12), vertical=ui.dp(6)),
            styleSheet=transparentButton
        )

        self.layout.addWidget(self.backBtn, alignment=Qt.AlignmentFlag.AlignLeft)

    def setMode(self, mode: TopBarMode):
        self.mode = mode
        if self.mode == TopBarMode.EMPTY:
            logger.debug('Setting TopBar to EMPTY mode')
            self.setVisible(False)
            self.backBtn.setVisible(False)
            self.setFixedHeight(0)
        elif self.mode == TopBarMode.BACK:
            self.setVisible(True)
            self.backBtn.setVisible(True)
            self.setFixedHeight(ui.dp(36))

    def setBackCallback(self, callback: Callable):
        self.backBtn.onClick(callback)
