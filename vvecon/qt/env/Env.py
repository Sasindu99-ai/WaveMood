import os

from ..enums import EnvMode

__all__ = ['Env']


class Env:
	_dotenv: str = None

	def __init__(self, mode: EnvMode, dotenv=f'{os.getcwd()}/.env', **kwargs):
		self.mode = mode
		self.debug = mode == EnvMode.DEBUG
		self._dotenv = dotenv

		self.__dict__.update(kwargs)

	def set(self, key: str, value):
		setattr(self, key, value)
		os.environ.setdefault(key, value)

	def get(self, key: str):
		return getattr(self, key)

	def init(self):
		for key, value in self.__dict__.items():
			if isinstance(value, str):
				os.environ.setdefault(key, value)
			elif isinstance(value, bool):
				os.environ.setdefault(key, str(value).lower())
			else:
				os.environ.setdefault(key, str(value))
		if self._dotenv and os.path.exists(self._dotenv):
			from dotenv import load_dotenv
			load_dotenv(self._dotenv)
