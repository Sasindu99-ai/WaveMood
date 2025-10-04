## InputField

Class: `vvecon.qt.contrib.widgets.Input.InputField`

Types: `vvecon.qt.enums.InputType` → TEXT, NUMBER, SEARCH, DATE

### Signature
```python
InputField(
    parent=None,
    name: str = '',
    inType: InputType = InputType.TEXT,
    width: int | None = None,
    height: int = 40,
    hint: str | None = None,
    placeholder: str = '',
    isLight: bool = False,
    icon: str | None = None,
    step: float = 0,
    maxVal: float | None = None,
    minVal: float | None = None,
    showTooltipIcon: bool = False,
    validator: Callable | None = None,
    styleScheme: StyleScheme | None = None,
    default: object | None = None,
)
```

### Signals and hooks
- `dateSelected: pyqtSignal(str)` for DATE type
- `inputClicked: pyqtSignal()` (icon click on TEXT with icon)
- `returnPressed` (proxy to QLineEdit)
- `onEnter(func)` to run after validation on Enter

### Methods
- `setValue(val)`, `getValue()` → str/int/float/datetime/None depending on type
- `validate()` → True or raises via `callback=displayError`
- `getValidatedValue()` → value if valid
- `displayError(msg)`, `displaySuccess(msg)` show styled bottom label
- `clear()`, `setFocus()`, `setDisabled(bool)`, `text()`

### StyleScheme
`StyleScheme` holds Style objects for container/labels; override to theme.
```python
from vvecon.qt.contrib.widgets.Input.StyleScheme import StyleScheme
custom = StyleScheme()
```

### Examples
```python
from vvecon.qt.contrib.widgets.Input import InputField
from vvecon.qt.enums import InputType

# Text input
name = InputField(name='Name', placeholder='Enter name')

# Integer input with +/- and bounds
age = InputField(name='Age', inType=InputType.NUMBER, step=1, minVal=0, maxVal=120)

# Float input
price = InputField(name='Price', inType=InputType.NUMBER, step=0.1, minVal=0.0)

# Search input (compact, no labels)
search = InputField(inType=InputType.SEARCH, placeholder='Search...')

# Date input with popup
date = InputField(name='Date', inType=InputType.DATE)
def on_date(s):
    print('selected', s)
date.dateSelected.connect(on_date)

# Validation
def not_empty(text: str, field_name: str, callback):
    if not text.strip():
        callback(f"{field_name} is required")
        return False
    return True
email = InputField(name='Email', validator=not_empty)
email.onEnter(lambda: print('valid value:', email.getValidatedValue()))
```


