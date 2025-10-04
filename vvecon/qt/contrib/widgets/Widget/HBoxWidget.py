from typing import Optional, Type, Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from vvecon.qt.contrib.widgets import Margin

from .Widget import Widget

__all__ = ['HBoxWidget']


class HBoxWidget(Widget):
	def __init__(
		self,
		parent: Optional[Type[QWidget] | QWidget] = None,
		spacing: int = 0,
		margin: Optional[Margin] = None,
		alignment: Union[Qt.AlignmentFlag] = Qt.AlignmentFlag.AlignLeft,
		**kwargs
	):
		super().__init__(
			parent=parent, layout=QHBoxLayout, spacing=spacing, margin=margin, alignment=alignment, **kwargs
		)
