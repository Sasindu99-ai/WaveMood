import os.path
from os import environ
from sys import platform

from cryptography.fernet import Fernet

from vvecon.qt.logger import logger

from .Util import Util

__all__ = ['Settings']

_ROOT = environ.get('BASE_PATH', None)
_APP = environ.get('APP_NAME', None)
_APP_PATH = f"{environ.get('LOCALAPPDATA')}\\{_APP}"
_SECRET_FOLDER = 'vvecon'
_SECRET_PATH = f'{_APP_PATH}/.{_SECRET_FOLDER}'

if not os.path.exists(_SECRET_PATH):
    if platform in ('win32', 'win64'):
        Util.mkSecretDir(_SECRET_PATH, Util.MK_DIR_UAC_MODE)
    # TODO: Handle Mac OS and Linux platforms


class Settings:
    _KEY = environ.get('SECRET_KEY', 'z9DODbJH3Q72whKWZ7VN7jsvm6_dE5KCdag8AwqeNdc=')
    _CIPHER = Fernet(_KEY.encode())

    @classmethod
    def set(cls, key: str, value: str):
        try:
            encrypted_value = cls._CIPHER.encrypt(value.encode())
            with open(f'{_SECRET_PATH}/{key}.txt', 'wb') as file:
                file.write(encrypted_value)
        except FileNotFoundError:
            logger.error('Unable locate settings containing file, try rerunning the application.')
            exit(-1)

    @classmethod
    def remove(cls, key: str):
        try:
            os.remove(f'{_SECRET_PATH}/{key}.txt')
        except FileNotFoundError:
            logger.error('Unable locate settings containing file, try rerunning the application.')

    @classmethod
    def get(cls, key: str, default: str | None = None):
        try:
            with open(f'{_SECRET_PATH}/{key}.txt', 'rb') as file:
                encrypted_value = file.read()
            decrypted_value = cls._CIPHER.decrypt(encrypted_value).decode()
            return decrypted_value
        except FileNotFoundError:
            logger.warning(f"Unable find the file containing the key {key}, Make sure you have set 'BASE_PATH' and "
                           f"'APP_NAME' environment variables.")
            return default
