import enum

__all__ = ['InputType']


class InputType(enum.Enum):
    TEXT = 'Text'
    NUMBER = 'Number'
    DATE = 'Date'
    SEARCH = 'Search'
