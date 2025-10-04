import json
import os
from enum import Enum
from typing import Dict

__all__ = ['LocaleBuilder']


class LocaleBuilder:
    """
    LocaleBuilder class to manage locale JSON files.
    This class allows setting and retrieving locale-specific strings from JSON files
    based on the current locale and a default locale. It raises errors if the JSON files
    are not found or if the locale is not an instance of Enum.

    Attributes:
        _base (str): Base directory for locale JSON files.
        _locale (Enum): Current locale.
        _default (Enum): Default locale.
        _json (Dict): Dictionary to store the current locale's strings.
        _defaultJson (Dict): Dictionary to store the default locale's strings.

    Methods:
        __init__(self, base: str = _base, locale: Enum = NotImplemented, default: Enum = NotImplemented) -> None:
            Initializes the LocaleBuilder with a base directory, current locale, and default locale.
        setBase(self, base: str) -> None:
            Sets the base directory for locale JSON files.
        getBase(self) -> str:
            Returns the base directory for locale JSON files.
        setLocale(self, locale: Enum) -> None:
            Sets the current locale and loads its JSON file.
        getLocale(self) -> Enum:
            Returns the current locale.
        setDefaultLocale(self, default: Enum) -> None:
            Sets the default locale and loads its JSON file.
        getDefaultLocale(self) -> Enum:
            Returns the default locale.
        get(self, key: str) -> str:
            Retrieves a string from the current or default locale based on the key.
        __getattribute__(self, item):
            Retrieves the value of an attribute or a string from the current or default locale.

    Raises:
        TypeError: If the locale or default is not an instance of Enum.
        FileNotFoundError: If the JSON file for the locale or default locale does not exist.
        AttributeError: If the requested attribute is not defined in the locale JSON files.

    Usage:
    >>> from enum import Enum
    >>> class Locale(Enum):
    ...     enUS = 'English (US)'
    ...     siLK = 'Sinhala (LK)'
    >>> localeBuilder = LocaleBuilder(locale=Locale.siLK, default=Locale.enUS)
    >>> print(localeBuilder.hello_world)  # Example usage, assuming 'hello_world' is defined in the locale JSON files
    """
    _base: str = 'res/locale'
    _locale: Enum = NotImplemented
    _default: Enum = NotImplemented
    _json: Dict = dict()
    _defaultJson: Dict = dict()
    _attributes = (
        '_base', '_locale', '_json', '_default', '_defaultJson', 'setLocale', 'getLocale', 'setDefaultLocale',
        'getDefaultLocale', 'get', 'setBase', 'getBase'
    )

    def __init__(self, base: str = _base, locale: Enum = NotImplemented, default: Enum = NotImplemented) -> None:
        """
        Initializes the LocaleBuilder with a base directory, current locale, and default locale.
        :param base: str - Base directory for locale JSON files.
        :param locale: Enum - Current locale.
        :param default: Enum - Default locale.
        :raises TypeError: If locale or default is not an instance of Enum.
        :raises FileNotFoundError: If the JSON file for the locale or default locale does not exist.
        :return: None
        """
        if not isinstance(locale, Enum):
            raise TypeError(f'Locale must be an instance of Enum, got {type(locale)}')
        self._locale = locale
        if not isinstance(default, Enum):
            raise TypeError(f'Default must be an instance of Enum, got {type(default)}')
        self._default = default
        self.setBase(base)

    def setBase(self, base: str) -> None:
        """
        Sets the base directory for locale JSON files.
        :param base: str - Base directory for locale JSON files.
        :raises FileNotFoundError: If the base directory does not exist.
        :return: None
        """
        if not os.path.exists(base):
            raise FileNotFoundError(f'Base directory {base} does not exist')
        self._base = base
        self.setLocale(self._locale)
        self.setDefaultLocale(self._default)

    def getBase(self) -> str:
        """
        Returns the base directory for locale JSON files.
        :return: str - Base directory for locale JSON files.
        """
        return self._base

    def setLocale(self, locale: Enum) -> None:
        """
        Sets the current locale and loads its JSON file.
        :param locale: Enum - Current locale.
        :raises TypeError: If locale is not an instance of Enum.
        :raises FileNotFoundError: If the JSON file for the locale does not exist.
        :return: None
        """
        self._locale = locale
        localePath = f'{self._base}/{self._locale.name}.json'

        if not os.path.exists(localePath):
            raise FileNotFoundError(f'{localePath} not found')

        with open(localePath, 'r') as file:
            self._json = json.load(file)

    def getLocale(self) -> Enum:
        """
        Returns the current locale.
        :return: Enum - Current locale.
        """
        return self._locale

    def setDefaultLocale(self, default: Enum) -> None:
        """
        Sets the default locale and loads its JSON file.
        :param default: Enum - Default locale.
        :raises TypeError: If default is not an instance of Enum.
        :raises FileNotFoundError: If the JSON file for the default locale does not exist.
        :return: None
        """
        self._default = default
        defaultPath = f'{self._base}/{self._default.name}.json'

        if not os.path.exists(defaultPath):
            raise FileNotFoundError(f'{defaultPath} not found')

        with open(defaultPath, 'r') as file:
            self._defaultJson = json.load(file)

    def getDefaultLocale(self) -> Enum:
        """
        Returns the default locale.
        :return: Enum - Default locale.
        """
        return self._default

    def get(self, key: str) -> str:
        """
        Retrieves a string from the current or default locale based on the key.
        :param key: str - Key to retrieve the string.
        :raises AttributeError: If the key is not defined in the current or default locale.
        :return: str - String from the current or default locale.
        """
        return getattr(self, key)

    def __getattribute__(self, item):
        """
        Retrieves the value of an attribute or a string from the current or default locale.
        :param item: str - Name of the attribute or key to retrieve.
        :raises AttributeError: If the requested attribute is not defined in the locale JSON files.
        :return: str - Value of the attribute or string from the current or default locale.
        """
        if item == '_attributes':
            return super(LocaleBuilder, self).__getattribute__(item)
        if item in self._attributes:
            return super(LocaleBuilder, self).__getattribute__(item)
        if item in self._json:
            return self._json[item]
        if item in self._defaultJson:
            return self._defaultJson[item]
        raise AttributeError(f'{item} is not defined in the locale')
