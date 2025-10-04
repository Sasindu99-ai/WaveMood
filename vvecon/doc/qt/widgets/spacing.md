## Spacing Helpers

### Margin
`vvecon.qt.contrib.widgets.Margin`

Constructors:
- `Margin(all: int)`
- `Margin(horizontal: int, vertical: int)`
- `Margin(left: int, top: int, right: int, bottom: int)`
- `Margin(horizontal=..., vertical=...)` or individual kwargs

Properties:
- `qss` → `'top right bottom left'` with px units or `'0'`
- `totalHorizontal()`, `totalVertical()`

### Padding
`vvecon.qt.contrib.widgets.Padding` — same API as `Margin`.

### Example
```python
from vvecon.qt.contrib.widgets import Margin, Padding

widget.setContentsMargins(Margin(8))
button.setStyleSheet(style.update(padding=Padding(horizontal=8, vertical=4).qss).qss)
```


