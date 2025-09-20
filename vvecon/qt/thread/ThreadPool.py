from typing import TypeVar, Dict, Callable, Optional
from PyQt6.QtCore import QThreadPool
from vvecon.qt.logger import logger

from .Worker import Worker

T = TypeVar('T', bound='ThreadPool')

__all__ = ['threadPool']


class ThreadPool:
    _instance: Optional[T] = None
    threadPool: QThreadPool = QThreadPool()
    _tasks: Dict[int, Worker] = dict()  # Use id(func) as key

    @classmethod
    def getInstance(cls) -> T:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if ThreadPool._instance is not None:
            raise Exception("Use getInstance() to access the ThreadPool instance.")
        ThreadPool._instance = self

    def add(self, func: Callable, delay: float = 0):
        func_id = id(func)
        if func_id in self._tasks:
            return
        runnable = Worker(func, delay)
        self._tasks[func_id] = runnable

    def start(
        self,
        func: Callable,
        *args,
        delay: float = 0,
        callback: Optional[Callable] = None,
        retry: bool = True,
        **kwargs
    ):
        func_id = id(func)
        try:
            self.add(func, delay)
            worker = self._tasks[func_id]
            worker.setData(*args, **kwargs)
            if callback:
                try:
                    worker.signals.finished.disconnect()
                except TypeError:
                    pass
                worker.signals.finished.connect(callback)
            self.threadPool.start(worker)
        except RuntimeError as e:
            logger.error(f"RuntimeError in ThreadPool.start: {e}")
            self._tasks.pop(func_id, None)
            if retry:
                self.start(func, *args, delay=delay, callback=callback, retry=False, **kwargs)

    def stop(self, func: Callable):
        func_id = id(func)
        if func_id in self._tasks:
            runnable = self._tasks.pop(func_id, None)
            if runnable:
                runnable.stop()

    def stopAll(self):
        try:
            for func_id, runnable in list(self._tasks.items()):
                runnable.stop()
                if hasattr(self.threadPool, 'cancel'):
                    self.threadPool.cancel(runnable)
                del self._tasks[func_id]
        except RuntimeError as e:
            logger.error(f"Error in ThreadPool.stopAll: {e}")

    def clearAll(self):
        try:
            self.stopAll()
            self.threadPool.clear()
        except RuntimeError as e:
            logger.error(f"Error in ThreadPool.clearAll: {e}")


threadPool = ThreadPool.getInstance()
