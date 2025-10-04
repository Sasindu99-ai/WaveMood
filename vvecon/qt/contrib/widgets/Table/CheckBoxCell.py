from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox

from .BaseCell import BaseCell

__all__ = ['CheckBoxCell']


class CheckBoxCell(BaseCell):
	checkBox: QCheckBox
	_onCheckChangedCallback = NotImplemented

	def __init__(self, *args, **kwargs):
		self._onCheckChangedCallback = kwargs.get('onCheckChanged', NotImplemented)

		super(CheckBoxCell, self).__init__(*args, **kwargs)

	def setupCell(self):
		self.checkBox = QCheckBox()
		self.checkBox.setCursor(Qt.CursorShape.PointingHandCursor)
		self.checkBox.stateChanged.connect(self.onCheckChanged)

		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.layout.addWidget(self.checkBox, alignment=Qt.AlignmentFlag.AlignCenter)

	def mousePressEvent(self, a0):
		self.checkBox.click()

	def onCheckChanged(self, state):
		if self._onCheckChangedCallback is not NotImplemented:
			self._onCheckChangedCallback(state, self, self._parent)

	def setValues(self, data: bool | dict):
		self.checkBox.stateChanged.disconnect()

		if isinstance(data, dict):
			val = data['val']
			disabled = data['disabled']
			self.checkBox.setChecked(val)
			self.checkBox.setDisabled(disabled)
		else:
			self.checkBox.setChecked(data)
		self.checkBox.stateChanged.connect(self.onCheckChanged)

	def getValue(self):
		return self.checkBox.isChecked()
