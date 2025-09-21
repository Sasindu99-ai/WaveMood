import json
import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar, Generic, Optional

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFontDatabase, QFont, QIcon
from PyQt6.QtWidgets import QLabel

__all__ = ['Icons', 'iconSet', 'SystemIcon']

iconSet = json.load(open(Path(__file__).parent / 'Icons' / 'icons.json', 'r', encoding='utf-8'))

_root = Path(__file__).parent / 'Icons'
_base = 'static/MaterialSymbols'

NORMAL = 0
FILLED = 1

_modes = [NORMAL, FILLED]

SHARP = 0
ROUNDED = 1
OUTLINED = 2

_styles = [SHARP, ROUNDED, OUTLINED]

_pts = [0, 28, 36, 48]

ExtraLight = 0
Light = 1
Thin = 2
Regular = 3
Medium = 4
SemiBold = 5
Bold = 6

_weights = [ExtraLight, Light, Thin, Regular, Medium, SemiBold, Bold]

_modesValues = ['', '_Filled']
_stylesValues = ['Sharp', 'Rounded', 'Outlined']
_ptsValues = {0: '', 28: '_28pt', 36: '_36pt', 48: '_48pt'}
_weightsValues = ['ExtraLight', 'Light', 'Thin', 'Regular', 'Medium', 'SemiBold', 'Bold']

_displayModes = ['', 'Filled']
_displayStyles = ['Sharp', 'Rounded', 'Outlined']
_displayPts = ['', 'pt28', 'pt36', 'pt48']
_displayWeights = ['ExtraLight', 'Light', 'Thin', 'Regular', 'Medium', 'SemiBold', 'Bold']


IconType = TypeVar('IconType', bound='Icon')
SystemIconType = TypeVar('SystemIconType', bound='SystemIcon')


def _generateFilePath(mode: int = NORMAL, style: int = SHARP, pt: int = 0, weight: int = Regular):
	if mode not in _modes:
		raise ValueError(f'mode must be one of {_modesValues}')
	if style not in _styles:
		raise ValueError(f'style must be one of {_stylesValues}')
	if pt not in _pts:
		raise ValueError(f'pt must be one of {_ptsValues}')
	if weight not in _weights:
		raise ValueError(f'weight must be one of {_weightsValues}')
	return (
		f'{_root}/{_stylesValues[style]}/{_base}{_stylesValues[style]}{_modesValues[mode]}'
		f'{_ptsValues[pt]}-{_weightsValues[weight]}.ttf'
	)

class SystemIcon(QIcon, Generic[SystemIconType]):
	_icon: IconType

	# def __init__(self):
	# 	super().__init__()
	# 	self._iconFamilies = None

	def setIcon(self, icon: IconType):
		self._icon = icon

	def update(self, size: Optional[int] = None, color: Optional[str] = None, background: Optional[str] = None):
		icon = deepcopy(self._icon)
		if size:
			icon.size = size
		if color:
			icon.color = color
		if background:
			icon.backGround = background
		newIcon = icon.generateIcon()
		newIcon.setIcon(icon)
		return newIcon

	def setSize(self, size: int) -> SystemIconType:
		return self.update(size=size)

	def setColor(self, color: str) -> SystemIconType:
		return self.update(color=color)

	def setBackgroundColor(self, background: str) -> SystemIconType:
		return self.update(background=background)

	def toStr(self):
		return self._icon.toStr()

	def toPixmap(self, mode: QIcon.Mode = QIcon.Mode.Normal, state: QIcon.State = QIcon.State.Off):
		return self.pixmap(QSize(self._icon.size, self._icon.size), mode=mode, state=state)

	def getFont(self) -> QFont:
		font = QFont(self._icon.iconFamilies[self._icon.style][self._icon.mode][self._icon.pt][self._icon.weight])
		font.setPixelSize(self._icon.size)
		return font

	def toText(self) -> str:
		return iconSet[self._icon.icon]


@dataclass
class Icon(Generic[IconType]):
	mode: int = NotImplemented
	style: Optional[int] = None
	pt: Optional[int] = None
	weight: Optional[int] = None
	icon: Optional[str] = None
	size: int = 24
	backGround: str = 'transparent'
	color: str = 'black'

	iconFamilies = {}
	for style in _styles:
		iconFamilies[style] = {}
		for mode in _modes:
			iconFamilies[style][mode] = {}
			for pt in _pts:
				iconFamilies[style][mode][pt] = {}
				for weight in _weights:
					filePath = _generateFilePath(mode, style, pt, weight)
					if os.path.exists(filePath):
						fontId = QFontDatabase.addApplicationFont(filePath)
						family = QFontDatabase.applicationFontFamilies(fontId)[0]
						iconFamilies[style][mode][pt][weight] = family

	def generateIcon(self):
		if self.mode not in _modes or self.style not in _styles or self.pt not in _pts or self.weight not in _weights:
			raise ValueError('Invalid attribute')
		if self.icon not in iconSet:
			raise ValueError('Invalid icon')
		font = QFont(self.iconFamilies[self.style][self.mode][self.pt][self.weight])
		font.setPixelSize(self.size)

		label = QLabel()
		label.setFont(font)
		label.setText(iconSet[self.icon])
		label.setStyleSheet(f'background-color: {self.backGround}; color: {self.color};')
		icon = SystemIcon(label.grab())
		icon.setIcon(self)
		return icon

	def toStr(self):
		return f'{_displayModes[self.mode]}{f" {_displayStyles[self.style]}" if self.style is not None else ""}' \
			f'{f" {_displayPts[self.pt]}" if self.pt is not None else ""}' \
			f'{f" {_displayWeights[self.weight]}" if self.weight is not None else ""}' \
			f' {self.icon}'


class Nested:
	icon: Icon

	def __init__(self, icon: Icon):
		self.icon = icon

	def __getattr__(self, name):
		icon = self.icon

		if self.icon.style is None:
			if name in _displayStyles:
				icon.style = _displayStyles.index(name)
				return Nested(icon)
			icon.style = 0
			return getattr(Nested(icon), name)

		if self.icon.pt is None:
			if name in _displayPts:
				icon.pt = _ptsValues[_displayPts.index(name)]
				return Nested(icon)
			icon.pt = 0
			return getattr(Nested(icon), name)

		if self.icon.weight is None:
			if name in _displayWeights:
				icon.weight = _displayWeights.index(name)
				return Nested(icon)
			icon.weight = 3
			return getattr(Nested(icon), name)

		if self.icon.icon is None:
			if name in iconSet:
				icon.icon = name
				return icon.generateIcon()
			raise AttributeError(f'Icon {name} not found')


class icons:
	def __getattr__(self, name):
		if name == _displayModes[1]:
			return Nested(Icon(
				mode=1,
				style=None,
				pt=None,
				weight=None,
				icon=None
			))
		if name == _displayModes[0]:
			return Nested(Icon(
				mode=0,
				style=None,
				pt=None,
				weight=None,
				icon=None
			))

		return getattr(Nested(Icon(
			mode=0,
			style=None,
			pt=None,
			weight=None,
			icon=None
		)), name)


Icons = icons()
