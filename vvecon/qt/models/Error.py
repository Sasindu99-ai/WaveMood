from .DataModel import DataModel

__all__ = ['Error']


class Error(DataModel):
	status_code: int
	error: dict

	def getMessage(self, default: str = ''):
		if isinstance(self.error, list) and len(self.error) > 0 and isinstance(self.error[0], str):
			return self.error[0]
		return self.error.get('details', default)

	def __str__(self):
		return f'Error {self.status_code}: {self.getMessage()}'
