from urllib.parse import urlparse

import pytube
from pytube.exceptions import LiveStreamError
from typing_extensions import Final

from parsers.abstract_parser import AbstractParser, ParseResult


def fix_url(url:str) -> str:
    '''
    Adds support for yewtu.be and other invidious links that point to youtube videos
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

        youtube_url = fix_url(url)

        p_t = pytube.YouTube(youtube_url)
        videos = []
        video = None
        try:
            p_t.check_availability()
        except LiveStreamError:
            stream_url = p_t.streaming_data['hlsManifestUrl']
            video = {"url": stream_url, "qualityLabel": 'Live', "mimeType": 'application/x-mpegURL', 'bitrate': 0}
            videos.append(video)
            # videos = p_t.streaming_data['adaptiveFormats']

        if not videos:
            try:
                videos = p_t.streaming_data['formats']
            except Exception:
                videos = [{"url": item.url, "qualityLabel": item.resolution,
                           "mimeType": item.mime_type, 'bitrate': item.bitrate} for item in p_t.fmt_streams]
        video = sorted(videos, key=lambda x: x['bitrate'], reverse=True)[0]

        return ParseResult(
            video['url'],
            url,
            f"[{video['qualityLabel']}] {p_t.title}",
            video['mimeType'],
            p_t.thumbnail_url,
            p_t.length,
            True,
            video['qualityLabel'] == 'Live')
