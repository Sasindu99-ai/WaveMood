from enum import Enum
from typing import Dict

from .ColorTheme import ColorTheme
from .Images import Images
from .LocaleBuilder import LocaleBuilder

__all__ = ['Theme']

from ..logger import logger


class Theme:
    """
    Represents the application theme, including color and image themes.
    This class manages the color palette and image resources based on the selected themes.
    It allows setting the color theme and image theme, and provides access to the corresponding
    color palette and images.

    Attributes:
        colorTheme (Enum): The current color theme.
        imageTheme (Enum): The current image theme.
        colorPalette (Dict[Enum, ColorTheme]): A dictionary mapping color themes to their respective ColorTheme objects.
        images (Images): An instance of the Images class for managing image resources.
        locale (LocaleBuilder): An instance of LocaleBuilder for managing localization.

    Methods:
        __setattr__(self, key, value): Custom setter to handle image theme changes.
        colors (ColorTheme): Returns the ColorTheme corresponding to the current color theme.

    Raises:
        TypeError: If the image theme is not an instance of Enum.
        ValueError: If the color theme is not recognized.
    """
    colorTheme: Enum
    imageTheme: Enum

    colorPalette: Dict[Enum, ColorTheme]
    images: Images
    colors: ColorTheme
    locale: LocaleBuilder

    def __setattr__(self, key, value) -> None:
        """
        Custom setter to handle image theme changes.
        :param key: str - The name of the attribute to set.
        :param value: Any - The value to set for the attribute.
        :raises TypeError: If the image theme is not an instance of Enum.
        :raises ValueError: If the color theme is not recognized.
        :return: None
        """
        print(f'Setting {key} to {value}')
        if key == 'imageTheme':
            if not isinstance(value, Enum):
                raise TypeError(f'Image theme must be an instance of Enum, got {type(value)}')
            self.images.setTheme(value)
        if key == 'colorTheme':
            if not isinstance(value, Enum):
                raise ValueError(f'Color theme must be an instance of Enum, got {type(value)}')
            if colorTheme := self.colorPalette.get(value):
                setattr(self, 'colors', colorTheme)
        super(Theme, self).__setattr__(key, value)

    @classmethod
    def setColorTheme(cls, theme: Enum):
        """
        Set the color theme of the application.
        :param theme: Enum - The new color theme to set.
        """
        if theme not in cls.colorPalette:
            raise ValueError(f'Color theme {theme} is not recognized.')
        cls.colorTheme = theme
        cls.colors = cls.colorPalette[theme]
        logger.info(f'Setting color theme to {theme}')
