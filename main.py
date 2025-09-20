import faulthandler
import logging
import os
import sys

from env import env
from PyQt6.QtCore import QCoreApplication, Qt
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


if __name__ == '__main__':
	app = QApplication(sys.argv)
	# ic.disable()
	QFontDatabase.addApplicationFont('lib/res/fonts/Inter.ttf')
	app.setFont(QFont('Inter', 9))

	from vvecon.qt.res import Icons
	app.setWindowIcon(Icons.settings_applications)

	from WaveMood import WaveMood
	WaveMood()
	sys.exit(app.exec())
