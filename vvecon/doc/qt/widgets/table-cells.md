## Table Cells

Cells subclass `BaseCell` and are used inside `Row`. Each implements:
- `setupCell(self)` to construct internal widgets
- `setValues(self, data)` to update from a datum

### BaseCell
`vvecon.qt.contrib.widgets.Table.BaseCell`

Constructor forwards any args/kwargs; they are stored and reused when cloning rows.
APIs:
- `setParent(row)` is called by `Row`
- `args()` and `kwargs()` return initial construction args
- `setStyleScheme(CellStyleScheme)` to override label/padding styles

### Cell
`vvecon.qt.contrib.widgets.Table.Cell`

```python
Cell(extract: Callable | None = None, reformat: str | None = None, textAlign=Qt.AlignCenter, padding=Padding(0), margin=Margin(0))
```

Data handling:
- If `extract` is provided, call it with `data` → `(args, kwargs)`; then format using `reformat`
- Without extract: accepts `(args, kwargs)` tuple, list/tuple, dict, or a scalar

### ActionCell
`vvecon.qt.contrib.widgets.Table.ActionCell`

```python
ActionCell(actions=[{ 'key': 'edit', 'label': 'Edit', 'icon': QIcon, 'enabled': True, 'visible': True, 'callback': lambda data: ... }])
```

Renders a menu on a three-dots button. Use `setValues({key: {enabled, visible, label, icon, shortcut}})` to update.

### ButtonCell
Renders inline `QPushButton`s.
```python
ButtonCell(actions=[{ 'icon': path_or_QIcon, 'action': lambda data: ... }, ...])
```

### CheckBoxCell
`CheckBoxCell(onCheckChanged=lambda state, cell, row: ...)`

`setValues(bool | {val: bool, disabled: bool})`. `getValue()` returns checked state.

### BooleanCell
Shows a green check or red close icon depending on boolean value.

### ComboBoxCell
```python
ComboBoxCell(items=[...], padding=Padding(...), margin=Margin(...), width=int, height=int, callback=lambda value, row: ...)
```
`setValues([{label, value, selected}...])` updates items and selection.

### InputCell
Wraps `InputField` as a cell.
```python
InputCell(name='Qty', inputType=InputType.NUMBER, step=1, minValue=0, maxValue=100, onTextChanged=lambda text, cell, row: ...)
```
APIs: `getValue()`, `disable(bool)`; `setValues(val | {val, disabled})`.


