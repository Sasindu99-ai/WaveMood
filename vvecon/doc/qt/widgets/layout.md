## Layout Containers

### Widget
`vvecon.qt.contrib.widgets.Widget.Widget`

```python
Widget(
    parent: QWidget | None = None,
    layout: Type[QLayout] = QVBoxLayout,
    spacing: int = 0,
    margin: Margin | None = None,
    alignment: Qt.AlignmentFlag = Qt.AlignLeft,
)
```

Methods:
- `addWidget(widget)`, `addLayout(layout)`
- `addSpacing(px)`, `addStretch(stretch=1)`
- `getLayout()` returns underlying layout

### HBoxWidget
`vvecon.qt.contrib.widgets.Widget.HBoxWidget`
Uses `QHBoxLayout`, same params as `Widget` except no `layout` arg.

### VBoxWidget
`vvecon.qt.contrib.widgets.Widget.VBoxWidget`
Uses `QVBoxLayout`.

### Example
```python
from vvecon.qt.contrib.widgets.Widget import HBoxWidget, VBoxWidget
from vvecon.qt.contrib.widgets import Margin

row = HBoxWidget(spacing=8, margin=Margin(horizontal=12, vertical=6))
row.addWidget(Button(text='A'))
row.addWidget(Button(text='B'))

col = VBoxWidget(spacing=12)
col.addLayout(row.getLayout())
```


