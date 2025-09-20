from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from vvecon.qt.contrib.styles.Card import primaryCard
from vvecon.qt.contrib.styles.Label import transparentBg
from vvecon.qt.contrib.widgets import Margin
from vvecon.qt.contrib.widgets.Card import Card as CardWidget
from vvecon.qt.contrib.widgets.QLabel import Label
from vvecon.qt.util import ui

__all__ = ['Card']


class Card(CardWidget):
    def __init__(
            self, parent: Optional[QWidget] = None, title: str = '', image: Optional[QPixmap] = None,
            description: str = ''
    ):
        super(Card, self).__init__(
            parent, margin=Margin(horizontal=12, vertical=6),
            style=primaryCard.update(
                color='#FFFFFF', backgroundColor='#2C2C2C', borderColor='#444444', borderWidth=1, borderRadius=8
            )
        )

        self.layout.setSpacing(ui.dp(8))
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.image = Label()
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setStyleSheet(transparentBg.qss)

        self.title = Label()
        self.title.setWordWrap(True)
        self.title.setStyleSheet(transparentBg.update(fontSize=ui.sp(14), color='#FFFFFF').qss)

        self.description = Label()
        self.description.setWordWrap(True)
        self.description.setStyleSheet(transparentBg.update(fontSize=ui.sp(12), color='#666666').qss)

        self.layout.addWidget(self.image, stretch=1)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.description)

        self.setTitle(title)
        self.setDescription(description)
        if image:
            self.setImage(image)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def setTitle(self, title: str):
        self.title.setText(title)

    def setDescription(self, description: str):
        self.description.setText(description)

    def setImage(self, image: QPixmap):
        self.image.setPixmap(image.scaled(
            ui.size(100, 100), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
