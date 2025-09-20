from typing import Dict, List, Type

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QSizePolicy,
    QStackedWidget,
    QWidget,
)

from ..contrib.widgets import Margin
from ..logger import logger
from ..signals import window
from ..util import ui

__all__ = ['Window']


class Window(QMainWindow):
    _PAGES: Dict[QWidget, Type[QWidget]] = dict()
    mainWidget: QWidget
    mainLayout: QGridLayout
    centralWidget: QStackedWidget
    navigationHistory: List[type] = list()

    def __init__(self, **__kwargs):
        """
        Window(parent: Optional[QWidget] = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags(),
		row: int = 1, column: int = 1, rowSpan: int = 1, columnSpan: int = 1,
		alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment())

		Description:
		    This is a base class for all windows. This class is used to create windows for the application. This class
            provides the basic structure for all windows. This class provides the basic structure for all windows. This
            class provides the basic structure for all windows. This class provides the basic structure for all
            windows.

        Attributes:
            _PAGES: Dict[QWidget] = dict()
            mainWidget: QWidget
            mainLayout: QGridLayout
            centralWidget: QStackedWidget
            navigationHistory: List[type] = list()

        Methods:
            navigate(self, view, *args, **kwargs) -> None
            navigateBack(self) -> None
            getViews(self) -> Dict[QWidget]
            removeView(self, view) -> None
            onTabChanged(self, tab: str) -> None
            removeCurrentView(self) -> None
		"""
        super(QMainWindow,self).__init__(__kwargs.get('parent'))

        ui.setLogicalDpi(self.screen().logicalDotsPerInch())

        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout(self.mainWidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(Margin(0))
        self.mainWidget.setLayout(self.mainLayout)
        self.mainWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.centralWidget = QStackedWidget()
        row = __kwargs.get('row') or 1
        column = __kwargs.get('column') or 1
        row_span = __kwargs.get('rowSpan') or 1
        column_span = __kwargs.get('columnSpan') or 1
        alignment = __kwargs.get('alignment', Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.centralWidget, row, column, row_span, column_span, alignment)

        self.setCentralWidget(self.mainWidget)

    def navigate(self, view, *args, **kwargs) -> None:
        """
        navigate method for navigating to a view
        :param view: View to navigate to
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: None
        """
        resume = False
        if view is None:
            return
        if view in self._PAGES.keys():
            resume = True
        if view not in self._PAGES.keys():
            page = view(self, *args, **kwargs)
            self._PAGES[view] = page
            self.centralWidget.addWidget(self._PAGES[view])
        self.centralWidget.setCurrentWidget(self._PAGES[view])
        self.navigationHistory.append(self._PAGES[view].__class__)
        logger.debug(f'Navigated to {view.__name__}, resume: {resume}')
        if resume:
            self._PAGES[view].onResume(*args, **kwargs)
        if not resume:
            window.newViewAdded.emit(self._PAGES[view])
            self._PAGES[view].onCreate(*args, **kwargs)

    def navigateBack(self) -> None:
        """
        navigateBack method for navigating back
        :return: None
        """
        logger.debug(f'navigation history {self.navigationHistory}')
        if len(self.navigationHistory) > 1:
            self.navigationHistory.pop()
            lastView = self.navigationHistory[-1]
            logger.debug(f'last view {lastView}')
            self.navigate(lastView)
        else:
            logger.warning('No more views to navigate back to.')

    def getViews(self) -> Dict[QWidget, Type[QWidget]]:
        """
        getViews method for getting all views
        :return: List[QWidget]
        """
        return self._PAGES

    def removeView(self, view) -> None:
        """
        removeView method for removing a view
        :param view: View to be removed
        :return: None
        """
        try:
            if hasattr(self._PAGES[view.__class__], 'onDestroy') and self._PAGES[view.__class__].onDestroy():
                window.tabRemoved.emit(self._PAGES[view.__class__])
                self.mainLayout.removeWidget(self._PAGES[view.__class__])
                self._PAGES[view.__class__].deleteLater()
                del self._PAGES[view.__class__]
        except KeyError as e:
            logger.error(f'Remove View Error: {e}')

    @pyqtSlot(str)
    def onTabChanged(self, tab: str) -> None:
        """
        onTabChanged method for handling tab changes
        :param tab: Tab name
        :return: None
        """
        pass

    def removeCurrentView(self) -> None:
        """
        removeCurrentView method for removing the current view
        :return: None
        """
        self.removeView(self.centralWidget.currentWidget())
