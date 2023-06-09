import asyncio
import os

from pychromecast.error import NotConnected

from caster import Caster
from listeners import get_listeners
from listeners.abstract_listener import AbstractListener, MessageResult
from parsers import get_parser_for_url
from utils.string_utils import StringUtils

VIDEO_PLAY_THRESHOLD = 30


def _play_video(caster: Caster, listener: AbstractListener, url: str, result: MessageResult) -> None:
    # pass it to the parsers to get the video
    for parser in get_parser_for_url(url):
        try:
            video = parser.parse(url)
            if video:
                break
        except Exception as exception:
            listener.send(MessageResult(StringUtils.escape_markdown(repr(exception)), result.extra))

    try:
        if video:
            caster.play(video)
        else:
            raise Exception("No video to play")
    # if there's another app interrupting, reconnect to the device
    except NotConnected:
        caster.play(video)
    # debug on client side
    except Exception as exception:
        listener.send(MessageResult(StringUtils.escape_markdown(repr(exception)), result.extra))
        return

    options = []
    now_playing = caster.now_playing(video)
    if video.support_resume and not video.is_live:
        if video.title in caster.state.history:
            start_at = caster.state.history[video.title]
            if start_at > VIDEO_PLAY_THRESHOLD and (not video.duration or start_at <= video.duration - VIDEO_PLAY_THRESHOLD):
                time_code = StringUtils.seconds_to_timestamp(start_at)
                now_playing += f"\n_You didn't finish watching this video last time and stopped at `{time_code}`\\. Resume?_"
                options.append(time_code)

    listener.send(MessageResult(now_playing, result.extra, options, video))


def main():
    '''
    Entry point of the app
    '''

    with Caster(os.environ.get('CHROMECAST_DEVICE')) as caster:
        caster.connect()

        caster.start_debug_thread()

        def on_callback(listener: AbstractListener, result: MessageResult) -> None:
            """
            Handles messages from a listener
            """
            url = StringUtils.find_url(result.text)
            number = StringUtils.get_float(result.text)
            seconds = StringUtils.timestamp_to_seconds(result.text)
            skip_seconds = StringUtils.extract_number(result.text)

            # replaying a video, if this is a currently playing video
            # then restart it skipping video parsing
            if url and result.text == f'rp {url}':
                if caster.current_video and caster.current_video.original_url == url:
                    caster.play()
                else:
                    _play_video(caster, listener, url, result)
            # video url was provided, parse and play
            elif url:
                _play_video(caster, listener, url, result)
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
