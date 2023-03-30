from typing_extensions import Final
import pytube
from urllib.parse import urlparse


from parsers.abstract_parser import AbstractParser, ParseResult


def fix_url(url:str) -> str:
    '''
    Adds support for yewtu.be and other invidious links
    That point to youtube videos
    '''
    parsed_url = urlparse(url)
    original_domain = parsed_url.netloc

    if original_domain.startswith('www.'):
        domain = original_domain[4:] # strip out www. part if present
    else:
        domain = original_domain

    if domain not in TubeParser.YOUTUBE_URLS:
        url = url.replace(original_domain, TubeParser.YOUTUBE_URLS[0])

    return url

class TubeParser(AbstractParser):
    '''
    Youtube Parser
    '''
    YOUTUBE_URLS: Final[list[str]] = ['youtube.com', 'youtu.be']

    @staticmethod
    def supported_domains() -> list[str]:
        return TubeParser.YOUTUBE_URLS + ['/watch?v=']

    @staticmethod
    def parse(url: str) -> ParseResult:
        '''
        Parse
        '''

        url = fix_url(url)

        p_t = pytube.YouTube(url)

        video = sorted(p_t.streaming_data['formats'], key=lambda x: x['bitrate'], reverse=True)[0]

        return ParseResult(video['url'], f"[{video['qualityLabel']}] {p_t.title}", video['mimeType'], p_t.thumbnail_url, True)
