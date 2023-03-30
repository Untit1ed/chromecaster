from abc import ABC, abstractmethod
from typing import Callable, Optional

from attr import dataclass


@dataclass
class MessageResult:
    """
    Class to hold listener's message result.

    Attributes:
        message (str): The message returned by the listener.
        extra (object, optional): Optional extra data returned by the listener. Defaults to None.
    """
    message: str
    extra: Optional[object] = None

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
