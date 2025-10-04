## Core

### Window (`vvecon.qt.core.Window`)

Constructor:
```python
Window(
    parent: QWidget | None = None,
    *,
    row: int = 1,
    column: int = 1,
    rowSpan: int = 1,
    columnSpan: int = 1,
    alignment: Qt.AlignmentFlag = Qt.AlignCenter,
)
```

Properties:
- `mainWidget: QWidget`
- `mainLayout: QGridLayout`
- `centralWidget: QStackedWidget`
- `navigationHistory: list[type]`

Methods:
```python
def navigate(self, view: type[QWidget], *args, **kwargs) -> None
    # On first visit: constructs view(self, *args, **kwargs), adds to stack,
    # emits window.newViewAdded(view_instance), then calls view.onCreate()
    # On revisit: calls view.onResume()

def navigateBack(self) -> None
    # Goes to previous view type in navigationHistory if available

def getViews(self) -> dict[QWidget, type[QWidget]]

def removeView(self, view: QWidget) -> None
    # Calls view.onDestroy(); if True, removes and deletes

def removeCurrentView(self) -> None
```

Signals (via `vvecon.qt.signals.window`): `newViewAdded(object)`, `tabRemoved(object)`

### View (`vvecon.qt.core.View`)

Constructor:
```python
View(parent: Window | None, name: str | None = None)
```

Lifecycle:
```python
def onCreate(self) -> None: ...
def onResume(self) -> None: ...
def onDestroy(self) -> bool:  # return False to block removal when busy
```

APIs:
```python
def setViewName(self, name: str) -> None
def getViewName(self) -> str
def setStatus(self, isBusy: bool) -> None
def navigate(self, view: type['View'], *args, **kwargs) -> None  # delegates to parent
```


