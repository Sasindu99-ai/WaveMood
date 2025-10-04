from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, TypeVar, Optional

import pytz # type: ignore
from icecream import ic
from vvecon.qt.exceptions import ParseError
from vvecon.qt.models.util import getAllAnnotations

__all__ = ['ModelAbstract']

T = TypeVar('T', bound='ModelAbstract')


class ModelAbstract(Generic[T]):
	"""
	ModelAbstract

	Description:
		This is a base class for all models. This class is used to create models for the application. This class
		provides the basic structure for all models. This class provides the basic structure for all models. This

	Methods:
		__init__(self, **kwargs)
		fromList(cls, data: List[T]) -> List[T]
		fromDict(cls, data: dict) -> T
		json(self) -> Dict
	"""

	@classmethod
	def _convertInt(cls, value: Any) -> int:
		return int(float(value))

	_dateFormat = '%Y-%m-%d %H:%M:%S'
	_dateFormats = [
		'%Y-%m-%d %H:%M:%S',
		'%Y-%m-%d %H:%M:%S.%f',
		'%Y-%m-%dT%H:%M:%S',
		'%Y-%m-%dT%H:%M:%S.%f',
		'%Y-%m-%d',
		'%Y-%m-%dT%H:%M:%S',
		'%Y-%m-%dT%H:%M:%S.%f%z',
		'%Y-%m-%dT%H:%M:%S%z'
	]
	_typeCasting = dict(str=str, int=int, float=float, bool=bool)

	def __init__(self, **kwargs):
		annotations = getAllAnnotations(self.__class__)
		for key, value in kwargs.items():
			if key in annotations:
				setattr(self, key, self._convert(value, annotations[key]))

	@classmethod
	def _convertDict(cls, value: Any, dateType: type) -> Dict:
		if not hasattr(dateType, '__args__'):
			return value
		return {
			key: cls._convert(item, dateType.__args__[1])
			for key, item in value.items()
		}

	@classmethod
	def _convertOptional(cls, value: Any, dateType: type) -> Any:
		if value is None:
			return None
		if not hasattr(dateType, '__args__'):
			return value
		return cls._convert(value, dateType.__args__[0])

	@classmethod
	def _convertList(cls, value: Any, dateType: type) -> Any:
		return [
			cls._convert(
				item, (list(dateType.__args__)[0] if hasattr(dateType, '__args__') else Any)
			) for item in value
		]

	@classmethod
	def _convertUnexpected(cls, value: Any, dateType: type) -> Any:
		try:
			return dateType.__call__(value)
		except TypeError:
			pass
		try:
			return dateType.__call__(*value)
		except TypeError:
			pass
		return dateType.__call__(**value)

	@classmethod
	def _convertDate(cls, value: Any) -> datetime:
		if isinstance(value, datetime):
			if value.tzinfo is None:
				utc_timezone = pytz.utc
				return utc_timezone.localize(value)
			return value
		if value.endswith('Z'):
			value = value[:-1]
		convertedDate: Optional[datetime] = None
		for dateFormat in cls._dateFormats:
			try:
				convertedDate = datetime.strptime(value, dateFormat)
			except ValueError:
				pass
		if convertedDate is None:
			convertedDate = datetime.strptime(value, cls._dateFormat)
		if convertedDate.tzinfo is not None:
			return convertedDate
		utc_timezone = pytz.utc
		parsed_date = utc_timezone.localize(convertedDate)
		return parsed_date


	@classmethod
	def _convert(cls, value: Any, dateType: type) -> Any:
		"""
        This function is used to convert the value to the given type
        :param value: Any
        :param dateType: type
        :return: Any
        """
		try:
			if dateType is datetime:
				return cls._convertDate(value)
			if str(dateType).startswith('typing.Optional'):
				return cls._convertOptional(value, dateType)
			if str(dateType).startswith('typing.List'):
				return cls._convertList(value, dateType)
			if str(dateType).startswith('typing.Dict'):
				return cls._convertDict(value, dateType)
			if str(dateType).startswith('typing.Any'):
				return value
			if dateType in cls._typeCasting.values():
				if dateType is int:
					return cls._convertInt(value)
				return cls._typeCasting[dateType.__name__](value)
			return cls._convertUnexpected(value, dateType)
		except TypeError as e:
			ic.enable()
			ic(e)
			ic(value, dateType)
			ic.disable()
			line = 0
			column = ''
			if e.__traceback__ is not None:
				line = e.__traceback__.tb_lineno if hasattr(e.__traceback__, 'tb_lineno') else 0
				column = e.__traceback__.tb_frame.f_code.co_filename
			raise ParseError('Type Error', line, column)

	@classmethod
	def fromList(cls, data: List) -> List:
		"""
        This function is used to convert the list of data to the model
        :param data: List
        :return: List
        """
		return [cls(**item) for item in data]

	@classmethod
	def fromDict(cls, data: dict):
		"""
        This function is used to convert the dictionary data to the model
        :param data:
        :return: Model
        """
		return cls(**data)

	def _json(self, data):
		"""
		This function is used to convert the model to dictionary
		:param data: Any
		:return: Any
		"""
		if isinstance(data, datetime):
			return data.strftime(self._dateFormat)
		if hasattr(data, 'json'):
			return data.json()
		if isinstance(data, list) and len(data) > 0 and hasattr(data[0], 'json'):
			return [item.json() for item in data]
		if isinstance(data, list) and len(data) > 0 and isinstance(data[0], datetime):
			return [item.strftime(self._dateFormat) for item in data]
		if isinstance(data, dict):
			return {
				self._json(k): self._json(v)
				for k, v in data.items()
			}
		if isinstance(data, Enum):
			return data.value
		return data

	def json(self) -> Dict:
		"""
		This function is used to convert the model to dictionary
		:return: Dict
		"""
		return self._json(self.__dict__)

	def __repr__(self):
		return """{}({})""".format(
			self.__class__.__name__,
			', '.join(
				[
					f'{key}={value}'
					for key, value in self.__dict__.items()
				]
			)
		)

	def __str__(self):
		return self.__repr__()
