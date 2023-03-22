import time

import config
from caster import Caster
from listeners import get_listeners
from parsers import get_parser_for_url


def main():
    '''
    Entry point of the app
    '''

    with Caster(config.CHROMECAST_DEVICE) as caster:
        caster.connect()
        caster.set_playback_rate(1.2)
        caster.start_debug_thread()

        def handle(message: str) -> None:
            if message.message.startswith('https://'):
                parsed_video = get_parser_for_url(message.message)[0].parse(message.message)
                caster.play(parsed_video)
                caster.set_playback_rate(1.2)

        for listener in get_listeners(config):
            listener.start(handler = handle)


        try:
            while 1:
                time.sleep(1)
        except KeyboardInterrupt:
            print('bye')


if __name__ == "__main__":
    raise SystemExit(main())
