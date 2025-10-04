from typing import Dict, List, Optional

from PyQt6.QtCore import QPoint, QSize, Qt
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

from vvecon.qt.contrib.widgets.QButton import Button
from vvecon.qt.contrib.styles.Menu import menu
from vvecon.qt.contrib.styles.Button import transparentButton
from vvecon.qt.logger import logger
from vvecon.qt.res import Icons

from .BaseCell import BaseCell

__all__ = ['ActionCell']

from .. import Padding


class ActionCell(BaseCell):
	"""
	ActionCell(actions: Optional[List[Dict[str, Any]] = None)
	"""
	_actions: List = []
	_actionWidgets: Dict[str, QAction] = dict()
	button: Button
	menu: QMenu

	def __init__(self, *args, **kwargs):
		self._actions = [
			action | (dict() if 'key' in action else dict(key=action.get('label', '')))
			for action in kwargs.get('actions', [])
		]

		super(ActionCell, self).__init__(*args, **kwargs)

	def setupCell(self):
		self.button = Button(
			icon=Icons.Filled.Rounded.more_horiz,
			iconSize=QSize(20, 20),
			padding=Padding(vertical=4, horizontal=8),
			style=Qt.ToolButtonStyle.ToolButtonIconOnly
		)
		transparentButton.apply(self.button)

		self.menu = QMenu()
		self.menu.setCursor(Qt.CursorShape.PointingHandCursor)
		menu.apply(self.menu)
		for action in self._actions:
			def makeCallback(act):
				return lambda: act.get('callback', lambda _: logger.info('No Action is set.'))(self._parent.data)

			actionWidget = QAction(action.get('label', ''), self.menu)
			actionWidget.setEnabled(action.get('enabled', True))
			actionWidget.setVisible(action.get('visible', True))
			if icon := action.get('icon'):
				actionWidget.setIcon(icon)
			self._actionWidgets[action.get('key', '')] = actionWidget
			self._actionWidgets[action.get('key', '')].triggered.connect(makeCallback(action))
			self.menu.addAction(self._actionWidgets[action.get('key', '')])

		self.layout.addWidget(self.button)

		self.button.onPress(self.onActionButton)

	def onActionButton(self, event):
		if not hasattr(self, 'menu'):
			return
		self.menu.raise_()
		self.menu.exec(event.globalPosition().toPoint() - QPoint(100, 0))

	def setValues(self, data: Optional[dict] = None):
		if data is None:
			return
		for key, actionData in data.items():
			self._actionWidgets[key].setEnabled(actionData.get('enabled', True))
			self._actionWidgets[key].setVisible(actionData.get('visible', True))
			if label := actionData.get('label'):
				self._actionWidgets[key].setText(label)
			if icon := actionData.get('icon'):
				self._actionWidgets[key].setIcon(icon)
			if shortcut := actionData.get('shortcut'):
				self._actionWidgets[key].setShortcut(shortcut)
