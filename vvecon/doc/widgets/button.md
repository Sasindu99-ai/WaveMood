## Button (QToolButton)

Class: `vvecon.qt.contrib.widgets.QButton.Button`

### Signature
```python
Button(
    text: str = '',
    tooltip: str = '',
    icon: QIcon | None = None,
    iconSize: QSize | None = None,
    padding: Padding | None = None,
    style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonFollowStyle,
    direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
    styleSheet: Style | str | None = None,
    onClick: Callable | None = None,
    spaceBetween: int = 0,
)
```

### Attributes and methods
- `setText(str)` / `setToolTip(str)`
- `setIcon(QIcon, iconSize: QSize | None = None)` / `setIconSize(QSize)`
- `setPadding(Padding)` to apply content margins
- `setStyle(Qt.ToolButtonStyle)` and `setDirection(Qt.LayoutDirection)`
- `onClick(callable)` connects to `clicked`
- `onPress(callable)` triggers on mouse press (before click)
- `sizeHint()` considers icon size and padding

Icon/text layout auto-selects a tool button style when not explicitly provided.

### Examples
```python
from vvecon.qt.contrib.widgets import Button, Padding
from vvecon.qt.res import Icons
from vvecon.qt.util import ui
from PyQt6.QtCore import Qt

# Icon-only button
btn = Button(icon=Icons.Rounded.search, iconSize=ui.size(24, 24))

# Text-only button
btn2 = Button(text='Save', onClick=lambda: print('save'))

# Text under icon
btn3 = Button(
    text='Upload',
    icon=Icons.Rounded.upload,
    iconSize=ui.size(48, 48),
    style=Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
    padding=Padding(vertical=ui.dp(8), horizontal=ui.dp(12)),
)

# Press-only handler (e.g., show menu)
def on_press(ev):
    print('pressed at', ev.globalPosition())
btn.onPress(on_press)
```


