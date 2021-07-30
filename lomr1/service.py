import abc
from typing import TypeVar


__all__ = [
    'IServiceRequest', 'IServiceResponse', 'IServiceHandler',
    'IRequest', 'IResponse'
]


class IServiceRequest(metaclass=abc.ABCMeta):
    pass


class IServiceResponse(metaclass=abc.ABCMeta):
    pass


IRequest = TypeVar('IRequest', bound=IServiceRequest)
IResponse = TypeVar('IResponse', bound=IServiceResponse)


class IServiceHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, request: IRequest) -> IResponse:
        pass
