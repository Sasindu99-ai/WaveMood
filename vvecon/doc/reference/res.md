## Res

### Theme (`vvecon.qt.res.Theme.Theme`)
Class variables to define in your app theme class:
```python
colorTheme: Enum
imageTheme: Enum
colorPalette: dict[Enum, ColorTheme]
images: Images
colors: ColorTheme
locale: LocaleBuilder
```

Methods:
```python
@classmethod
def setColorTheme(cls, theme: Enum) -> None
    # Validates and sets cls.colorTheme and cls.colors
```

`__setattr__` reacts to setting `imageTheme` and `colorTheme` (updates `images`/`colors`).

### Images (`vvecon.qt.res.Images.Images`)
```python
Images(base: str = 'res/images/', theme: Enum, default: Enum, **images)
```
Attributes set via kwargs become image names (e.g., `logo='logo.png'`).

Methods:
```python
setBase(base: str) -> None
getBase() -> str
setTheme(theme: Enum) -> None
getTheme() -> Enum
setDefaultTheme(default: Enum) -> None
getDefaultTheme() -> Enum
```
Accessing an attribute returns the resolved path: prefers current theme, falls back to default.

### LocaleBuilder (`vvecon.qt.res.LocaleBuilder.LocaleBuilder`)
```python
LocaleBuilder(base: str = 'res/locale', locale: Enum, default: Enum)
```
Methods:
```python
setBase(base: str) -> None
getBase() -> str
setLocale(locale: Enum) -> None
getLocale() -> Enum
setDefaultLocale(default: Enum) -> None
getDefaultLocale() -> Enum
get(key: str) -> str
```
Accessing an attribute returns the localized string from current or default JSON.

### Icons (`vvecon.qt.res.Icons.Icons`)
Fluent API for Material Symbols. Example:
```python
from vvecon.qt.res import Icons
icon = Icons.Rounded.check.setColor('#fff').setSize(24)
pix = icon.pixmap(QSize(24,24))
```


