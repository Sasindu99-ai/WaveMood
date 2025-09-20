from typing import Any, Callable, List, Optional, Type


from vvecon.qt.models import ModelAbstract

__all__ = ['Row']


class Row:
	_parent = None
	_cells: List
	_index: Optional[int] = None
	_data: Optional[Any] = None
	_extractor: Optional[Callable] = None

	def __init__(self, parent, cells: List):
		super(Row, self).__init__()

		self._parent = parent
		self._cells = cells

		for column in range(len(self._cells)):
			self._cells[column].setParent(self)

	@property
	def data(self):
		return self._data

	def setIndex(self, index: int):
		if self._index:
			self._parent.removeRow(self._index)
		self._index = index
		for column in range(len(self._cells)):
			self._parent.setCellWidget(self._index, column, self._cells[column])

	def setExtractFunction(self, extract: Callable):
		self._extractor = extract

	def new(self, index: int, data: Type[ModelAbstract.T]):
		newCells = [cell.__class__(*cell.args(), **cell.kwargs()) for cell in self._cells]
		row = self.__class__(self._parent, cells=newCells)
		if self._extractor:
			row.setExtractFunction(self._extractor)
		row.setIndex(index)
		row.update(data)
		return row

	def update(self, data: Type[ModelAbstract.T]):
		if self._data and getattr(self._data, 'id', None) != getattr(data, 'id', NotImplemented):
			raise ValueError('Data ID does not match')
		self._data = data
		if self._extractor:
			extractedData: List = self._extractor(data)
			for index, cell in enumerate(self._cells):
				cell.setValues(extractedData[index])
			return

		for cell in self._cells:
			cell.setValues(self._data)

	@property
	def index(self):
		return self._index

	@property
	def cells(self):
		return self._cells
