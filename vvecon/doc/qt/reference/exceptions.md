## Exceptions

### ParseError (`vvecon.qt.exceptions.ParseError`)
```python
ParseError(message: str, line: int, column: int)
str(ParseError) -> 'Parse error at line X, column Y: message'
```

Raised by model parsing when type conversion fails in `ModelAbstract._convert`.


