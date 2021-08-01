import abc
from typing import Any


__all__ = ['IService', 'IQueryService', 'ICommandService']


class IService(metaclass=abc.ABCMeta):
    pass


class IQueryService(IService):
    pass


class ICommandService(IService):
    pass
