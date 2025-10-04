from Components.Common import Padding
from vvecon.qt.enums import FontWeight
from vvecon.qt.util import Style

__all__ = ['comboBox']

comboBox = Style("""
QComboBox [
	background-color: {backgroundColor};
	color: {color};
	padding: {padding};
	font-size: {fontSize}px;
	text-align: {textAlign};
	font-weight: {fontWeight};
	border: {border};
	border-radius: {radius}px;
	selection-background-color: {selectionBackground};
]

/* Dropdown arrow */
QComboBox::drop-down [
	border: none;
	width: 20px;
	background: transparent;
]
QComboBox::down-arrow [
	image: url(lib/res/images/0/down_arrow.png);
	width: 12px;
	height: 12px;
	padding-right: 10px;
]


/* When hovered */
QComboBox:hover [
	border: 1px solid {hoverBorder};
	background-color: {hoverBackground};
]

/* When clicked/focused */
QComboBox:focus [
	border: 1px solid {focusBorder};
	background-color: {focusBackground};
]

/* Dropdown popup */
QComboBox QAbstractItemView [
	background-color: {dropdownBackground};
	border: {border};
	selection-background-color: {selectionBackground};
	outline: 0;
]

QComboBox QAbstractItemView::item [
	padding-left: 10px;
	padding-top: 5px;
	padding-bottom: 5px;
]

""", **dict(
	color='black',
	fontSize=12,
	textAlign='center',
	border='1px solid #D9D9D9',
	backgroundColor='#FFFFFF',
	padding=Padding(6, 10).qss,
	radius=6,
	fontWeight=FontWeight.Normal,
	hoverBorder='#A6A6A6',
	hoverBackground='#F5F5F5',
	focusBorder='#0078D4',
	focusBackground='#E6F2FF',
	dropdownBackground='#FFFFFF',
	selectionBackground='#0078D4'
))
