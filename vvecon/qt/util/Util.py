import sys
import os


from vvecon.qt.logger import logger

__all__ = ['Util']


class Util:
	MK_DIR_NORMAL_MODE: int = 0o777
	MK_DIR_UAC_MODE: int = 0o700

	@classmethod
	def mkSecretDir(cls, path: str, mode: int = MK_DIR_NORMAL_MODE) -> bool:
		cls.mkDir(path, mode)
		if sys.platform == 'win32':
			from ctypes import windll
			return windll.kernel32.SetFileAttributesW(path, 0x02)
		return True

	@classmethod
	def mkDir(cls, path: str, mode: int = MK_DIR_NORMAL_MODE):
		try:
			path = path.replace('/', '\\') if '/' in path else path
			container = '\\'.join(path.split('\\')[:-1])
			if not os.path.exists(container):
				cls.mkDir(container, mode)
			os.mkdir(path, mode)
		except FileNotFoundError:
			logger.error(f'Unexpected error, Failed to create {path} folder')
			exit(-1)
		except FileExistsError:
			logger.warning(f'{path} folder already exists')

	@classmethod
	def either(cls, *args, default=None):
		for arg in args:
			if arg is not None:
				return arg
		return default
