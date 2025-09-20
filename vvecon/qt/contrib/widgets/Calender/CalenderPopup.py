from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen
from PyQt6.QtWidgets import QCalendarWidget, QToolButton

from vvecon.qt.contrib import styles
from vvecon.qt.res import Icons

__all__ = ['CalendarPopup']


class CalendarPopup(QCalendarWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setGridVisible(False)
		self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
		self.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)

		text_format = self.weekdayTextFormat(Qt.DayOfWeek.Saturday)
		text_format.setForeground(QColor('black'))
		self.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, text_format)
		self.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, text_format)

		self.setStyleSheet(styles.Calender.calendarPopup.qss)

		self.customize_navigation_buttons()

	def customize_navigation_buttons(self):
		prev_month_button = self.findChild(QToolButton, 'qt_calendar_prevmonth')
		next_month_button = self.findChild(QToolButton, 'qt_calendar_nextmonth')
		month_year_label = self.findChild(QToolButton, 'qt_calendar_monthbutton')
		year_label = self.findChild(QToolButton, 'qt_calendar_yearbutton')

		button_size = QSize(42, 42)
		if prev_month_button:
			prev_month_button.setFixedSize(button_size)
			prev_month_button.setIcon(Icons.Rounded.left_arrow)
			prev_month_button.setIconSize(button_size)
		if next_month_button:
			next_month_button.setFixedSize(button_size)
			next_month_button.setIcon(Icons.Rounded.right_arrow)
			next_month_button.setIconSize(button_size)

		if month_year_label:
			month_year_label.setStyleSheet(styles.Calender.monthField.qss)

			month_year_label.setArrowType(Qt.ArrowType.NoArrow)

		if year_label:
			year_label.setStyleSheet(styles.Calender.yearField.qss)

			year_label.setArrowType(Qt.ArrowType.NoArrow)
			year_label.setPopupMode(
				QToolButton.ToolButtonPopupMode.InstantPopup)
			year_label.setMenu(None)

		prev_month_button.setStyleSheet('margin: 0; padding: 0;')
		next_month_button.setStyleSheet('margin: 0; padding: 0;')

	def paintCell(self, painter, rect, date):
		if date == self.selectedDate():
			painter.save()
			painter.setRenderHint(QPainter.RenderHint.Antialiasing)

			painter.setBrush(QBrush(Qt.GlobalColor.transparent))
			painter.setPen(QPen(Qt.PenStyle.NoPen))
			painter.drawRect(
				rect)

			painter.setBrush(QColor(38, 123,
									195))
			ellipse_rect = rect.adjusted(
				6, 4, -6, -4)
			painter.drawEllipse(ellipse_rect)

			painter.setPen(QColor('white'))
			painter.setFont(
				self.font())

			painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(date.day()))

			painter.restore()
		else:
			current_month = self.selectedDate().month()
			current_year = self.selectedDate().year()

			if date.month() != current_month or date.year() != current_year:
				painter.save()

				painter.setPen(QColor(169, 169, 169))

				super().paintCell(painter, rect, date)

				painter.restore()
			else:
				super().paintCell(painter, rect, date)
