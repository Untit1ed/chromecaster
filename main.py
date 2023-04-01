import asyncio
import os
import time

from caster.caster import Caster
from pychromecast.error import NotConnected
from listeners import get_listeners
from listeners.abstract_listener import AbstractListener, MessageResult
from parsers import get_parser_for_url
from utils.string_utils import StringUtils


def main():
    '''
    Entry point of the app
    '''

    with Caster(os.environ.get('CHROMECAST_DEVICE')) as caster:
        caster.connect()

        caster.start_debug_thread()

        def on_callback(listener: AbstractListener, result: MessageResult) -> None:
            url = StringUtils.find_url(result.message)
            number = StringUtils.get_float(result.message)
            seconds = StringUtils.time_str_to_seconds(result.message)
            skip_seconds = StringUtils.extract_number(result.message)

            # video url was provided
            if url:
                try:
                    parsed_video = get_parser_for_url(url)[0].parse(url)
                    caster.play(parsed_video)
                    listener.send(MessageResult(caster.now_playing(parsed_video), result.extra))
                except NotConnected:
                    caster.play(parsed_video)
                    listener.send(MessageResult(caster.now_playing(parsed_video), result.extra))
                except Exception as exception:
                    listener.send(MessageResult(str(exception), result.extra))
            # time code was provided
            elif seconds:
                caster.seek(seconds)
            # FF or rewind
            elif skip_seconds:
                caster.skip(skip_seconds)
            # volume or play rate
            elif number >= 0:
                if 0.5 <= number <= 2:  # 0.5 - 2 - play rate
                    caster.set_playback_rate(number)
                else:  # 0 - 100 - volume
                    caster.set_volume(number)

        for listener in get_listeners(dict(os.environ)):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(listener.start(handler=on_callback))

        try:
            while 1:
                time.sleep(1)
        except KeyboardInterrupt:
            print('bye')


if __name__ == "__main__":
    raise SystemExit(main())
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
