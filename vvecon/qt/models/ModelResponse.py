from datetime import datetime
from typing import Optional

from .ModelAbstract import ModelAbstract


class ModelResponse(ModelAbstract):
	"""
	ModelResponse(ModelAbstract)

	Description:
		This is a base class for all responses. This class is used to create responses for the application. This class
		provides the basic structure for all responses. This class provides the basic structure for all responses.

	Arguments:
		  id: Optional[int] = NotImplemented
	"""
	id: Optional[int] = NotImplemented
	created_at: Optional[datetime] = NotImplemented
	updated_at: Optional[datetime] = NotImplemented
	deleted_at: Optional[datetime] = NotImplemented
