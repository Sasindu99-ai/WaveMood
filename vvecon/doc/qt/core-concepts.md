## Core Concepts

### Window
`vvecon.qt.core.Window` is a `QMainWindow` with a `QStackedWidget` as the central area and simple navigation.

Key APIs:
- `navigate(view_cls, *args, **kwargs)`: create or resume a `View` subclass and show it
- `navigateBack()`: go back to previous view (when supported)
- `mainWidget`, `mainLayout`, `centralWidget`: layout primitives
- Signals: `vvecon.qt.signals.window.newViewAdded` emitted when a new view is created

Initialization also sets logical DPI in `ui` so `dp()/sp()` scale correctly on your display.

### View
`vvecon.qt.core.View` is a `QWidget` base with lifecycle hooks:
- `onCreate(self)`: called the first time the view is shown
- `onResume(self)`: called when returning to an existing view
- `setViewName(name)`, `getViewName()`

Navigate from views just like in MKT:
```python
class HomeView(View):
    def onEmailButtonClick(self):
        self.navigate(EmailMKTView)  # delegates to parent window
```

If you prefer explicit calls:
```python
self.parent.navigate(EmailMKTView)
```

### Navigation history
The window tracks `navigationHistory` internally. You can implement back behavior in your own top bar and trigger `navigateBack()` when needed.


