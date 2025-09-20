from dataclasses import dataclass
from typing import Optional

from vvecon.qt.contrib.styles import InputField
from vvecon.qt.util import Style

__all__ = ['StyleScheme']


@dataclass
class StyleScheme:
	label: Optional[Style] = InputField.label
	container: Optional[Style] = InputField.container
	searchContainer: Optional[Style] = InputField.searchContainer
	lineEdit: Optional[Style] = InputField.lineEdit
	errorContainer: Optional[Style] = InputField.errorContainer
	successContainer: Optional[Style] = InputField.successContainer
	bottomLabel: Optional[Style] = InputField.bottomLabel
	errorBottomLabel: Optional[Style] = InputField.errorBottomLabel
	successBottomLabel: Optional[Style] = InputField.successBottomLabel
