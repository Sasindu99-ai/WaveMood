from typing import Dict, TypeVar, Generic
from .Style import Style

__all__ = ['StyleSheet']

T = TypeVar('T', bound='StyleSheet')


class StyleSheet(Generic[T]):
	def __init__(self, **kwargs: Dict[str, Style]):
		for key, value in kwargs.items():
			if not isinstance(value, Style):
				raise TypeError(f"Invalid type, expected 'Style', got {type(value).__name__}")
			setattr(self, key, value)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if not hasattr(self, key):
				raise KeyError(f'{key} attribute not found')
			if not isinstance(value, Style):
				raise TypeError(f"Invalid type, expected 'Style', got {type(value).__name__}")
			setattr(self, key, value)
		return self
