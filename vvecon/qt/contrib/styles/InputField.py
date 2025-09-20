from vvecon.qt.contrib.widgets import Padding
from vvecon.qt.util import Style

label = Style("""
font-size: {fontSize}px;
color: {color};
padding: {padding};
""", **dict(
	fontSize=12,
	color='white',
	padding=Padding(3, 0, 0, 0).qss
))

container = Style("""
background-color: {backgroundColor};
border-radius: {borderRadius}px;
border: {border};
""", **dict(
	backgroundColor='#B6B6B6',
	borderRadius=4,
	border='none'
))

searchContainer = container.update(**dict(
	backgroundColor='#B6B6B6',
))

pinkContainer = container.update(**dict(
	backgroundColor='#F9CFC2',
))

lineEdit = Style("""
font-size: {fontSize}px;
background-color: {backgroundColor};
border: {border};
color: {color};
""", **dict(
	fontSize=13,
	backgroundColor='transparent',
	border='none',
	color='black'
))

errorContainer = container.update(**dict(
	border='1px solid #C74343'
))

successContainer = container.update(**dict(
	border='1px solid #198754'
))

bottomLabel = Style("""
font-size: {fontSize}px;
color: {color};
""", **dict(
	fontSize=12,
	color='#4B4B4B'
))

errorBottomLabel = bottomLabel.update(**dict(
	color='#C74343'
))

successBottomLabel = bottomLabel.update(**dict(
	color='#198754'
))

lightInputField = dict(
	label = Style("""
	font-size: {fontSize}px;
	color: {color};
	padding: {padding};
	""", **dict(
		fontSize=12,
		color='black',
		padding=Padding(3, 0, 0, 0).qss
	)),

	container = Style("""
	background-color: {backgroundColor};
	border-radius: {borderRadius}px;
	border: {border};
	""", **dict(
		backgroundColor='#f9f9f9',
		borderRadius=4,
		border='1px solid #CACACA'
	)),

	searchContainer = container.update(**dict(
		backgroundColor='#ffffff',
		border='1px solid #AEAEAE'
	)),

	lineEdit = Style("""
	font-size: {fontSize}px;
	background-color: {backgroundColor};
	border: {border};
	""", **dict(
		fontSize=16,
		backgroundColor='transparent',
		border='none'
	)),

	errorContainer = container.update(**dict(
		border='1px solid #C74343'
	)),

	successContainer = container.update(**dict(
		border='1px solid #198754'
	)),

	bottomLabel = Style("""
	font-size: {fontSize}px;
	color: {color};
	""", **dict(
		fontSize=12,
		color='#4B4B4B'
	)),

	errorBottomLabel = bottomLabel.update(**dict(
		color='#C74343'
	)),

	successBottomLabel = bottomLabel.update(**dict(
		color='#198754'
	)),
)
