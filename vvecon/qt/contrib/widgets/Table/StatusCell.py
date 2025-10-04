from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from .BaseCell import BaseCell

__all__ = ['StatusCell']


class StatusCell(BaseCell):
	label: QLabel
	_width: Optional[int] = 100
	_height: int = 30

	def __init__(self, *args, **kwargs):
		self._width = kwargs.get('width', self._width)
		self._height = kwargs.get('height', self._height)

		super(StatusCell, self).__init__(*args, **kwargs)

	def setupCell(self):
		self.label = QLabel('Test')
		self.label.setFixedHeight(30)
		self.label.setContentsMargins(20, 5, 20, 5)
		self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

	def setValues(self, data: str):
		self.label.setText(str(data))
		self.label.setStyleSheet(f"""
			font-size: 12px;
			color: white;
			border-radius: 3px;
			background-color: {self.getColor(data.lower())};
		""")

	@staticmethod
	def getColor(status):
		if status == 'pending':
			return '#5D5D5D'
		elif status == 'approved':
			return '#13AE82'
		elif status == 'confirmed':
			return '#FFCC00'
		else:
			return '#3D6AFF'
