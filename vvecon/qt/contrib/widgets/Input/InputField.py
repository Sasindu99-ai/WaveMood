from datetime import datetime
from typing import Callable, Optional

from PyQt6.QtCore import QDate, QSize, Qt, QTimer, pyqtSignal, QEvent
from PyQt6.QtGui import QColor, QIcon, QPixmap
from PyQt6.QtWidgets import (
	QDialog,
	QFrame,
	QGraphicsDropShadowEffect,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QSizePolicy,
	QSpacerItem,
	QVBoxLayout,
)

from vvecon.qt.enums import InputType
from vvecon.qt.res import Icons
from vvecon.qt.util import Util, ui
from .StyleScheme import StyleScheme
from .. import Button
from ..Calender.CalenderPopup import CalendarPopup
from ..Toast import WarningPopup

__all__ = ['InputField']

from ... import styles


class LineEdit(QLineEdit):
	finishEditing = pyqtSignal()

	def __init__(self, parent=None, *args, **kwargs):
		super(QLineEdit, self).__init__(parent, *args, **kwargs)
		self.returnPressed.connect(self.emitFinishEditing)
		self.focusOutEvent = self.customFocusOutEvent
		self.backspaceHeld = False
		self.timer = QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.emitFinishEditing)

	def emitFinishEditing(self):
		self.finishEditing.emit()

	def customFocusOutEvent(self, event):
		self.emitFinishEditing()
		super().focusOutEvent(event)

	def keyPressEvent(self, event):
		super().keyPressEvent(event)
		if event.key() == Qt.Key.Key_Backspace:
			self.backspaceHeld = True
			self.timer.start(100)

	def keyReleaseEvent(self, event):
		super().keyReleaseEvent(event)
		if event.key() == Qt.Key.Key_Backspace and self.backspaceHeld:
			self.backspaceHeld = False
			self.timer.start(1000)


