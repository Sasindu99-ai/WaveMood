## Card Components

### ScrollableCard
`vvecon.qt.contrib.widgets.Card.ScrollableCard`

Styled frame with an internal `ScrollArea` and a content widget with `QVBoxLayout`.

Signals:
- `scrollBarVisibilityChanged: pyqtSignal(bool)` — True if vertical scrollbar visible

Key methods:
- `setScrollAreaStyleSheet(qss: str)`
- `setScrollAreaLayout(layout: QLayout)` — replace inner layout if needed

Example:
```python
from vvecon.qt.contrib.widgets.Card import ScrollableCard
card = ScrollableCard(margin=Margin(12))
card.layout.addWidget(Button(text='Inside card'))
```

### ScrollArea
`vvecon.qt.contrib.widgets.Card.ScrollArea`

Emits:
- `verticalScrollBarStateChanged(bool)`
- `horizontalScrollBarStateChanged(bool)`

Used by `ScrollableCard` to adjust right padding when scrollbar appears.


