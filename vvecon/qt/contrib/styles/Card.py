from vvecon.qt.util import Style

__all__ = ['primaryCard']

primaryCard = Style("""
QFrame [
	background-color: {backgroundColor};
	border-radius: {borderRadius}px;
	border: {borderWidth}px solid {borderColor};
]
""", **dict(
    backgroundColor='#FAFAFA',
    borderRadius=4,
    borderColor='#D9D9D9',
    borderWidth=1
))
