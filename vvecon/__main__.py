import os
import sys

from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
	args = sys.argv
	if len(args) == 3 and args[1] == 'qt' and args[2] == 'icons':
		print(os.path.dirname(__file__))
		os.chdir(os.path.dirname(__file__))
		app = QApplication(sys.argv)
		from vvecon.qt.res.IconExplorer import IconsExplorer
		from vvecon.qt.res.Icons import iconSet
		window = IconsExplorer(iconSet)
		window.show()
		sys.exit(app.exec())
