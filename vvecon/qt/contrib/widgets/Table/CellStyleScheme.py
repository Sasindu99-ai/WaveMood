from vvecon.qt.contrib.styles import Label
from vvecon.qt.util import Style

__all__ = ['CellStyleScheme']


class CellStyleScheme:
	label: Style = Label.label.update(fontSize=13, color='white')
