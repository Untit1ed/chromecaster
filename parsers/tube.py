import pytube

from parsers.abstract_parser import AbstractParser, ParseResult


class TubeParser(AbstractParser):
    '''
    Youtube Parser
    '''


    @staticmethod
    def supported_domains() -> list[str]:
        return ['youtube.com', 'youtu.be']

    @staticmethod
    def parse(url: str) -> ParseResult:
        '''
        Parse
        '''

        p_t = pytube.YouTube(url)

        video = sorted(p_t.streaming_data['formats'], key=lambda x: x['bitrate'], reverse=True)[0]

        return ParseResult(video['url'], f"[{video['qualityLabel']}] {p_t.title}", video['mimeType'], p_t.thumbnail_url)
