from typing import Optional, Type

from PyQt6.QtWidgets import QWidget

from .Window import Window
from ..logger import logger

__all__ = ['View', 'WindowType']

WindowType = Window


class View(QWidget):
    """
    View(QWidget)

    Description:
        This is a base class for all views. This class is used to create views for the application. This class provides
        the basic structure for all views.

    Attributes:
        parent: Optional[WindowType]
        __viewName: str = ''
        _isBusy: bool = False

    Methods:
        setViewName(self, name: str) -> None
        getViewName(self) -> str
        onCreate(self) -> None
        onResume(self) -> None
        setStatus(self, isBusy: bool) -> None
        onClose(self) -> bool
    """
    parent: Optional[WindowType]
    __viewName: str = ''
    _isBusy: bool = False

    def __init__(self,
                 parent: Optional[WindowType],
                 name: Optional[str] = None):
        self.parent = parent

        super(View, self).__init__()
        super(View, self).setParent(self.parent)

        if name:
            self.setObjectName(name)

    def setViewName(self, name: str) -> None:
        """
        setTabName(self, name: str) -> None
        :param name: str
        :return: None
        """
        self.__viewName = name

    def getViewName(self) -> str:
        """
        getTabName(self)
        :return: str
        """
        return self.__viewName

    def onCreate(self) -> None:
        """
        onCreate(self)
        This method is called when the view is created.
        :return: None
        """
        pass

    def onResume(self) -> None:
        """
        onResume(self)
        This method is called when the view is resumed.
        :return: None
        """
        pass

    def setStatus(self, isBusy: bool) -> None:
        """
        setStatus(self, isBusy: bool) -> None
        This method is used to set the status of the view.
        :param isBusy: bool
        :return: None
        """
        self._isBusy = isBusy

    def onDestroy(self) -> bool:
        """
        onClose(self) -> bool
        This method is called when the view is closed.
        :return: bool
        """
        return not self._isBusy

    def navigate(self, view: Optional[Type['View']], *args, **kwargs) -> None:
        """
        navigate(self, view: Optional['View'], *args, **kwargs) -> None
        This method is used to navigate to a different view.
        :param view: Optional[WindowType] - The view to navigate to.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: None
        """
        if not issubclass(view, View):
            logger.error(f'View {view} is not an instance of View')
            raise TypeError(f'View {view} is not an instance of View')
        if not self.parent:
            logger.error(f'Parent is not set for the view {self.__viewName}')
            raise ValueError(f'Parent is not set for the view {self.__viewName}')
        self.parent.navigate(view, *args, **kwargs)
