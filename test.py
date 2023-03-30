
import asyncio
import os
import time

from listeners import get_listeners
from listeners.abstract_listener import AbstractListener, MessageResult
from parsers import get_parser_for_url
from utils.url_utils import UrlUtils


async def main():
    '''
    Entry point of the app
    '''

    def handle(listener: AbstractListener, result: MessageResult) -> None:
        url = UrlUtils.find_url(result.message)
        if url:
            parsed_video = get_parser_for_url(result.message)[0].parse(result.message)
            listener.send(MessageResult(parsed_video.to_json(), result.extra))

    listeners = get_listeners(dict(os.environ))
    for listener in listeners:
        asyncio.ensure_future(listener.start(handler=handle))


    try:
        while 1:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print('bye')


if __name__ == "__main__":
    #raise SystemExit(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
