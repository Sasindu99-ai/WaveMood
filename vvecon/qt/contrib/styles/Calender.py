from vvecon.qt.util import Style, ui

__all__ = ['calendarPopup', 'monthField', 'yearField']

calendarPopup = Style("""
QCalendarWidget QAbstractItemView [
	color: {foregroundColor};
]
QCalendarWidget QWidget [  /* Month and year selectors */
	color: {foregroundColor};
	font-size: {fontSize}px;
	background-color: {backgroundColor};
]
QCalendarWidget QToolButton {  /* Navigation buttons */
	color: {foregroundColor};
	font-size: {fontSize}px;
	background-color: transparent;
	border: none;
}
QCalendarWidget QHeaderView {  /* Day names header */
	background: {backgroundColor};
}
""", **dict(
    foregroundColor='black',
    backgroundColor='#F5F5F5',
    fontSize=ui.sp(16)
))

monthField = Style("""
background-color: #F5F5F5;
color: #4B4B4B;
font-size: 16px;
font-weight: bold;
border-radius: 5px
padding: 5px 15px;
margin-left: 0px;
margin-right: 100px;
""")

yearField = Style("""
color: #4B4B4B;
font-size: 16px;            /* Font size */
font-weight: bold;          /* Bold text */
border-radius: 5px;        /* Rounded corners */
padding: 5px 15px;
""")
