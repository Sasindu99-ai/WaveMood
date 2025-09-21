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
		# self.setMinimumSize(ui.size(800, 600))
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


if __name__ == '__main__':
	import faulthandler
	import logging
	import os
	import sys
	from env import env
	from PyQt6.QtCore import QCoreApplication
	from PyQt6.QtGui import QFont, QFontDatabase
	from PyQt6.QtWidgets import QApplication

	env.init()

	QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
	logging.getLogger('urllib3').setLevel(logging.DEBUG)
	faulthandler.enable()

	if getattr(sys, 'frozen', False):
		ROOTPATH = os.path.dirname(sys.executable)
	else:
		ROOTPATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	os.chdir(ROOTPATH)
	os.environ.setdefault('BASE_PATH', ROOTPATH)
	os.environ.setdefault('APP_NAME', 'Nevada Broadcaster')

	app = QApplication(sys.argv)
	# ic.disable()
	QFontDatabase.addApplicationFont('lib/res/fonts/Inter.ttf')
	app.setFont(QFont('Inter', 9))

	from vvecon.qt.res import Icons
	app.setWindowIcon(Icons.settings_applications)

	WaveMood()
	sys.exit(app.exec())
