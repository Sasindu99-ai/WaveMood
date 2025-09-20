from PyQt6.QtGui import QColor

__all__ = ['ColorTheme']


class ColorTheme:
    """
    ColorTheme

    Description:
        This class is used to create a color theme for the application. This class provides the basic structure
        for the color theme. You can initialize color theme like this:
        ColorTheme(
            background="#FFFFFF",
            foreground="#000000",
            primary="#FF5733",
            secondary="#33FF57",
            accent="#3357FF"
        )

    Attributes:

    Method:
        addColor(self, name: str, color: str) -> None
        getColor(self, name: str) -> QColor
    """

    def __setattr__(self, key, value):
        if not key.isidentifier():
            raise ValueError(f'Invalid attribute name: {key}')
        if not isinstance(value, str) or not QColor(value).isValid():
            raise ValueError(f'Invalid color value for {key}')
        super().__setattr__(key, QColor(value))

    def __getattr__(self, item):
        return super().__getattribute__(item)

    def __init__(self, **kwargs):
        """
        Initialize the ColorTheme with the given colors.
        :param kwargs: dict
        """
        super(ColorTheme, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def addColor(self, name: str, color: str) -> None:
        """
        addColor(self, name: str, color: str) -> None
        :param name: str
        :param color: str
        :return: None
        """
        setattr(self, name, color)

    def getColor(self, name: str) -> QColor:
        """
        getColor(self, name: str) -> QColor
        :param name: str
        :return: QColor
        """
        if not name.isidentifier():
            raise ValueError('Invalid name')
        if not hasattr(self, name):
            raise AttributeError('Color is not defined in the theme')
        return getattr(self, name)
