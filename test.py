
import time

import config
from listeners import get_listeners
from parsers import get_parser_for_url


def main():
    '''
    Entry point of the app
    '''

    def handle(message: str) -> None:
        if message.startswith('https://'):
            parsed_video = get_parser_for_url(message)[0].parse(message)
            listener.send(parsed_video.to_json())

    for listener in get_listeners(config):
        listener.start(handler = handle)

    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print('bye')


if __name__ == "__main__":
    raise SystemExit(main())
