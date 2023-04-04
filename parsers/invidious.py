import pytube
import requests

from parsers.abstract_parser import AbstractParser, ParseResult
from parsers.tube import TubeParser, fix_url


class InvidiousParser(AbstractParser):
    '''
    Invidious Parser
    '''

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

        if p_t.vid_info['playabilityStatus']['status'] != 'LOGIN_REQUIRED':
            return None

        url = f'https://yewtu.be/latest_version?id={p_t.video_id}&itag=22'

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
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=5)
        if response.status_code == 302:  # redirect
            url = response.next.url

        return ParseResult(
            url,
            f"[Invidious] {p_t.title}",
            'video/mp4',
            p_t.thumbnail_url,
            p_t.length,
            True,
            False)