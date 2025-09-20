## Theming, Icons, and UI Utilities

### Theming
Create an app theme by extending `vvecon.qt.res.Theme` and defining `ColorTheme`, `Images`, and `LocaleBuilder`.

MKT example:
```python
# res/AppTheme.py
from vvecon.qt.res import Theme as ThemeMeta, ColorTheme, Images, LocaleBuilder
from enums import Theme, Locale

class AppTheme(ThemeMeta):
    colorTheme = Theme.LIGHT
    colorPalette = {
        Theme.LIGHT: ColorTheme(primary="#4CAF50", secondary="#FF9800", background="#FFFFFF", text="#212121", accent="#03A9F4", error="#F44336"),
        Theme.DARK:  ColorTheme(primary="#4CAF50", secondary="#FF9800", background="#121212", text="#E0E0E0", accent="#03A9F4", error="#F44336"),
    }
    colors = colorPalette[colorTheme]

    imageTheme = Theme.LIGHT
    images = Images(theme=Theme.LIGHT, default=Theme.LIGHT, logo="logo.png")

    locale = LocaleBuilder(locale=Locale.enUS, default=Locale.enUS)
```

Apply theme and palette in your window:
```python
from PyQt6.QtGui import QPalette
from res import AppTheme

AppTheme.setColorTheme(Theme.DARK)
pal = window.palette()
pal.setColor(QPalette.ColorRole.Window, AppTheme.colors.background)
pal.setColor(QPalette.ColorRole.WindowText, AppTheme.colors.text)
window.setPalette(pal)
```

### Icons
`vvecon.qt.res.Icons` provides Material Symbols via a fluent API:
```python
from vvecon.qt.res import Icons
from vvecon.qt.util import ui

icon = Icons.Rounded.mail.setColor('#FFFFFF').setSize(ui.dp(100))
button.setIcon(icon)
```

Browse icons:
```bash
python -m vvecon qt icons
```

### UI utilities
`vvecon.qt.util.ui` exposes density-aware helpers:
- `ui.dp(px)`, `ui.sp(px)`: scale by logical DPI
- `ui.size(w, h)`: returns `QSize` with `dp` scaling
- `ui.pixmap(path, w, h)`, `ui.icon(path, ...)`: load assets

`Window` sets logical DPI automatically; you can override via `ui.setLogicalDpi(dpi)`.