class InputField(QFrame):
	inputEdit: LineEdit
	iconLabel = None
	plusButton = None
	minusButton = None
	dateButton = None
	name: str = ''
	showTooltipIcon: bool = False
	dateSelected = pyqtSignal(str)
	_validator: Optional[Callable] = None
	_onEnterCallback: Optional[Callable] = None
	inputClicked = pyqtSignal()

	styleScheme: StyleScheme = StyleScheme()

	def __init__(
		self,
		parent=None,
		name='',
		inType: InputType = InputType.TEXT,
		width=None,
		height=40,
		hint=None,
		placeholder='',
		isLight=False,
		icon=None,
		step: float = 0,
		maxVal=None,
		minVal=None,
		showTooltipIcon: bool = False,
		validator: Optional[Callable] = None,
		styleScheme: Optional[StyleScheme] = None,
		default = None
	):
		super(InputField, self).__init__(parent)

		self.name = name
		self.heightVal = height
		self.widthVal = width
		self.toast = None
		self.hint = hint if hint else None
		self.placeholder = placeholder
		self.inType = inType
		self.icon = icon
		self.step = step if step else 1
		self.maxValue = maxVal
		self.minValue = minVal
		self.showTooltipIcon = showTooltipIcon
		self._validator = validator
		if styleScheme:
			self.styleScheme = styleScheme

		if self.inType == InputType.SEARCH:
			isLight = True

		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

		self.label = QLabel(self.name)
		self.styleScheme.label.apply(self.label)  # type: ignore

		self.bottomSection = QFrame()
		self.bottomSection.layout = QHBoxLayout(self.bottomSection)
		self.bottomSection.layout.setContentsMargins(0, 0, 0, 0)
		self.bottomSection.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

		self.inputContainer = QFrame()
		self.inputContainer.layout = QHBoxLayout(self.inputContainer)
		self.inputContainer.layout.setContentsMargins(10, 0, 10, 0)
		self.inputContainer.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.inputContainer.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

		if isLight or self.inType == InputType.SEARCH:
			self.styleScheme.searchContainer.apply(self.inputContainer)  # type: ignore
		else:
			self.styleScheme.container.apply(self.inputContainer)  # type: ignore

		if self.widthVal and self.heightVal:
			self.inputContainer.setFixedSize(QSize(
				self.widthVal, self.heightVal
			))
		elif self.widthVal and not self.heightVal:
			self.setFixedWidth(self.widthVal)
		elif not self.widthVal and self.heightVal:
			self.inputContainer.setFixedHeight(self.heightVal)

		self.inputEdit = QLineEdit()
		self.styleScheme.lineEdit.apply(self.inputEdit)  # type: ignore
		if self.placeholder:
			self.inputEdit.setPlaceholderText(self.placeholder)
		self.inputEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

		if default is not None:
			self.inputEdit.setText(str(default))

		self.hintButton = Button(
			icon=Icons.Filled.Rounded.add,
			iconSize=ui.size(20, 20),
			styleSheet='background-color: transparent; border: none;',
			onClick=lambda: self.show_toast(self.hint)
		)
		self.hintButton.setFixedSize(ui.size(35, 35))
		self.hintButton.installEventFilter(self)
		self.bottomSection.layout.addWidget(self.hintButton)

		self.bottomSection.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.bottomSection.layout.setSpacing(ui.dp(10))
		self.bottomSection.layout.addWidget(self.inputContainer)
		self.bottomSection.layout.addWidget(self.hintButton)

		self.bottomLabel = QLabel(name)
		self.styleScheme.bottomLabel.apply(self.bottomLabel)  # type: ignore

		self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
		self.layout.setSpacing(7)
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.bottomSection)
		self.layout.addWidget(self.bottomLabel)

		self.updateInputField()

		self.returnPressed.connect(self._onEnter)

	def updateInputField(self):
		if self.name:
			self.label.show()
		else:
			self.label.hide()
		if not self.inType == InputType.SEARCH:
			self.resetFormatting()
		if self.hint and self.showTooltipIcon:
			self.hintButton.show()
		else:
			self.hintButton.hide()

		if self.inType == InputType.TEXT:
			self.generateTextInput()
			self.installEventFilter(self)
		elif self.inType == InputType.NUMBER:
			self.generateNumberInput()
			self.inputEdit.installEventFilter(self)
		elif self.inType == InputType.SEARCH:
			self.generateSearchInput()
		elif self.inType == InputType.DATE:
			self.generateDateInput()
			self.inputEdit.installEventFilter(self)

	def setValue(self, val):
		if self.inType == InputType.TEXT:
			self.inputEdit.setText(str(val))
		elif self.inType == InputType.NUMBER and isinstance(self.step, int):
			try:
				intVal = int(float(val))
			except ValueError:
				intVal = 0
			self.inputEdit.setText(str(intVal))
		elif self.inType == InputType.NUMBER and isinstance(self.step, float):
			self.inputEdit.setText(str(val))
		elif self.inType == InputType.DATE:
			if isinstance(val, datetime):
				self.inputEdit.setText(val.strftime('%Y-%m-%d'))

	def getValue(self):
		if self.inType == InputType.TEXT or self.inType == InputType.SEARCH:
			return self.inputEdit.text()
		elif self.inType == InputType.NUMBER and isinstance(self.step, int):
			val = (
				int(self.inputEdit.text())
				if self.inputEdit.text() != '' and self.inputEdit.text() != '-'
				else 0
			)
			cursorCursor = self.inputEdit.cursorPosition()
			self.setValue(val)
			self.inputEdit.setCursorPosition(cursorCursor)
			return val
		elif self.inType == InputType.NUMBER and isinstance(self.step, float):
			val = (
				float(self.inputEdit.text())
				if self.inputEdit.text() != '' and self.inputEdit.text() != '-'
				else 0.0
			)
			cursorCursor = self.inputEdit.cursorPosition()
			self.setValue(val)
			self.inputEdit.setCursorPosition(cursorCursor)
			return val
		elif self.inType == InputType.DATE:
			if self.inputEdit.text() != '':
				return datetime.strptime(self.inputEdit.text(), '%Y-%m-%d')
			else:
				return None
		return None

	def generateTextInput(self):
		self.inputContainer.layout.insertWidget(0, self.inputEdit)
		self.inputContainer.installEventFilter(self)
		if self.icon:
			self.iconLabel = QLabel()
			self.iconLabel.setStyleSheet("""background-color: transparent; border: none;""")
			self.iconLabel.installEventFilter(self)
			self.iconLabel.setPixmap(
				self.icon.pixmap(ui.size(20, 20)).scaled(
					20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
			self.inputContainer.layout.addWidget(self.iconLabel)

	def generateNumberInput(self):
		self.plusButton = Button(
			icon=Icons.Filled.Rounded.add,
			iconSize=ui.size(20, 20),
			styleSheet='background-color: transparent; border: none;',
			onClick=self.increaseValue
		)
		self.plusButton.setFixedSize(ui.size(40, 25))

		self.minusButton = Button(
			icon=Icons.Filled.Rounded.remove,
			iconSize=ui.size(20, 20),
			styleSheet='background-color: transparent; border: none;',
			onClick=self.decreaseValue
		)
		self.minusButton.setFixedSize(ui.size(40, 25))

		if self.step and isinstance(self.step, int):
			self.inputEdit.setText('0')
		elif self.step and isinstance(self.step, float):
			self.inputEdit.setText('0.0')

		self.inputContainer.layout.insertWidget(0, self.inputEdit)
		self.inputContainer.layout.addWidget(self.plusButton)
		self.inputContainer.layout.addWidget(self.minusButton)

		self.inputEdit.editingFinished.connect(self.checkMaxAndMin)

	def generateSearchInput(self):
		self.label.hide()
		self.hintButton.hide()
		self.bottomLabel.hide()

		self.icon = QLabel()
		self.icon.setPixmap(QPixmap(Icons.Rouneded.search).scaled(
			15, 15, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
		self.icon.setStyleSheet("""
			border: none;
		""")
		self.inputContainer.layout.setContentsMargins(10, 0, 10, 0)
		self.inputContainer.layout.setSpacing(15)
		self.inputContainer.layout.addWidget(self.icon)
		self.inputContainer.layout.addWidget(self.inputEdit)

	def generateDateInput(self):
		self.inputContainer.layout.insertWidget(0, self.inputEdit)
		self.dateButton = Button(
			icon=QIcon(
				QPixmap(Icons.Rounded.calender).scaled(ui.dp(30), ui.dp(30), Qt.AspectRatioMode.KeepAspectRatio)
			),
			iconSize=ui.size(30, 30),
			styleSheet=styles.Properties.bgTransparent.qss,
			onClick=self.show_calendar_dialog
		)
		self.inputContainer.layout.addWidget(self.dateButton)

		self.inputEdit.setPlaceholderText('YYYY-MM-DD')
		self.inputEdit.setReadOnly(True)

		self.dateButton.clicked.connect(self.show_calendar_dialog)

	def resetFormatting(self):
		self.bottomLabel.hide()
		self.styleScheme.container.apply(self.inputContainer)

	def displayError(self, msg: str):
		self.styleScheme.errorContainer.apply(self.inputContainer)  # type: ignore
		self.bottomLabel.show()
		self.styleScheme.errorBottomLabel.apply(self.bottomLabel)  # type: ignore
		self.bottomLabel.setText(msg if msg else 'Error')
		self.inputEdit.setFocus()

	def displaySuccess(self, msg: str):
		self.styleScheme.successContainer.apply(self.inputContainer)  # type: ignore
		self.bottomLabel.show()
		self.styleScheme.successBottomLabel.apply(self.bottomLabel)  # type: ignore
		self.bottomLabel.setText(msg if msg else 'Error')

	def show_toast(self, message):
		if not self.toast:
			self.toast = WarningPopup(self, 'Waring', message)

		button_pos = self.hintButton.mapToGlobal(
			self.hintButton.rect().topRight())
		self.toast.show_at(button_pos)

	def increaseValue(self):
		if self.step:
			scale = 10 ** len(str(self.step).split('.')[1]) if isinstance(self.step, float) else 1
			value = int(float(self.inputEdit.text()) * scale) if self.inputEdit.text() != '' else 0
			step = int(self.step * scale)
			value += step
			decimal_places = len(str(self.step).split('.')[1]) if isinstance(self.step, float) else 0
			finalValue = f'{value / scale:.{decimal_places}f}'
			if self.maxValue is not None and float(self.maxValue) >= float(finalValue):
				self.inputEdit.setText(finalValue)
			elif self.maxValue is None:
				self.inputEdit.setText(finalValue)

	def decreaseValue(self):
		if self.step:
			scale = 10 ** len(str(self.step).split('.')[1]) if isinstance(self.step, float) else 1
			value = int(float(self.inputEdit.text()) * scale) if self.inputEdit.text() != '' else 0
			step = int(self.step * scale)
			value -= step
			decimal_places = len(str(self.step).split('.')[1]) if isinstance(self.step, float) else 0
			finalValue = f'{value / scale:.{decimal_places}f}'
			if self.minValue is not None and float(self.minValue) <= float(finalValue):
				self.inputEdit.setText(finalValue)
			elif self.minValue is None:
				self.inputEdit.setText(finalValue)

	def show_calendar_dialog(self):
		dialog = QDialog(self)
		dialog.setWindowFlag(Qt.WindowType.FramelessWindowHint)
		dialog.resize(200, 640)
		dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

		dialog.layout = QVBoxLayout(dialog)
		dialog.layout.setContentsMargins(50, 50, 50, 50)

		body = QFrame()
		body.setLayout(QVBoxLayout())
		body.setStyleSheet('border-radius: 16px;background-color: #F5F5F5;')

		shadow_effect = QGraphicsDropShadowEffect(dialog)
		shadow_effect.setBlurRadius(60)
		shadow_effect.setOffset(0, 0)
		shadow_effect.setColor(QColor(0, 0, 0, 80))

		body.setGraphicsEffect(shadow_effect)

		body.layout().setContentsMargins(20, 20, 20, 20)
		body.layout().setSpacing(30)

		calendar = CalendarPopup(body)

		if self.inputEdit.text():
			selected_date = QDate.fromString(self.inputEdit.text(), 'yyyy-MM-dd')
		else:
			selected_date = QDate.currentDate()

		calendar.setSelectedDate(selected_date)

		body.layout().addWidget(calendar)

		calendar.activated.connect(lambda date: self.set_date_from_calendar_signal(date, dialog))

		button_layout = QHBoxLayout()
		button_layout.setContentsMargins(20, 0, 20, 0)

		clear_button = Button(
			text='Clear',
			styleSheet=styles.Button.secondaryButton.qss,
			onClick=lambda: self.clear_selected_date(calendar, dialog)
		)
		clear_button.setCursor(Qt.CursorShape.PointingHandCursor)

		spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

		ok_button = Button(
			text='OK',
			styleSheet=styles.Button.primaryButton.qss,
			onClick=lambda: self.set_date_from_calendar_signal(calendar.selectedDate(), dialog)
		)
		ok_button.setCursor(Qt.CursorShape.PointingHandCursor)

		cancel_button = Button(
			text='Cancel',
			styleSheet=styles.Button.secondaryButton.qss,
			onClick=dialog.reject
		)
		cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

		button_layout.setSpacing(30)
		button_layout.addWidget(clear_button)
		button_layout.addItem(spacer)
		button_layout.addWidget(ok_button)
		button_layout.addWidget(cancel_button)
		button_layout.setAlignment(clear_button, Qt.AlignmentFlag.AlignLeft)
		button_layout.setAlignment(ok_button, Qt.AlignmentFlag.AlignRight)
		button_layout.setAlignment(cancel_button, Qt.AlignmentFlag.AlignRight)
		body.layout().addLayout(button_layout)

		dialog.layout.addWidget(body)

		dialog.exec()

	def set_date_from_calendar_signal(self, date, dialog):
		self.inputEdit.setText(date.toString('yyyy-MM-dd'))
		dialog.accept()
		self.dateSelected.emit(self.inputEdit.text())

	def clear_selected_date(self, calendar, dialog):
		self.inputEdit.clear()
		calendar.setSelectedDate(QDate())
		dialog.accept()

	def checkMaxAndMin(self):
		if self.inputEdit.text() == '':
			return
		if isinstance(self.step, int):
			val = int(self.inputEdit.text())
			if self.maxValue is not None and val > self.maxValue:
				val = int(self.maxValue)
			elif self.minValue is not None and val < self.minValue:
				val = int(self.minValue)
		else:
			val = float(self.inputEdit.text())
			if self.maxValue is not None and val > self.maxValue:
				val = float(self.maxValue)
			elif self.minValue is not None and val < self.minValue:
				val = float(self.minValue)

		self.inputEdit.setText(str(val))

	def eventFilter(self, source, event):
		if hasattr(self, 'hintButton') and source == self.hintButton:
			if event.type() == QEvent.Type.Enter:  # Mouse hover starts
				self.show_toast(self.hint)
			elif event.type() == QEvent.Type.Leave:  # Mouse hover ends
				if self.toast:
					self.toast.hide()

		elif hasattr(self, 'inputEdit') and source == self.inputEdit and self.inType == InputType.NUMBER:
			if event.type() == QEvent.Type.KeyPress:
				key = event.key()
				text = event.text()
				if (
					key in (
					Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_Left, Qt.Key.Key_Right,
					Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Enter, Qt.Key.Key_Return,  # Allow Enter/Return keys
					Qt.Key.Key_Alt, Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_End
					)
					or text.isdigit()
					or text == '-'
					or (isinstance(self.step, float) and text == '.')
				):
					return super(InputField, self).eventFilter(source, event)
				else:
					# Handle invalid input
					self.inputEdit.setText('0')  # Reset to 0 for invalid input
					return True  # Consume the event
		elif self.inType == InputType.DATE:
			if event.type() == QEvent.Type.MouseButtonPress:
				self.show_calendar_dialog()
				return True
		elif (
				hasattr(self, 'inputContainer') and hasattr(self, 'iconLabel') and
				event.type() == QEvent.Type.MouseButtonPress and
				(source == self.iconLabel)
		):
			self.inputClicked.emit()

		return super(InputField, self).eventFilter(source, event)

	@property
	def returnPressed(self):
		return self.inputEdit.returnPressed

	def clear(self):
		self.inputEdit.clear()
		self.bottomLabel.hide()
		self.resetFormatting()
		self.updateInputField()

	def setFocus(self):
		self.inputEdit.setFocus()

	def onEnter(self, func):
		self._onEnterCallback = func

	def _onEnter(self):
		try:
			self.validate()
		except ValueError:
			pass
		if self._onEnterCallback:
			self._onEnterCallback()

	def validate(self):
		if self._validator:
			return self._validator(
				str(self.getValue()),
				Util.either(self.name, self.hint, self.placeholder, default='Input field'),
				callback=self.displayError,
			)
		return True

	def getValidatedValue(self):
		if self.validate():
			return self.getValue()

	def isEmpty(self):
		return not self.getValue()

	def text(self) -> str:
		return self.inputEdit.text()

	def setDisabled(self, val: bool = True):
		self.inputEdit.setReadOnly(val)
		if hasattr(self, 'plusButton') and self.plusButton:
			self.plusButton.setDisabled(val)
		if hasattr(self, 'minusButton') and self.minusButton:
			self.minusButton.setDisabled(val)
