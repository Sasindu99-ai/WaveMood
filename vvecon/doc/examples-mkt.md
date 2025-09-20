## Examples (Generic)

These examples use only `vvecon` so they can be published standalone.

### Minimal Window/View
```python
from PyQt6.QtWidgets import QApplication
from vvecon.qt.core import Window, View, WindowType

class Home(View):
    def __init__(self, parent: WindowType | None = None):
        super().__init__(parent, 'Home')
    def onCreate(self):
        # build layout, connect signals
        pass

class App(Window):
    def __init__(self):
        super().__init__()
        self.navigate(Home)
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    App()
    app.exec()
```

### Threaded task with callback
```python
from vvecon.qt.thread import threadPool

def compute(x):
    return x * 2

def on_done(result):
    print('result:', result)

threadPool.start(compute, 21, callback=on_done)
```

### Controller usage
```python
from vvecon.qt.api import Controller

class Health(Controller):
    api = ''

svc = Health()
data, status = svc.get('health')
```


