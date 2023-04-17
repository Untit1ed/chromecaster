from urllib.parse import urlparse

from parsers import consts


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

    if domain not in consts.YOUTUBE_URLS:
        url = url.replace(original_domain, consts.YOUTUBE_URLS[0])

    return url
