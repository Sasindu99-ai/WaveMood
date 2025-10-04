## Table

### Header
`vvecon.qt.contrib.widgets.Table.Header`

```python
Header(name: str, width: int | NotImplemented = NotImplemented, stretch: int | NotImplemented = 1, headerType: int = Header.SINGLE_LINE)
```

Width modes inferred:
- `FIXED` if `width` set; `STRETCH` if `stretch` set; else `PREFERRED` (interactive)

### Row
`vvecon.qt.contrib.widgets.Table.Row`

Holds a list of cell widgets and updates them from data.
Key APIs:
- `setIndex(index)` inserts cell widgets into table
- `setExtractFunction(callable)` maps data → list for cells
- `new(index, data)` clones a row instance and populates
- `update(data)` updates cell widgets

### TableWidget
`vvecon.qt.contrib.widgets.Table.TableWidget`

Constructor:
```python
TableWidget(parent=None, headers: list[Header] | None = None, primaryField: str = 'id')
```

APIs:
- `setHeaders(headers)` / `updateTableHeaders()`
- `setRowWidget(Row)` and `setExtractFunction(callable)`
- `updateContent(iterable)` inserts/updates rows by `primaryField`
- `getRows()`, `getSelectedRowData()`, `selectNextRow()`
- `resizeColumnsToContents()`
- Infinite-scroll helpers: `setVerticalScrollbarHitBottomCallback(callback)`

Example:
```python
headers = [Header('Name', stretch=2), Header('Status', width=120)]
table = TableWidget(headers=headers, primaryField='id')

from vvecon.qt.contrib.widgets.Table import Row, Cell, BooleanCell
row = Row(table, cells=[Cell(reformat='{name}'), BooleanCell()])
table.setRowWidget(row)

def extract(model):
    return ([model.name], {})
table.setExtractFunction(extract)

table.updateContent([model1, model2])
```


