from abc import ABC, abstractmethod
from typing import Callable


class AbstractListener(ABC):
    '''
    Abstract listener
    '''

    @abstractmethod
    def __init__(self, config) -> None:
        pass

    @abstractmethod
    def start(self, handler: Callable[[str], None]) -> None:
        '''
        Listen to a message, call handler on message
        '''
