## Util

### ui (`vvecon.qt.util.ui.ui`)
```python
ui.setLogicalDpi(dpi: int) -> None
ui.dpiFactor -> float
ui.dp(unit: int) -> int
ui.sp(unit: int) -> int
ui.size(w: int, h: int) -> QSize
ui.pixmap(path: str, width: int | None = None, height: int | None = None, aspect_ratio_mode=..., transform_mode=...) -> QPixmap
ui.icon(path: str, ...) -> QIcon
```

### Settings (`vvecon.qt.util.Settings.Settings`)
Encrypted per-app settings using `LOCALAPPDATA/<APP_NAME>/.vvecon/`.
```python
Settings.set(key: str, value: str) -> None
Settings.get(key: str, default: str | None = None) -> str | None
Settings.remove(key: str) -> None
```
Environment required: `BASE_PATH`, `APP_NAME`, optional `SECRET_KEY`.

### Style / StyleSheet
`vvecon.qt.util.Style`, `StyleSheet` are used by contrib styles to apply QSS. Typical usage:
```python
style.apply(widget)  # or style.update(padding='8px 12px', radius=6).qss
```

### Util
`vvecon.qt.util.Util` contains filesystem helpers (e.g., `mkSecretDir`) used by Settings.


