## Getting Started

This project uses vvecon (PyQt6) for a simple Window/View architecture.

### Requirements
- Python 3.10+
- PyQt6
- SQLAlchemy (optional, for DB helper)

Install deps (example):
```bash
pip install -r requirements.txt  # or use your env manager
```

### Run the MKT app
```bash
python main.py
```

The entry point sets up environment, QApplication, fonts, and window icon, then constructs the main window:

```python
# main.py (excerpt)
from env import env
from PyQt6.QtWidgets import QApplication

env.init()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from vvecon.qt.res import Icons

    app.setWindowIcon(Icons.settings_applications)
    from WaveMood import WaveMood

    WaveMood()
    sys.exit(app.exec())
```

The main window is a subclass of `vvecon.qt.core.Window` and navigates to an initial `View`:
```python
# MKT.py (excerpt)
from vvecon.qt.core import Window

class MKT(Window):
    def __init__(self):
        super().__init__(row=4, column=2)
        self.setWindowTitle('MKT')
        self.setupTopBar()
        from views import HomeView
        self.navigate(HomeView)
        self.show()
```

### Minimal skeleton for a new app
```python
from PyQt6.QtWidgets import QApplication
from vvecon.qt.core import Window, View, WindowType

class Home(View):
    def __init__(self, parent: WindowType | None = None):
        super().__init__(parent, 'Home')
    def onCreate(self):
        ...

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

### Icon explorer
```bash
python -m vvecon qt icons
```


