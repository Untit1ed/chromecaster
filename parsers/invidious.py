import pytube
import requests

from parsers import consts, utils
from parsers.abstract_parser import AbstractParser, ParseResult


class InvidiousParser(AbstractParser):
    '''
    Invidious Parser
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

        # if p_t.vid_info['playabilityStatus']['status'] != 'LOGIN_REQUIRED':
        #    return None

        stream_url = InvidiousParser.get_stream_from_id(p_t.video_id)

        return ParseResult(
            stream_url,
            url,
            f"[Invidious] {p_t.title}",
            'video/mp4',
            p_t.thumbnail_url,
            p_t.length,
            True,
            False,
            [("Channel Url", p_t.channel_url)])

    @staticmethod
    def get_stream_from_id(youtube_id: int) -> str:
        '''
        Gets a youtube video stream from an invidious page
        '''
        stream_check_urls = [
            f'https://{domain}/latest_version?id={youtube_id}&itag=22' for domain in consts.INVIDIOUS_URLS
        ]

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "DNT": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

        for stream_check_url in stream_check_urls:
            error = None
            try:
                response = requests.get(stream_check_url, headers=headers, allow_redirects=False, timeout=5)
                if response.status_code == 302:  # redirect
                    return response.next.url
            except Exception as err:
                error = err

        if error:
            raise error

        return None
