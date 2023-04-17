from abc import ABC, abstractmethod
from typing import Callable, Optional

from attr import dataclass

from parsers.abstract_parser import ParseResult


@dataclass
class MessageResult:
    """
    Class to hold listener's message result.

    Attributes:
        text (str): The message returned by the listener.
        extra (object, optional): Optional extra data returned by the listener. Defaults to None.
    """
    text: str
    extra: Optional[object] = None
    options: Optional[list[str]] = None
    video: Optional[ParseResult] = None

class AbstractListener(ABC):
    '''
    Abstract listener
    '''

    @abstractmethod
    def __init__(self, config) -> None:
        pass

    @abstractmethod
    def send(self, message: MessageResult) -> None:
        '''
        Send message back to the listener
        '''

    @abstractmethod
    async def start(self, handler: Callable[[str, object, MessageResult], None]) -> None:
        '''
        Listen to a message, call handler on message
        '''
