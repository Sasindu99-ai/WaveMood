## Toasts / Message Popups

### MessagePopup
`vvecon.qt.contrib.widgets.Toast.MessagePopup`

```python
MessagePopup(
    parent=None,
    title: str = '',
    msg: str = '',
    img: QPixmap = default,
    confirmText: str = 'Proceed',
    styleScheme: ToastStyleScheme = ToastStyleScheme(),
    margin: Margin = Margin(vertical=ui.dp(40), horizontal=ui.dp(80)),
)
```

Frameless, translucent dialog with title, message, and confirm button.

Methods:
- `onConfirm()` closes dialog; Enter/Return triggers confirm
- `showOverlay()`/`hideOverlay()` call optional parent spinner methods

### Variants
- `SuccessPopup(...)`
- `DangerPopup(...)`
- `WarningPopup(...)`

Example:
```python
from vvecon.qt.contrib.widgets.Toast import SuccessPopup

SuccessPopup(title='Saved', msg='Your changes were saved.').exec()
```


