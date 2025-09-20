## Widgets and Styles

vvecon ships with convenience widgets and style helpers under `vvecon.qt.contrib`.

Common imports used in MKT:
```python
from vvecon.qt.contrib.widgets import Button, Margin, Padding
from vvecon.qt.contrib.styles.Button import successButton, infoButton
from vvecon.qt.contrib.widgets.Table import TableWidget, Header, Row, Cell
from vvecon.qt.contrib.widgets.Widget import HBoxWidget
```

### Buttons
```python
from vvecon.qt.res import Icons
from vvecon.qt.util import ui

emailButton = Button(
    text='Email\nMarketing',
    icon=Icons.Rounded.mail.setColor('#FFFFFF').setSize(ui.dp(100)),
    iconSize=ui.size(100, 100),
    style=Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
    onClick=self.onEmailButtonClick,
)
emailButton.setStyleSheet(successButton.update(fontSize=ui.sp(16)).qss)
```

### Layout helpers
- `Margin(horizontal=..., vertical=...)`
- `Padding(horizontal=..., vertical=...)`
- `HBoxWidget(parent, spacing=..., margin=Margin(...))`

### Table
MKT uses `TableWidget` with `Header`, `Row`, `Cell` for custom table UIs. See `views/EmailMKTView.py` for usage.


