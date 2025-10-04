from typing import Any, Dict, Generic, List, Optional, TypeVar

from PyQt6.QtWidgets import QHBoxLayout, QWidget

from vvecon.qt.contrib.widgets import Margin

from .CellStyleScheme import CellStyleScheme

__all__ = ['BaseCell']

T = TypeVar('T', bound='BaseCell')


class BaseCell(QWidget, Generic[T]):
	_initialArgs: List = []
	_initialKwargs: Dict = dict()
	_parent: Optional[Any] = None
	_styleScheme: CellStyleScheme = CellStyleScheme()

	def __init__(self, *args, **kwargs):
		super(BaseCell, self).__init__()

		self.saveInitialValues(*args, **kwargs)

		self.layout = QHBoxLayout(self)
		self.layout.setContentsMargins(Margin(0))
		self.layout.setSpacing(0)
		self.setLayout(self.layout)

		self.setupCell()

	def saveInitialValues(self, *args, **kwargs):
		self._initialArgs = list(args)
		self._initialKwargs = kwargs

	def setupCell(self):
		"""
		This function is to modify the cell widget
		:return: None
		"""
		pass

	def setParent(self, parent):
		self._parent = parent

	def setValues(self, data: Any):
		"""
		This function is to update the widget when data changes
		:param data: Any
		:return: None
		"""
		pass

	@classmethod
	def setStyleScheme(cls, styleScheme: CellStyleScheme):
		cls._styleScheme = styleScheme

	def args(self):
		return self._initialArgs

	def kwargs(self):
		return self._initialKwargs
