## API Reference (vvecon.qt)

This reference lists public modules/classes commonly used in apps. Import paths are shown as backticks.

### Core (`vvecon.qt.core`)
- `Window` (`vvecon.qt.core.Window`)
  - Properties: `mainWidget`, `mainLayout`, `centralWidget`, `navigationHistory`
  - Methods: `navigate(view_cls, *args, **kwargs)`, `navigateBack()`, `getViews()`, `removeView(view)`, `removeCurrentView()`
  - Signals: `vvecon.qt.signals.window.newViewAdded`, `vvecon.qt.signals.window.tabRemoved`
- `View` (`vvecon.qt.core.View`)
  - Ctor: `View(parent: Window | None, name: str | None = None)`
  - Lifecycle: `onCreate()`, `onResume()`, `onDestroy()`
  - Methods: `setViewName(name)`, `getViewName()`, `setStatus(isBusy)`, `navigate(view_cls, *args, **kwargs)`

### Res (`vvecon.qt.res`)
- `Icons` (`vvecon.qt.res.Icons.Icons`) — Material Symbols fluent API
- `Theme` (`vvecon.qt.res.Theme.Theme`) — configure `colorPalette`, `images`, `locale`; call `Theme.setColorTheme(theme)`
- `Images` (`vvecon.qt.res.Images.Images`) — theme-aware image paths
- `LocaleBuilder` (`vvecon.qt.res.LocaleBuilder.LocaleBuilder`) — JSON-based i18n
- `ColorTheme` (`vvecon.qt.res.ColorTheme.ColorTheme`) — color palette dataclass

### Util (`vvecon.qt.util`)
- `ui` — DPI-aware helpers: `dp(px)`, `sp(px)`, `size(w,h)`, `pixmap(path, w, h)`, `icon(...)`, `setLogicalDpi(dpi)`
- `Settings` — encrypted app-local settings: `set(key,val)`, `get(key, default=None)`, `remove(key)`
- `Style`, `StyleSheet` — style composition helpers used by contrib styles
- `Util`, `Settings` and other helpers as needed by widgets/styles

### API (`vvecon.qt.api`)
- `Controller` — HTTP helper with JSON, bearer auth via `Settings`, refresh logic

### Env (`vvecon.qt.env`)
- `Env`, `EnvManager` — environment variables and export to `os.environ`

### Threading (`vvecon.qt.thread`)
- `threadPool` — singleton; `start(func, *args, delay=0, callback=None)`, `stop(func)`, `stopAll()`, `clearAll()`
- `Worker` — internal `QRunnable` wrapper with `finished` signal

### Signals (`vvecon.qt.signals`)
- `SignalPool` — base for grouping signals
- `window` — shared window signals: `newViewAdded`, `tabRemoved`

### DB (`vvecon.qt.db`)
- `Database` — wrapper around SQLAlchemy: `Model` base, `session`, `create_all()`

### Logger (`vvecon.qt.logger`)
- `logger` — convenience wrapper for Python logging with filename:line in messages


