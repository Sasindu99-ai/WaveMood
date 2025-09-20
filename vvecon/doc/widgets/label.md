## Label (Clickable QLabel)

Class: `vvecon.qt.contrib.widgets.QLabel.Label`

### Signature
```python
Label(*args, onClick: Callable | None = None, **kwargs)
```

When clicked, invokes the provided `onClick()` callback.

Important: Provide an `onClick` function; otherwise calling `self.onClick()` on mouse press would fail.

### Example
```python
from vvecon.qt.contrib.widgets.QLabel import Label

label = Label('Open settings', onClick=lambda: print('clicked'))
```


