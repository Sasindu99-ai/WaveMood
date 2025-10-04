from typing import List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon


from .BaseCell import BaseCell

__all__ = ['ButtonCell']


class ButtonCell(BaseCell):
	"""
	ActionCell(actions: Optional[List[Dict[str, Any]] = None)
	"""
	_actions: List[dict] = []

	def __init__(self, *args, **kwargs):
		self._actions = kwargs.get('actions', [])
		super(ButtonCell, self).__init__(*args, **kwargs)

		self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		# self.layout.setSpacing(10)

	def setupCell(self):
		for action in self._actions:
			btn = QPushButton()
			btn.setStyleSheet('background-color: transparent; border: none;')
			btn.setIcon(QIcon(action['icon']))
			btn.setFixedSize(30, 30)
			if action.get('action'):
				btn.clicked.connect(lambda _, a=action['action']: a(self._parent.data))
			self.layout.addWidget(btn)

	def setValues(self, data: Optional[dict] = None):
		pass
