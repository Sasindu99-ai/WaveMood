from typing import Any, Callable, Optional

from vvecon.qt.contrib.widgets.Input import InputField
from Enums import InputType

from .BaseCell import BaseCell

__all__ = ['InputCell']


class InputCell(BaseCell):
	inputField: InputField
	_name: str = ''
	_inputType: InputType = InputType.TEXT
	_width: Optional[int] = None
	_height: int = 40
	_hint: Optional[str] = None
	_placeholder: str = ''
	_isLight: bool = True
	_icon: Optional[str] = None
	_step: float = 0.0
	_maxValue: Optional[float] = None
	_minValue: Optional[float] = None
	_showTooltipIcon: bool = False
	_validator: Optional[Callable] = None
	_onTextChanged: Optional[Callable] = None
	_setDisabled: bool = False
	_default: Optional[float] = None

	def __init__(self,*args, **kwargs):
		self._name = kwargs.get('name', self._name)
		self._inputType = kwargs.get('inputType', self._inputType)
		self._width = kwargs.get('width', self._width)
		self._height = kwargs.get('height', self._height)
		self._hint = kwargs.get('hint', self._hint)
		self._placeholder = kwargs.get('placeholder', self._placeholder)
		self._isLight = kwargs.get('isLight', self._isLight)
		self._icon = kwargs.get('icon', self._icon)
		self._step = kwargs.get('step', self._step)
		self._maxValue = kwargs.get('maxValue', self._maxValue)
		self._minValue = kwargs.get('minValue', self._minValue)
		self._showTooltipIcon = kwargs.get('showTooltipIcon', self._showTooltipIcon)
		self._validator = kwargs.get('validator', self._validator)
		self._onTextChanged = kwargs.get('onTextChanged', self._onTextChanged)
		self._setDisabled = kwargs.get('setDisabled', self._setDisabled)
		self._default = kwargs.get('default', self._default)

		super(InputCell, self).__init__(*args, **kwargs)

		if self._setDisabled:
			self.disable(True)

	def setupCell(self):
		self.inputField = InputField(
			parent=self,
			name=self._name,
			inType=self._inputType,
			width=self._width,
			height=self._height,
			hint=self._hint,
			placeholder=self._placeholder,
			isLight=self._isLight,
			icon=self._icon,
			step=self._step,
			maxVal=self._maxValue,
			minVal=self._minValue,
			showTooltipIcon=self._showTooltipIcon,
			validator=self._validator,
			default=self._default
		)
		self.inputField.inputEdit.textChanged.connect(self.onTextChanged)

		self.layout.addWidget(self.inputField)

	def setValues(self, data: Any | dict):
		self.inputField.inputEdit.blockSignals(True)

		if isinstance(data, dict):
			val = data['val']
			disabled = data['disabled']
			self.inputField.setValue(val)
			self.inputField.setDisabled(disabled)
		else:
			self.inputField.setValue(data)
		self.inputField.inputEdit.blockSignals(False)

	def getValue(self):
		return self.inputField.getValue()

	def onTextChanged(self, value: str):
		if self._onTextChanged is not None:
			self._onTextChanged(value, self, self._parent)

	def disable(self, value: bool):
		self.inputField.setDisabled(value)
