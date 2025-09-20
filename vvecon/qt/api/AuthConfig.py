
__all__ = ['AuthConfig']


class AuthConfig:
	refreshUrl: str

	def __init__(self, refreshUrl: str):
		self.refreshUrl = refreshUrl
