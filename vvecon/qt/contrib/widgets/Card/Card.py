from typing import Optional

from PyQt6.QtWidgets import QVBoxLayout, QWidget, QFrame

from vvecon.qt.contrib.styles.Card import primaryCard
from vvecon.qt.contrib.widgets import Margin
from vvecon.qt.util import Style

__all__ = ['Card']


class Card(QFrame):
	parent: Optional[QWidget]

	def __init__(
            self, parent: Optional[QWidget] = None, margin: Optional[Margin] = None, style: str | Style = primaryCard
    ):
		super().__init__(parent)
		self.parent = parent

		if margin is None:
			margin = Margin(0)

		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(margin)
		self.setLayout(self.layout)

		self.setStyleSheet(style if isinstance(style, str) else style.qss)
