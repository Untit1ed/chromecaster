from dataclasses import dataclass

import pytube
from pytube.exceptions import LiveStreamError

from parsers import consts, utils
from parsers.abstract_parser import AbstractParser, ParseResult
from parsers.invidious import InvidiousParser


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
    @staticmethod
    def supported_domains() -> list[str]:
        return consts.YOUTUBE_URLS + ['/watch?v=']

    @staticmethod
    def parse(url: str) -> ParseResult:
        '''
        Parse
        '''

        youtube_url = utils.fix_url(url)

        p_t = pytube.YouTube(youtube_url)
        videos = None
        try:
            p_t.check_availability()

            # pass to the invidious parser if the vid is age restricted
            if p_t.vid_info['playabilityStatus']['status'] == 'LOGIN_REQUIRED':
                stream_url = InvidiousParser.get_stream_from_id(p_t.video_id)
                videos = [Video(stream_url, 'LOGIN_REQUIRED', 'video/mp4', 0)]
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
            video.quality == 'Live',
            [("Channel Url", p_t.channel_url)])
