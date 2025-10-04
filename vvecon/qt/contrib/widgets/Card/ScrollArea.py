from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QScrollArea

__all__ = ['ScrollArea']


class ScrollArea(QScrollArea):
	resized: pyqtSignal = pyqtSignal()
	verticalScrollBarStateChanged: pyqtSignal = pyqtSignal(bool)
	horizontalScrollBarStateChanged: pyqtSignal = pyqtSignal(bool)

	verticalScrollBarLastState: bool = True
	horizontalScrollBarLastState: bool = True

	def resizeEvent(self, a0):
		super().resizeEvent(a0)
		self.checkVerticalScrollBarState()
		self.checkHorizontalScrollBarState()

	def checkVerticalScrollBarState(self):
		verticalScrollBarState = self.verticalScrollBar().isVisible()
		if self.verticalScrollBarLastState != verticalScrollBarState:
			self.verticalScrollBarLastState = verticalScrollBarState
			self.verticalScrollBarStateChanged.emit(verticalScrollBarState)

	def checkHorizontalScrollBarState(self):
		horizontalScrollBarState = self.horizontalScrollBar().isVisible()
		if self.horizontalScrollBarLastState != horizontalScrollBarState:
			self.horizontalScrollBarLastState = horizontalScrollBarState
			self.horizontalScrollBarStateChanged.emit(horizontalScrollBarState)
