## Contrib Styles

Styles are `vvecon.qt.util.Style` instances that produce QSS and support `.update(**overrides)` and `.apply(widget)`.

### Button (`vvecon.qt.contrib.styles.Button`)
Exports:
- `defaultButton`, `primaryButton`, `secondaryButton`, `successButton`, `warningButton`, `dangerButton`, `infoButton`, `lightButton`, `darkButton`, `noButton`, `transparentButton`

Usage:
```python
from vvecon.qt.contrib.styles.Button import primaryButton
btn.setStyleSheet(primaryButton.update(fontSize=14).qss)
```

### InputField (`vvecon.qt.contrib.styles.InputField`)
Exports style objects used by `InputField`:
- `label`, `container`, `searchContainer`, `lineEdit`, `errorContainer`, `successContainer`, `bottomLabel`, `errorBottomLabel`, `successBottomLabel`
- `lightInputField`: dict of light variants with same keys

Other style modules: `ComboBox`, `Label`, `Menu`, `Properties`, `ScrollArea`, `Tab`, `TableStyle` follow a similar pattern and can be applied to widgets with `.apply(widget)` or by using `.qss` on `setStyleSheet`.


