## Logger

### Logger (`vvecon.qt.logger.Logger`) and `logger` instance

Methods:
```python
setUserName(userName: str) -> None
setConfig(config: dict[str,str]) -> None
setLevel(level: int | str) -> None
setFormat(logFormat: str) -> None
setDestination(filePath: str) -> None  # add file handler

debug(msg, **kwargs) -> None
info(msg, **kwargs) -> None
warning(msg, **kwargs) -> None
error(msg, **kwargs) -> None
critical(msg, **kwargs) -> None
```

Messages are formatted with `[filename:lineno] LEVEL: | user - message`.


