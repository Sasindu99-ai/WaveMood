__all__ = ['ParseError']


class ParseError(Exception):

	def __init__(self, message, line, column):
		self.message = message
		self.line = line
		self.column = column

	def __str__(self):
		try:
			return 'Parse error at line %d, column %d: %s' % (
				self.line, self.column, self.message)
		except TypeError:
			return 'Parse error: %s' % self.message
