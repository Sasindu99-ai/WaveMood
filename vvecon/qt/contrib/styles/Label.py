from vvecon.qt.contrib.widgets import Padding
from vvecon.qt.enums import FontWeight
from vvecon.qt.util import Style

__all__ = ['label', 'successBg', 'errorBg', 'transparentBg']

label = Style("""
QLabel [
	background-color: {backgroundColor};
	color: {color};
	border: {border};
	border-radius: {radius}px;
	padding: {padding};
	font-size: {fontSize}px;
	text-align: {textAlign};
	font-weight: {fontWeight};
]
""", **dict(
	color='black',
	fontSize=12,
	textAlign='center',
	border='none',
	backgroundColor='transparent',
	padding=Padding(0).qss,
	radius=0,
	fontWeight=FontWeight.Normal
))

successBg = label.update(**dict(
	backgroundColor='#4CAF50',
	color='#FFFFFF'
))

errorBg = label.update(**dict(
	backgroundColor='#F44336',
	color='#FFFFFF'
))

transparentBg = label.update(**dict(
	backgroundColor='transparent',
	color='black'
))
