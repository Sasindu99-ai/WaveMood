from enum import Enum

__all__ = ['SizeType']


class SizeType(Enum):
	FIXED = 0
	STRETCH = 1
	PREFERRED = 2
