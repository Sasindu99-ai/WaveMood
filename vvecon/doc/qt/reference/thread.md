## Thread

### ThreadPool (`vvecon.qt.thread.ThreadPool` and `threadPool` singleton)
```python
threadPool.start(func: Callable, *args, delay: float = 0, callback: Callable | None = None, retry: bool = True, **kwargs) -> None
threadPool.stop(func: Callable) -> None
threadPool.stopAll() -> None
threadPool.clearAll() -> None
```

The worker emits `finished(result)`; when `callback` provided, it is connected to this signal.

### Worker (`vvecon.qt.thread.Worker`)
Internal `QRunnable` wrapper with optional periodic execution via `QTimer` when `delay > 0`.


