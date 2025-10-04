from typing import Any, Callable, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from vvecon.qt.contrib.widgets import Margin, Padding

from .BaseCell import BaseCell

__all__ = ['Cell']


class Cell(BaseCell):
	"""
	Cell(extract: Optional[Callable] = None, reformat: Optional[str] = None)
	"""
	_reformat: Optional[str]
	_extract: Optional[Callable]
	_padding: Padding = Padding(0)
	_margin: Margin = Margin(0)
	label: QLabel

	def __init__(self, *args, **kwargs):
		self._extract = kwargs.get('extract')
		self._reformat = kwargs.get('reformat')

		self.textAlign = kwargs.get('textAlign', Qt.AlignmentFlag.AlignCenter)
		self._padding = kwargs.get('padding', self._padding)
		self._margin = kwargs.get('margin', self._margin)
		super(Cell, self).__init__(*args, **kwargs)

	def setupCell(self):
		self.label = QLabel(self)
		self.label.setWordWrap(False)
		self.label.setAlignment(self.textAlign)
		self.label.setStyleSheet(self._styleScheme.label.update(**dict(
			padding=self._padding.qss
		)).qss)

		self.layout.setContentsMargins(self._margin)
		self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignVCenter)

	def setValues(self, data: Any):
		try:
			if self._extract:
				arguments, keywords = self._extract(data)
				self.label.setText(
					self._reformat.format(*arguments, **keywords) if self._reformat else arguments[0]
				)
				return
			if isinstance(data, (list, tuple)) and len(data) == 2 and (
				isinstance(data[0], (tuple, list))
			) and isinstance(data[1], dict):
				arguments, keywords = data
				self.label.setText(
					self._reformat.format(*arguments, **keywords) if self._reformat else arguments[0]
				)
				return
			if isinstance(data, (tuple, list)):
				self.label.setText(self._reformat.format(*data) if self._reformat else data)
				return
			if isinstance(data, dict):
				self.label.setText(self._reformat.format(**data) if self._reformat else data)
				return
			self.label.setText(self._reformat.format(data) if self._reformat else data)
		except IndexError:
			raise ValueError('Invalid data, unable to extract values')
