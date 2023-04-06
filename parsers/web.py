from bs4 import BeautifulSoup
from selenium import webdriver

from parsers.abstract_parser import AbstractParser, ParseResult


class WebParser(AbstractParser):
    '''
    Finds videos on a web page
    '''

    @staticmethod
    def supported_domains() -> list[str]:
        return ['rumble.com', 'vkplay.live']

    @staticmethod
    def parse(url: str) -> ParseResult:
        '''
        Parse
        '''

        # Start a headless Chrome browser using Selenium
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(options=options)

        # Load a web page that uses JavaScript to build the DOM
        browser.get(url)

        # Extract the HTML content of the page
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.string
        video_url = ''
        thumbnail_url = ''

        # find all videos on the webpage
        videos = soup.find_all('video')
        for video in videos:
            src = video.get('src')
            thumbnail_url = video.get('poster')

            if src:
                video_url = src
                print(video_url)
            else:
                children = video.findChildren('source')
                for child in children:
                    src = child.get('src')
                    if src:
                        video_url = src
                        print(video_url)

        return ParseResult(video_url, url, title, 'video/mp4', thumbnail_url)
