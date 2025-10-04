from typing import Type, Dict

__all__ = ['getAllAnnotations']


def getAllAnnotations(cls: Type) -> Dict[str, Type]:
    annotations = {}
    for base in cls.__mro__:
        if hasattr(base, '__annotations__'):
            annotations.update(base.__annotations__)
    return annotations
