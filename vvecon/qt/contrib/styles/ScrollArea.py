from vvecon.qt.util import Style

__all__ = ['basic']

basic = Style("""
QScrollArea [
	border: none;
	background: transparent;
]

QScrollBar:vertical [
	border: none;
	background-color: transparent;
	border-radius: 8px;
	width: 18px;
	margin-left: 10px;
]

QScrollBar::handle:vertical [
	background: #287DC5;
	border-radius: 3px;
]

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical [
	border: none;
	height: 0px;
]

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical [
	background: transparent;
]
""")
