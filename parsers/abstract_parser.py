import json
from abc import ABC, abstractmethod

from attr import dataclass


@dataclass
class ParseResult:
    """
    Class to hold parser's result.
    """
    url: str
    title: str
    mime_type: str
    thumbnail_url: str = None
    duration: float = None
    support_resume: bool = False
    is_live: bool = False


    def to_json(self) -> str:
        '''
        Serializes class to JSON string
        '''
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class AbstractParser(ABC):
    '''
    Abstract parser
    '''


    @staticmethod
    @abstractmethod
    def supported_domains() -> list[str]:
        '''
        Returns a list of supported domains
        '''

    @staticmethod
    @abstractmethod
    def parse(url: str) -> ParseResult:
        '''
        Gets video info from the url
        '''
