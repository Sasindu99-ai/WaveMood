from vvecon.qt.util import Style

table = Style("""
QTableWidget [
	margin-top: 20px;
	background-color: transparent;
	color: white;
	border: none;
	outline: none;
]
QTableWidget::item [
	background-color: #555555;
	outline: none;
	border-bottom: 2px solid #262626;
]
QTableWidget#light::item[
	background-color: white;
]
QTableWidget::item:selected [
	background-color: #696969;
]
QTableWidget::item:focus [
	outline: none;
]
QHeaderView::section [
	background-color: #ED7048;
	color: #262626;
	font-weight: 500;
	padding: 5px;
	border-bottom: 2px solid #262626;
	border-left: 1px solid #262626;
	border-top: none;
	font-size: 13px;
	text-align: left;
]
QHeaderView::section:first [
	border-left: none;
]
""")
