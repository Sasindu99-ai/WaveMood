from typing import Optional, Type, Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLayout, QVBoxLayout, QWidget

from vvecon.qt.contrib.widgets import Margin

__all__ = ['Widget']


class Widget(QWidget):
	_layout: Type[QLayout]

	def __init__(
		self,
		parent: Optional[Type[QWidget] | QWidget] = None,
		layout: Type[QLayout] = QVBoxLayout,
		spacing: int = 0,
		margin: Optional[Margin] = None,
		alignment: Union[Qt.AlignmentFlag] = Qt.AlignmentFlag.AlignLeft,
		**kwargs
	):
		super(Widget, self).__init__(parent, **kwargs)
		self.parent = parent

		self._layout = layout(self)
		self._layout.setSpacing(spacing)
		self._layout.setContentsMargins(margin if margin else Margin(0))
		self._layout.setAlignment(alignment)
		self.setStyleSheet('background-color: transparent')
		self.setLayout(self._layout)

	def addWidget(self, w: QWidget, **kwargs):
		self._layout.addWidget(w, **kwargs)

	def addLayout(self, layout: QLayout, **kwargs):
		self._layout.addLayout(layout, **kwargs)

	def addSpacing(self, spacing: int):
		self._layout.addSpacing(spacing)

	def addStretch(self, stretch: int = 1):
		self._layout.addStretch(stretch)

	def getLayout(self):
		return self._layout
