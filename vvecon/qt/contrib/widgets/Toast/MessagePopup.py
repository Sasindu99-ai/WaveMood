from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import (
	QDialog,
	QFrame,
	QGraphicsDropShadowEffect,
	QHBoxLayout,
	QLabel,
	QSizePolicy,
	QVBoxLayout,
)

from vvecon.qt.contrib.widgets import Margin, Padding
from vvecon.qt.contrib.widgets.QButton import Button
from vvecon.qt.contrib.widgets.Toast.ToastStyleScheme import (
	dangerToastStyleSheet,
	successToastStyleSheet,
	warningToastStyleSheet,
)
from vvecon.qt.res import Icons
from vvecon.qt.util import ui
from .ToastStyleScheme import ToastStyleScheme

__all__ = ['MessagePopup', 'SuccessPopup', 'DangerPopup', 'WarningPopup']


class Colors:
	success = '#4BB543'
	danger = '#FF3333'
	warning = '#FFCC00'
	info = '#3399FF'


class MessagePopup(QDialog):
	def __init__(
		self,
		parent=None,
		title: str = '',
		msg: str = '',
		img: QPixmap = Icons.Rounded.info.update(color=Colors.info, size=ui.dp(84)).toPixmap(),
		confirmText: str = 'Proceed',
		styleScheme: ToastStyleScheme = ToastStyleScheme(),
		margin: Margin = Margin(vertical=ui.dp(40), horizontal=ui.dp(80))
	):
		super(MessagePopup, self).__init__()
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

		self.parent = parent
		self.showOverlay()

		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(Margin(0))
		self.setLayout(self.layout)

		self.body = QFrame()
		self.body.setMinimumWidth(ui.dp(480))
		self.body.layout = QVBoxLayout(self.body)
		self.body.layout.setContentsMargins(margin)
		self.body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
		self.body.setStyleSheet(styleScheme.background.qss)
		self.body.setLayout(self.body.layout)

		shadow_effect = QGraphicsDropShadowEffect(self)
		shadow_effect.setBlurRadius(ui.dp(60))
		shadow_effect.setOffset(0, 0)
		shadow_effect.setColor(QColor(0, 0, 0, 80))

		self.body.setGraphicsEffect(shadow_effect)

		self.image = QLabel()
		self.image.setPixmap(img)
		self.image.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

		self.title = QLabel(title)
		self.title.setStyleSheet(styleScheme.title.qss)
		self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.message = QLabel(msg)
		self.message.setStyleSheet(styleScheme.message.qss)
		self.message.setWordWrap(True)
		self.message.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
		self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.buttonSection = QFrame()
		self.buttonSection.layout = QHBoxLayout(self.buttonSection)
		self.buttonSection.layout.setContentsMargins(0, 0, 0, 0)
		self.buttonSection.layout.setSpacing(ui.dp(8))

		self.confirmBtn = Button(
			text=confirmText,
			tooltip=confirmText,
			padding=Padding(ui.dp(20), ui.dp(12)),
			style=Qt.ToolButtonStyle.ToolButtonTextOnly
		)
		self.confirmBtn.setStyleSheet(styleScheme.confirmButton.qss)

		self.buttonSection.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.buttonSection.layout.addWidget(self.confirmBtn)

		self.body.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.body.layout.addWidget(self.image)
		self.body.layout.addWidget(self.title)
		self.body.layout.addWidget(self.message)
		self.body.layout.addWidget(self.buttonSection)

		self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.layout.addWidget(self.body)

		self.confirmBtn.onClick(self.onConfirm)

		self.exec()

	def onConfirm(self):
		self.hideOverlay()
		self.accept()

	def showOverlay(self):
		if self.parent and hasattr(self.parent, 'showSpinner'):
			self.parent.showSpinner()

	def hideOverlay(self):
		if self.parent and hasattr(self.parent, 'hideSpinner'):
			self.parent.hideSpinner()

	def destroy(self, **kwargs):
		self.hideOverlay()
		super().destroy(**kwargs)

	def keyPressEvent(self, event):
		if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
			self.onConfirm()
		else:
			super().keyPressEvent(event)


class SuccessPopup(MessagePopup):
	def __init__(
		self,
		parent=None,
		title: str = '',
		msg: str = '',
		img: QPixmap = Icons.Rounded.check_circle.update(color=Colors.success, size=ui.dp(84)).toPixmap(),
		confirmText: str = 'Proceed',
		styleScheme: ToastStyleScheme = successToastStyleSheet,
		margin: Margin = Margin(vertical=ui.dp(40), horizontal=ui.dp(80))
	):
		super(SuccessPopup, self).__init__(
			parent, title, msg, img, confirmText, styleScheme, margin
		)


class DangerPopup(MessagePopup):
	def __init__(
		self,
		parent=None,
		title: str = '',
		msg: str = '',
		img: QPixmap = Icons.Rounded.error.update(color=Colors.danger, size=ui.dp(84)).toPixmap(),
		confirmText: str = 'Proceed',
		styleScheme: ToastStyleScheme = dangerToastStyleSheet,
		margin: Margin = Margin(vertical=ui.dp(40), horizontal=ui.dp(80))
	):
		super(DangerPopup, self).__init__(
			parent, title, msg, img, confirmText, styleScheme, margin
		)


class WarningPopup(MessagePopup):
	def __init__(
		self,
		parent=None,
		title: str = '',
		msg: str = '',
		img: QPixmap = Icons.Rounded.warning.update(color=Colors.warning, size=ui.dp(84)).toPixmap(),
		confirmText: str = 'Okay',
		styleScheme: ToastStyleScheme = warningToastStyleSheet,
		margin: Margin = Margin(vertical=ui.dp(40), horizontal=ui.dp(80))
	):
		super(WarningPopup, self).__init__(
			parent, title, msg, img, confirmText, styleScheme, margin
		)
