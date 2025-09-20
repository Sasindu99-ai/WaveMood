## Models

### ModelAbstract (`vvecon.qt.models.ModelAbstract`)

Constructor:
```python
ModelAbstract(**kwargs)
```
Converts values to annotated types; supports nested lists/dicts, `datetime`, `Enum`, and optionals. Raises `ParseError` on type issues.

Class methods:
```python
fromList(data: list[dict]) -> list[T]
fromDict(data: dict) -> T
```

Instance methods:
```python
json() -> dict
```

### Model / ModelRequest / ModelResponse
- `Model`: adds common fields `id`, `created_at`, `updated_at`, `deleted_at`
- `ModelRequest`: for request payloads; `id`
- `ModelResponse`: for responses; adds timestamps

### Error (`vvecon.qt.models.Error`)
Fields: `status_code: int`, `error: dict`
Methods:
```python
getMessage(default: str = '') -> str
__str__() -> str
```


