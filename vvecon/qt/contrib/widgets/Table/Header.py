from dataclasses import dataclass
from typing import Optional

__all__ = ['Header']

from vvecon.qt.enums import SizeType


@dataclass
class Header:
	SINGLE_LINE = 0
	DOUBLE_LINE = 1

	name: str
	width: Optional[int] = NotImplemented
	stretch: Optional[int] = 1
	headerType: Optional[int] = 0

	@property
	def widthType(self):
		if self.width is not NotImplemented:
			return SizeType.FIXED
		if self.stretch is not NotImplemented:
			return SizeType.STRETCH
		return SizeType.PREFERRED
