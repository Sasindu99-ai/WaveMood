import os
from enum import Enum
from typing import Dict

__all__ = ['Images']


class Images:
    """
    Images class to manage image paths based on themes and defaults.
    This class allows setting and retrieving image paths based on the current theme
    and a default theme. It raises errors if images are not found in the specified themes.

    Attributes:
        _base (str): Base directory for images.
        _theme (Enum): Current theme for images.
        _default (Enum): Default theme for images.
        _backup (Dict[str, str]): Backup dictionary to store image names and their paths.

    Methods:
        __setattr__(self, key, value): Sets an image path or theme.
        __init__(self, base: str, theme: Enum, default: Enum, **kwargs): Initializes the Images class.
        __getattribute__(self, item): Retrieves the image path for the given item.
        setBase(self, base: str): Sets the base directory for images.
        getBase(self) -> str: Gets the base directory for images.
        setTheme(self, theme: Enum): Sets the current theme for images.
        getTheme(self) -> Enum: Gets the current theme for images.
        setDefaultTheme(self, default: Enum): Sets the default theme for images.
        getDefaultTheme(self) -> Enum: Gets the default theme for images.
        getImage(self, name: str) -> str: Gets the image path for the given name.

    Raises:
        ValueError: If an invalid image name is provided.
        TypeError: If theme or default is not an instance of Enum.
        AttributeError: If the requested image is not defined.
        FileNotFoundError: If the image file does not exist in the specified themes.

    Usage:
    >>> from enum import Enum
    >>> class Theme(Enum):
    ...     LIGHT = 'light'
    ...     DARK = 'dark'
    >>> images = Images(theme=Theme.DARK, default=Theme.LIGHT, helody='helody.png')
    >>> print(images.helody)  # Should print the path to the helody.png image in the light theme
    >>> print(images.some_non_existent_image)  # Raises FileNotFoundError
    """
    _base ='res/images/'
    _theme: Enum = NotImplemented
    _default: Enum = NotImplemented
    _backup: Dict[str, str] = dict()
    _attributes = (
        '_base', '_theme', '_default', '_backup', 'setBase', 'getBase', 'setTheme', 'getTheme', 'setDefaultTheme',
        'getDefaultTheme', 'getImage'
    )

    def __setattr__(self, key, value) -> None:
        """
        Sets an image path or theme.
        :param key: str - The name of the image or theme.
        :param value: str - The path to the image or theme.
        :raises ValueError: If the key is not a valid image name.
        :raises TypeError: If theme or default is not an instance of Enum.
        :return: None
        """
        if not isinstance(key, str) or not key.isidentifier():
            raise ValueError(f'Invalid image name: {key}')
        self._backup[key] = str(value)
        if key in self._attributes:
            super(Images, self).__setattr__(key, value)

    def __init__(
            self, base: str = _base, theme: Enum = NotImplemented, default: Enum = NotImplemented, **kwargs
    ) -> None:
        """
        Initializes the Images class with a base directory, theme, and default theme.
        :param base: str - Base directory for images (default is 'res/images/').
        :param theme: Enum - Current theme for images (must be an instance of Enum).
        :param default: Enum - Default theme for images (must be an instance of Enum).
        :param kwargs: Additional keyword arguments for image paths.
        :raises TypeError: If theme or default is not an instance of Enum.
        :return: None
        """
        self._base = base
        if not isinstance(theme, Enum):
            raise TypeError(f'Theme must be an instance of Enum, got {type(theme)}')
        self._theme = theme
        if not isinstance(default, Enum):
            raise TypeError(f'Default must be an instance of Enum, got {type(default)}')
        self._default = default

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattribute__(self, item):
        """
        Retrieves the image path for the given item.
        :param item: str - The name of the image.
        :raises AttributeError: If the requested image is not defined.
        :raises FileNotFoundError: If the image file does not exist in the specified themes.
        :return: str - The path to the image.
        """
        if item == '_attributes':
            return super(Images, self).__getattribute__(item)
        if item in self._attributes:
            return super(Images, self).__getattribute__(item)
        if item not in self._backup:
            raise AttributeError(f'{item} is not defined in the images')
        return self.getImage(item)

    def setBase(self, base: str) -> None:
        """
        Sets the base directory for images.
        :param base: str - The new base directory for images.
        :return: None
        """
        self._base = base

    def getBase(self) -> str:
        """
        Gets the base directory for images.
        :return: str - The current base directory for images.
        """
        return self._base

    def setTheme(self, theme: Enum) -> None:
        """
        Sets the current theme for images.
        :param theme: Enum - The new theme for images.
        :raises TypeError: If theme is not an instance of Enum.
        :return: None
        """
        if not isinstance(theme, Enum):
            raise TypeError(f'Theme must be an instance of Enum, got {type(theme)}')
        self._theme = theme

    def getTheme(self) -> Enum:
        """
        Gets the current theme for images.
        :return: Enum - The current theme for images.
        """
        return self._theme

    def setDefaultTheme(self, default: Enum) -> None:
        """
        Sets the default theme for images.
        :param default: Enum - The new default theme for images.
        :raises TypeError: If default is not an instance of Enum.
        :return: None
        """
        if not isinstance(default, Enum):
            raise TypeError(f'Default must be an instance of Enum, got {type(default)}')
        self._default = default

    def getDefaultTheme(self) -> Enum:
        """
        Gets the default theme for images.
        :return: Enum - The current default theme for images.
        """
        return self._default

    def getImage(self, name: str) -> str:
        """
        Gets the image path for the given name.
        :param name: str - The name of the image.
        :raises AttributeError: If the requested image is not defined.
        :raises FileNotFoundError: If the image file does not exist in the specified themes.
        :return: str - The path to the image.
        """
        if os.path.exists(os.path.join(self._base, self._theme.value.lower(), self._backup[name])):
            return os.path.join(self._base, self._theme.value, self._backup[name])
        if os.path.exists(os.path.join(self._base, self._default.value.lower(), self._backup[name])):
            return os.path.join(self._base, self._default.value, self._backup[name])
        raise FileNotFoundError(f'Image {name} not found in theme {self._theme.value} or default {self._default.value}')
