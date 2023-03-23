import asyncio
import os
import time

from caster import Caster
from listeners import get_listeners
from listeners.abstract_listener import AbstractListener, MessageResult
from parsers import get_parser_for_url
from utils.url_utils import UrlUtils


def main():
    '''
    Entry point of the app
    '''

    with Caster(os.environ.get('CHROMECAST_DEVICE')) as caster:
        caster.connect()
        caster.set_playback_rate(1.2)
        caster.start_debug_thread()

        def handle(listener: AbstractListener, result: MessageResult) -> None:
            url = UrlUtils.find_url(result.message)
            if url:
                parsed_video = get_parser_for_url(result.message)[0].parse(result.message)
                caster.play(parsed_video)
                caster.set_playback_rate(1.2)
                listener.send(MessageResult(parsed_video.to_json(), result.extra))

        for listener in get_listeners(dict(os.environ)):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(listener.start(handler=handle))


        try:
            while 1:
                time.sleep(1)
        except KeyboardInterrupt:
            print('bye')


if __name__ == "__main__":
    raise SystemExit(main())
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
