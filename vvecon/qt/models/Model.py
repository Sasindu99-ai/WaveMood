from datetime import datetime
from typing import Optional


from .ModelAbstract import ModelAbstract

__all__ = ['Model']


class Model(ModelAbstract):
    """
    Model(ModelAbstract)

    Description:
        This is a base class for all models. This class is used to create models for the application. This class
        provides the basic structure for all models. This class provides the basic structure for all models. This

    Attributes:
        id: Optional[int] = NotImplemented
        created_at: Optional[datetime] = NotImplemented
        updated_at: Optional[datetime] = NotImplemented
        deleted_at: Optional[datetime] = None
    """
    id: Optional[int] = NotImplemented
    created_at: Optional[datetime] = NotImplemented
    updated_at: Optional[datetime] = NotImplemented
    deleted_at: Optional[datetime] = None

    # def __new__(cls, *args, **kwargs):
    #     ic(cls.__name__, args, kwargs)
    #     return super().__new__(cls, *args, **kwargs)
