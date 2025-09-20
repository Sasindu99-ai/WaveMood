from vvecon.qt.util import Style

__all__ = ['menu']

menu = Style("""
QMenu [
	background-color: #C6C6C6;
	color: black;
	border-radius: 5px;
	border: 2px solid #B6B6B6;
	padding: 5px;
	padding-left: 0px;
]
QMenu::indicator [
	width: 0px;
	height: 0px;
]
QAction [
	background-color: transparent;
	padding: 0px;
]
QAction::hover [
	background-color: #F0F0FF;
]
""")
