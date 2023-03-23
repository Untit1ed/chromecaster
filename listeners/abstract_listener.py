from abc import ABC, abstractmethod
from typing import Callable

from attr import dataclass


@dataclass
class MessageResult:
    """
    Class to hold listener's message result.
    """
    message: str
    extra: object = None

class AbstractListener(ABC):
    '''
    Abstract listener
    '''

    @abstractmethod
    def __init__(self, config) -> None:
        pass

    @abstractmethod
    def send(self, message: str) -> None:
        '''
        Send message back to the listener
        '''

    @abstractmethod
    async def start(self, handler: Callable[[str, object, MessageResult], None]) -> None:
        '''
        Listen to a message, call handler on message
        '''
