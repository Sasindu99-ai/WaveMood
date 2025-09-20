from PyQt6.QtCore import pyqtSignal

from .SignalPool import SignalPool

__all__ = ['window']


class Window(SignalPool):
    newViewAdded = pyqtSignal(object)
    tabRemoved = pyqtSignal(object)


window = Window()
