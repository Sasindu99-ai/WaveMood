from typing import Optional

from .ModelAbstract import ModelAbstract


class ModelRequest(ModelAbstract):
    """
    ModelRequest(ModelAbstract)

    Description:
        This is a base class for all requests. This class is used to create requests for the application. This class
        provides the basic structure for all requests. This class provides the basic structure for all requests.

    Arguments:
        id: Optional[int] = NotImplemented
    """
    id: Optional[int] = NotImplemented
