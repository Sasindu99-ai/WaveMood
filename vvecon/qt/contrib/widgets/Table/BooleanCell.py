from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QLabel

from vvecon.qt.contrib.styles import Label
from vvecon.qt.res import Icons

from .BaseCell import BaseCell

__all__ = ['BooleanCell']

from .. import Padding


class BooleanCell(BaseCell):
	"""
	BooleanCell()
	"""
	correct: QLabel
	wrong: QLabel

	def setupCell(self):
		self.correct = QLabel()
		self.correct.setPixmap(
			Icons.Rounded.check.update(size=20, color='white').pixmap(QSize(20, 20))
		)
		self.correct.setStyleSheet(
			Label.successBg.update(padding=Padding(horizontal=4, vertical=2).qss, radius=12).qss
		)
		self.layout.addWidget(self.correct, alignment=Qt.AlignmentFlag.AlignCenter)

		self.wrong = QLabel()
		self.wrong.setPixmap(
			Icons.Rounded.close.update(size=20, color='white').pixmap(QSize(20, 20))
		)
		self.wrong.setStyleSheet(
			Label.errorBg.update(padding=Padding(horizontal=4, vertical=2).qss, radius=12).qss
		)
		self.layout.addWidget(self.wrong, alignment=Qt.AlignmentFlag.AlignCenter)

		self.correct.setVisible(False)
		self.wrong.setVisible(False)

	def setValues(self, data: bool):
		if data:
			self.wrong.setVisible(False)
			self.correct.setVisible(True)
		else:
			self.correct.setVisible(False)
			self.wrong.setVisible(True)
