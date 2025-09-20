from vvecon.qt.contrib.widgets import Margin
from vvecon.qt.enums import FontWeight
from vvecon.qt.util import Style

styleSheet = """
font-family: 'Inter';

QLabel#h1 {
    font-size: 36px;
    font-weight: bold;
    color: #333333;
    margin: 10px 0;
    text-align: center;
}
"""

header = """
QLabel {
    font-size: 36px;
    font-weight: bold;
    color: #333333;
    margin: 10px 0;
    text-align: center;
}
"""

h1 = Style("""
QLabel [
	background-color: {backgroundColor};
	font-family: {fontFamily};
	font-weight: {fontWeight};
	font-size: {fontSize}px;
	border: {border};
	color: {color};
	margin: {margin};
]
""", **dict(
	fontFamily="'Inter'",
	fontWeight=FontWeight.Bold,
	fontSize=36,
	border='none',
	color='white',
	margin=Margin(0, 0, 0, 20).qss,
	backgroundColor='transparent'
))

h2 = h1.update(
	fontSize=32
)

h3 = h1.update(
	fontSize=28
)

h4 = h1.update(
	fontSize=24,
	fontWeight=FontWeight.SemiBold
)

h5 = h1.update(
	fontSize=20,
	fontWeight=FontWeight.Medium
)

h6 = h1.update(
	fontSize=16,
	fontWeight=FontWeight.Normal
)

tabButton = """
QToolButton {
	background-color: red;
	color: red;
	font-family: 'Inter';
	padding-top: 10px;
	padding-bottom: 10px;
	padding-left: 20px;
}
"""
