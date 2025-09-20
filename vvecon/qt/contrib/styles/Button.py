from vvecon.qt.contrib.widgets import Margin, Padding
from vvecon.qt.util import Style

__all__ = [
	'defaultButton', 'primaryButton', 'secondaryButton', 'successButton', 'warningButton', 'dangerButton',
	'infoButton', 'lightButton', 'darkButton', 'noButton', 'transparentButton'
]

defaultButton = Style("""
QToolButton [
	background-color: {backgroundColor};
	color: {color};
	border: none;
	font-family: {fontFamily};
	font-size: {fontSize}px;
	font-weight: {fontWeight};
	margin: {margin};
	border-radius: {radius}px;
	padding: {padding};
	text-align: {textAlign};
]
QToolButton:hover [
	background-color: {hoverColor};
]

QToolButton::icon [
	margin: {iconMargin};
]"
""", **dict(
	fontSize=12,
	hoverColor='#C15532',
	backgroundColor='#E95525',
	color='white',
	fontWeight='500',
	fontFamily="'Inter'",
	margin=Margin(0).qss,
	iconMargin=Margin(0).qss,
	radius=4,
	padding=Padding(5).qss,
	textAlign='center',
))

primaryButton = defaultButton.update(**dict(
	backgroundColor='#E95525',
	hoverColor='#C15532',
	color='white'
))

secondaryButton = defaultButton.update(**dict(
	backgroundColor='#D9D9D9',
	hoverColor='#BFBFBF',
	color='#000000',
))

successButton = defaultButton.update(**dict(
	backgroundColor='#13AE82',
	hoverColor='#0F9E6A',
))

warningButton = defaultButton.update(**dict(
	backgroundColor='#FFCC00',
	hoverColor='#FFB300',
	color='#000000',
))

dangerButton = defaultButton.update(**dict(
	backgroundColor='#F44336',
	hoverColor='#D32F2F',
))

infoButton = defaultButton.update(**dict(
	backgroundColor='#03A9F4',
	hoverColor='#0288D1',
))

lightButton = defaultButton.update(**dict(
	backgroundColor='#F0F0F0',
	hoverColor='#E5E5E5',
	color='#333333',
))

darkButton = defaultButton.update(**dict(
	backgroundColor='#424242',
	hoverColor='#212121',
))

noButton = defaultButton.update(**dict(
	backgroundColor='transparent',
	hoverColor='#E5E5E5',
	color='#333333',
))

transparentButton = defaultButton.update(**dict(
	backgroundColor='transparent',
	hoverColor='transparent',
	color='#333333',
))
