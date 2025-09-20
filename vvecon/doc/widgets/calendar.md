## CalendarPopup

Class: `vvecon.qt.contrib.widgets.Calender.CalenderPopup.CalendarPopup`

Styled `QCalendarWidget` with custom navigation buttons and paint for selected day.

### Behavior
- Hides grid and vertical header, uses single-letter weekday headers
- Applies custom styles and round highlight for selected date
- Replaces prev/next icons with `vvecon.qt.res.Icons`

### Usage
```python
from vvecon.qt.contrib.widgets.Calender.CalenderPopup import CalendarPopup

cal = CalendarPopup(parent)
cal.setSelectedDate(QDate.currentDate())
```

InputField with `inType=DATE` opens this calendar in a frameless dialog and emits `dateSelected`.


