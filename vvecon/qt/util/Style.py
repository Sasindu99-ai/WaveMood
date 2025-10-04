from typing import Tuple, Dict, Any

__all__ = ['Style']


class Style:
	_styleSheet: str
	_args: Tuple = tuple()
	_kwargs: Dict = dict()

	def __init__(self, styleSheet: str, *args, **kwargs):
		self._styleSheet = styleSheet
		self._args = args
		self._kwargs = kwargs

	def update(self, *args, **kwargs) -> 'Style':
		deepCopy = self.__class__(self._styleSheet, *self._args, **self._kwargs)
		deepCopy._args = args if args else self._args
		deepCopy._kwargs = {**self._kwargs, **kwargs}
		return deepCopy

	def apply(self, widget: Any, *args, **kwargs) -> None:
		"""
		Apply the style to the widget
		:param widget: Any Widget of PyQt
		:param args: Arguments to be passed to the style
		:param kwargs: Keyword arguments to be passed to the style
		:return: None
		"""
		if not hasattr(widget, 'setStyleSheet'):
			raise AttributeError(f'Widget {widget} does not have a setStyleSheet method')
		style = self._styleSheet.format(*args, *self._args, **kwargs, **self._kwargs)
		style = style.replace('[', '{').replace(']', '}')
		widget.setStyleSheet(style)

	@property
	def qss(self) -> str:
		"""
		Property to get the style sheet
		:return: str
		"""
		style = self._styleSheet.format(*self._args, **self._kwargs)
		style = style.replace('[', '{').replace(']', '}')
		return style
