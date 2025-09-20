from typing import Callable, List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QSizePolicy

from Components.Common import Padding
from vvecon.qt.contrib.widgets import Margin
from vvecon.qt.contrib.styles.ComboBox import comboBox

from .BaseCell import BaseCell

__all__ = ['ComboBoxCell']


class ComboBoxCell(BaseCell):
	"""
	ComboBoxCell(items: Optional[List[str]] = None)
	"""
	_items: List[str]
	_padding: Padding = Padding(0)
	_margin: Margin = Margin(0)
	_width: Optional[int] = None
	_height: Optional[int] = None
	_callback: Optional[Callable] = None
	comboBox: QComboBox

	def __init__(self, *args, **kwargs):
		self._items = kwargs.get('items', [])
		self._padding = kwargs.get('padding', self._padding)
		self._margin = kwargs.get('margin', self._margin)
		self._width = kwargs.get('width', self._width)
		self._height = kwargs.get('height', self._height)
		self._callback = kwargs.get('callback', self._callback)

		super(ComboBoxCell, self).__init__(*args, **kwargs)

	def setupCell(self):
		self.comboBox = QComboBox(self)
		self.comboBox.setCursor(Qt.CursorShape.PointingHandCursor)
		self.comboBox.addItems(self._items)
		self.comboBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
		self.setContentsMargins(self._margin)
		self.comboBox.setStyleSheet(comboBox.update(padding=self._padding.qss).qss)
		if self._width:
			self.comboBox.setFixedWidth(self._width)
		if self._height:
			self.comboBox.setFixedHeight(self._height)

		self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
		self.layout.addWidget(self.comboBox, alignment=Qt.AlignmentFlag.AlignCenter)

		if self._callback:
			self.comboBox.currentIndexChanged.connect(self.onChanged)

	def setValues(self, data: List):
		self.comboBox.clear()
		for datum in data:
			self.comboBox.addItem(datum.get('label', ''), datum.get('value', None))
			if datum.get('selected', False):
				self.comboBox.setCurrentIndex(self.comboBox.count() - 1)

	def getValue(self):
		return self.comboBox.currentData()

	def getText(self):
		return self.comboBox.currentText()

	def onChanged(self):
		val = self.comboBox.itemData(self.comboBox.currentIndex())
		self._callback(val, self._parent)
