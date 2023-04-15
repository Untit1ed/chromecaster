from dataclasses import dataclass
from urllib.parse import urlparse

import pytube
from pytube.exceptions import LiveStreamError
from typing_extensions import Final

from parsers.abstract_parser import AbstractParser, ParseResult


def fix_url(url: str) -> str:
    '''
    Adds support for yewtu.be and other invidious links that point to youtube videos
    '''
    parsed_url = urlparse(url)
    original_domain = parsed_url.netloc

    if original_domain.startswith('www.'):
        domain = original_domain[4:]  # strip out www. part if present
    else:
        domain = original_domain

    if domain not in TubeParser.YOUTUBE_URLS:
        url = url.replace(original_domain, TubeParser.YOUTUBE_URLS[0])

    return url


@dataclass
class Video():
    """
    Class to hold pytube video info
    """
    url: str = ''
    quality: str = ''
    mime_type: str = ''
    bitrate: int = 0


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
        videos = None
        try:
            p_t.check_availability()

            # pass to the invidious parser if the vid is age restricted
            if p_t.vid_info['playabilityStatus']['status'] == 'LOGIN_REQUIRED':
                return None
        except LiveStreamError:
            stream_url = p_t.streaming_data['hlsManifestUrl']
            videos = [Video(stream_url, 'Live', 'application/x-mpegUrl', 0)]

        if not videos:
            try:
                videos = [Video(item['url'], item['qualityLabel'], item['mimeType'], item['bitrate'])
                          for item in p_t.streaming_data['formats']]
            except Exception:
                videos = [Video(item.url, item.resolution, item.mime_type, item.bitrate)
                          for item in p_t.fmt_streams]

        video = sorted(videos, key=lambda x: x.bitrate, reverse=True)[0]

        return ParseResult(
            video.url,
            url,
            f"[{video.quality}] {p_t.title}",
            video.mime_type,
            p_t.thumbnail_url,
            p_t.length,
            True,
            video.quality == 'Live')
