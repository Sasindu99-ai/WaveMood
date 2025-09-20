from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPalette

from components.sections import TopBar
from enums import Theme
from vvecon.qt.core import Window
from vvecon.qt.util import ui
from res import AppTheme

__all__ = ['WaveMood']


class WaveMood(Window):
    topBar: TopBar

    def __init__(self):
        super(WaveMood, self).__init__(row=4, column=2)

        self.setObjectName('MainWindow')
        self.setWindowTitle('WaveMood')
        AppTheme.setColorTheme(Theme.DARK)
        self.setWindowIcon(QIcon(ui.pixmap(
            AppTheme.images.logo, 32, 32, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )))
        self.setMinimumSize(ui.size(800, 600))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, AppTheme.colors.background)
        pal.setColor(QPalette.ColorRole.WindowText, AppTheme.colors.text)
        self.setPalette(pal)
        self.setFocus()

        self.setupTopBar()

        from views import HomeView
        self.navigate(HomeView)

        self.show()

    def setupTopBar(self):
        self.topBar = TopBar(self.mainWidget)
        self.mainLayout.addWidget(self.topBar, 3, 2)

    def f11(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
