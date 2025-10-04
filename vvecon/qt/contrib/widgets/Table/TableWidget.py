from typing import Callable, Dict, List, Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHeaderView, QSizePolicy, QTableWidget

from vvecon.qt.contrib.styles import TableStyle
from vvecon.qt.enums import SizeType

from .Header import Header
from .Row import Row

__all__ = ['TableWidget']


class TableWidget(QTableWidget):
	_headers: List[Header]
	_row: Optional[Row] = None
	_extractor: Optional[Callable] = None
	_onVerticalScrollbarHitBottomCallback: Optional[Callable] = None
	rowSelected = pyqtSignal(object)

	scrolled = pyqtSignal()
	_primaryField: str = 'id'

	def __init__(self, parent=None, headers: Optional[List[Header]] = None, primaryField: str = 'id'):
		super(TableWidget, self).__init__(parent)

		if headers is None:
			headers = []
		self._primaryField = primaryField
		self._headers = headers
		self._rowWidgets: Dict[int, Row] = dict()

		self.updateTableHeaders()
		self.verticalHeader().setVisible(False)

		TableStyle.table.apply(self)
		self.setShowGrid(False)
		self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
		self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

	def setHeaders(self, headers: List[Header]):
		self._headers = headers
		self.updateTableHeaders()

	def updateTableHeaders(self):
		self.setColumnCount(len(self._headers))
		self.setHorizontalHeaderLabels([header.name for header in self._headers])
		for col, header in enumerate(self._headers):
			self.setHeaderWidth(col, header, self.calculateTotalStretch(self._headers, self.width()))

	@staticmethod
	def calculateTotalStretch(headers: List[Header], tableWidth: int) -> float:
		totalFixedWidth = sum(
			header.width
			for header in headers
			if header.widthType == SizeType.FIXED and header.width
		)
		availableWidth = max(tableWidth - totalFixedWidth, 0)
		totalStretch: float = 0
		for header in headers:
			if header.widthType == SizeType.STRETCH and header.stretch:
				adjustedStretch = availableWidth * (
					header.stretch / sum(h.stretch or 0 for h in headers if h.widthType == SizeType.STRETCH)
				)
				totalStretch += adjustedStretch
		return totalStretch

	def setHeaderWidth(self, col: int, header: Header, totalStretch: float):
		if header.widthType == SizeType.FIXED:
			self.setColumnWidth(col, header.width)
		elif header.widthType == SizeType.STRETCH:
			if header.stretch == 1:
				self.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
			elif totalStretch > 1 and isinstance(header.stretch, int):
				stretchFactor = header.stretch / totalStretch
				self.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
				self.setColumnWidth(col, int(self.width() * stretchFactor))
		elif header.widthType == SizeType.PREFERRED:
			self.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		totalStretch = sum(header.stretch if isinstance(header.stretch, int) else 0 for header in self._headers)
		for col, header in enumerate(self._headers):
			if header.widthType == SizeType.STRETCH and totalStretch > 1:
				stretch_factor = header.stretch / totalStretch
				self.setColumnWidth(col, int(self.width() * stretch_factor))

	def clear(self):
		self.clearContents()
		self.setRowCount(0)
		self._rowWidgets = dict()

	def setRowWidget(self, widget: Row):
		self._row = widget
		if self._extractor:
			self._row.setExtractFunction(self._extractor)

	def setExtractFunction(self, extract: Callable):
		self._extractor = extract
		if isinstance(self._row, Row):
			self._row.setExtractFunction(self._extractor)

	def updateContent(self, data):
		for datum in data:
			if getattr(datum, self._primaryField) in self._rowWidgets.keys():
				try:
					self._rowWidgets[getattr(datum, self._primaryField)].update(datum)
				except RuntimeError:
					rowCount = self.rowCount()
					self.insertRow(rowCount)
					self._rowWidgets[getattr(datum, self._primaryField)] = self._row.new(rowCount, datum)
			else:
				rowCount = self.rowCount()
				self.insertRow(rowCount)
				self._rowWidgets[getattr(datum, self._primaryField)] = self._row.new(rowCount, datum)

	def getRows(self):
		return self._rowWidgets

	def getSelectedRowData(self):
		indexes = self.selectedIndexes()
		if not indexes:
			return None

		selectedRow = indexes[0].row()

		for rowWidget in self._rowWidgets.values():
			if rowWidget.index == selectedRow:
				return rowWidget.data

		return None

	def selectNextRow(self):
		indexes = self.selectedIndexes()
		if not indexes:
			return False
		currentRow = indexes[0].row()
		if currentRow + 1 >= self.rowCount():
			return False

		self.selectRow(currentRow + 1)
		return True

	def wheelEvent(self, a0):
		self.scrolled.emit()
		if not self.verticalScrollBar().isVisible() and self._onVerticalScrollbarHitBottomCallback:
			self._onVerticalScrollbarHitBottomCallback()
		super().wheelEvent(a0)

	def resizeColumnsToContents(self):
		for col, header in enumerate(self._headers):
			if header.widthType == SizeType.PREFERRED:
				self.resizeColumnToContents(col)

	def setVerticalScrollbarHitBottomCallback(self, callback: Callable):
		self._onVerticalScrollbarHitBottomCallback = callback
		self.verticalScrollBar().setEnabled(True)
		self.verticalScrollBar().valueChanged.connect(self.onVerticalScrollbarHitBottom)
		self.scrolled.connect(self.onVerticalScrollbarHitBottom)

	def onVerticalScrollbarHitBottom(self, value: Optional[int] = None):
		scrollBar = self.verticalScrollBar()
		if (
			(value is not None and scrollBar.maximum() - value <= 10) or (scrollBar.isHidden())
			and self._onVerticalScrollbarHitBottomCallback
		):
			self._onVerticalScrollbarHitBottomCallback()

	def removeRowId(self, rowId: int):
		if rowId in self._rowWidgets:
			self.removeRow(self._rowWidgets[rowId].index)
			del self._rowWidgets[rowId]
			self.resizeColumnsToContents()
