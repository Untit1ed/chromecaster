import asyncio
import os
import time

from dotenv import load_dotenv
from pychromecast.error import NotConnected

from caster.caster import Caster
from listeners import get_listeners
from listeners.abstract_listener import AbstractListener, MessageResult
from parsers import get_parser_for_url
from utils.string_utils import StringUtils


def main():
    '''
    Entry point of the app
    '''

    load_dotenv()

    with Caster(os.environ.get('CHROMECAST_DEVICE')) as caster:
        caster.connect()

        caster.start_debug_thread()

        def on_callback(listener: AbstractListener, result: MessageResult) -> None:
            url = StringUtils.find_url(result.text)
            number = StringUtils.get_float(result.text)
            seconds = StringUtils.time_str_to_seconds(result.text)
            skip_seconds = StringUtils.extract_number(result.text)

            # video url was provided
            if url:
                # pass it to the parsers to get the video
                for parser in get_parser_for_url(url):
                    try:
                        parsed_video = parser.parse(url)
                        if parsed_video:
                            break

                    except Exception as error:
                        print(error)

                proceed = True
                try:
                    caster.play(parsed_video)
                # if there's another app interrupting, reconnect to the device
                except NotConnected:
                    caster.play(parsed_video)
                # debug on client side
                except Exception as exception:
                    proceed = False
                    listener.send(MessageResult(str(exception), result.extra))

                options = []
                if proceed:
                    now_playing = caster.now_playing(parsed_video)
                    if parsed_video.support_resume and not parsed_video.is_live:
                        if parsed_video.title in caster.state.history:
                            start_at = caster.state.history[parsed_video.title]
                            if start_at > 0:
                                time_code = StringUtils.format_seconds(start_at)
                                now_playing += f"\n\n You didn't finish watching this video last time and stopped at `{time_code}`. Resume?"
                                options.append(time_code)

                    listener.send(MessageResult(now_playing, result.extra, options))

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
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
