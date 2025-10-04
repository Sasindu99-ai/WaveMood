from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QWidget

from vvecon.qt.contrib.widgets import Margin
from vvecon.qt.util import ui

from .ScrollArea import ScrollArea

__all__ = ['ScrollableCard']

_scrollAreaStyleSheet = """
QScrollArea {
	border: none;
	background: transparent;
}

QScrollBar:vertical {
	border: none;
	background-color: transparent;
	border-radius: 8px;
	width: 18px;
	margin-left: 10px;
}

QScrollBar::handle:vertical {
	background: #287DC5;
	border-radius: 3px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
	border: none;
	height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
	background: transparent;
}
"""

_styleSheet = """
QFrame{
	background-color: #FAFAFA;
}
QFrame#border{
	border-radius: 3px;
	border: 1px solid #D9D9D9;
}
"""


class ScrollableCard(QFrame):
	scrollBarVisibilityChanged: pyqtSignal = pyqtSignal(bool)
	parent: Optional[QWidget]

	def __init__(self, parent: Optional[QWidget] = None, margin: Optional[Margin] = None):
		super().__init__(parent)
		self.setObjectName('border')

		self.parent = parent

		if margin is None:
			margin = Margin(0)

		self.mainLayout = QVBoxLayout(self)
		self.mainLayout.setContentsMargins(margin)
		self.setLayout(self.mainLayout)

		self.scrollArea = ScrollArea(self)
		self.scrollArea.setContentsMargins(Margin(0))
		self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.verticalScrollBarStateChanged.connect(self.onScrollAreaResized)

		self.scrollAreaWidget = QWidget(self)
		self.scrollAreaWidget.setStyleSheet('background-color: transparent;')
		self.scrollAreaWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.scrollArea.setWidget(self.scrollAreaWidget)

		self.layout = QVBoxLayout(self.scrollAreaWidget)
		self.layout.setContentsMargins(Margin(0, 0, ui.dp(24), 0))
		self.scrollAreaWidget.setLayout(self.layout)

		self.mainLayout.addWidget(self.scrollArea)

		self.setScrollAreaStyleSheet(_scrollAreaStyleSheet)
		self.setStyleSheet(_styleSheet)

	def onScrollAreaResized(self, state):
		if state:
			self.layout.setContentsMargins(Margin(0, 0, ui.dp(24), 0))
		else:
			self.layout.setContentsMargins(Margin(0))
		self.scrollBarVisibilityChanged.emit(state)

	def setScrollAreaStyleSheet(self, styleSheet):
		self.scrollArea.setStyleSheet(styleSheet)

	def setScrollAreaLayout(self, layout):
		self.scrollAreaWidget.setLayout(layout)
