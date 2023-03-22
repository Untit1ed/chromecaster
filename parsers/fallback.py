

from parsers.abstract_parser import AbstractParser, ParseResult


class FallbackParser(AbstractParser):
    '''
    Doesn't find anything, returns the url that was passed to it
    '''

    @staticmethod
    def supported_domains() -> list[str]:
        return []

    @staticmethod
    def parse(url: str) -> ParseResult:
        return ParseResult(url, 'Default Video', 'video/mp4')
