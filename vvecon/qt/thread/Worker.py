from typing import Callable, Dict
from uuid import uuid4

from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QTimer
from vvecon.qt.logger import logger


class WorkerSignals(QObject):
	finished = pyqtSignal(object)  # Emitted when the task finishes, passing the result or None


class Worker(QRunnable):
	def __init__(self, func: Callable, delay: float = 0):
		super().__init__()
		self.pk = uuid4()  # Unique identifier for this worker instance
		self._func = func
		self._delay = delay  # Delay between executions in seconds
		self._args = ()
		self._kwargs: Dict = {}
		self.signals = WorkerSignals()
		self._isRunning = False
		self._timer = QTimer()  # Timer to manage periodic execution
		self._timer.setInterval(int(self._delay * 1000))  # Set interval in milliseconds
		self._timer.timeout.connect(self._run_once)

	def setData(self, *args, **kwargs):
		"""
		Sets the data to be passed to the callable function.
		"""
		self._args = args
		self._kwargs = kwargs

	def run(self):
		"""
		Starts the worker execution using the QTimer.
		"""
		if self._isRunning:
			return

		self._isRunning = True

		if self._delay > 0:
			# Start periodic execution
			self._timer.start()
		else:
			# Single execution without delay
			self._run_once()

	def _run_once(self):
		"""
		Executes the callable function once and emits the result.
		"""
		if not self._isRunning:
			return

		try:
			result = self._func(*self._args, **self._kwargs)
			self.signals.finished.emit(result)
		except Exception as e:
			print(e)
			self.signals.finished.emit(None)

		if self._delay <= 0:  # Stop after one execution if no delay
			self.stop()

	def stop(self):
		"""
		Stops the worker and the QTimer safely.
		"""
		try:
			if not self._isRunning:
				return

			self._isRunning = False
			self._timer.stop()  # Stop the timer
		except RuntimeError as e:
			logger.error(f"Worker stop error: {e}")
