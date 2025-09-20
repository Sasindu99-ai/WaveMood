## Threading and Signals

### Thread pool
`vvecon.qt.thread.threadPool` is a singleton over `QThreadPool` with a simple API.

Run a function in the pool, optionally periodically via `delay` and with a completion callback:
```python
from vvecon.qt.thread import threadPool

def fetch_data(query: str):
    # long-running work
    return result

def on_done(result):
    if result is None:
        return
    # update UI here (runs in main thread via signal)

threadPool.start(fetch_data, 'hello', callback=on_done)
```

Stop a specific task or all tasks:
```python
threadPool.stop(fetch_data)
threadPool.stopAll()
```

### Signals
Use `vvecon.qt.signals.SignalPool` to group app-wide signals. Built-ins include window-level signals:
```python
from vvecon.qt.signals import window

window.newViewAdded.connect(lambda view: ...)
window.tabRemoved.connect(lambda view: ...)
```

Create your own pools by subclassing `SignalPool` and declaring `pyqtSignal` attributes.


