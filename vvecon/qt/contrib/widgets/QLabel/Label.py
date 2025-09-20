from typing import Callable, Optional

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

__all__ = ['Label']


class Label(QLabel):
	def __init__(
		self, *args, text: str = '', font: Optional[QFont] = None, onClick: Optional[Callable] = None, **kwargs
	):
		super(Label, self).__init__(*args, **kwargs)

		self.setText(text)
		self.onClick = onClick

		if font:
			self.setFont(font)

	def mousePressEvent(self, ev):
		# super().mousePressEvent(ev)
		if callable(self.onClick):
			self.onClick()
