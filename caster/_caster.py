
import sys
import threading
import time
from threading import Thread
from typing import Optional

import pychromecast

from caster._state import State
from parsers.abstract_parser import ParseResult
from utils.spinner_util import SpinnerUtil
from utils.string_utils import StringUtils


class Caster():
    """
    A class for discovering and connecting to a Chromecast device and controlling it.

    Attributes:
        cast_device: A Chromecast object representing the connected device.
        browser: A CastBrowser object used for discovering Chromecast devices.
        chromecast_name: The friendly name of the Chromecast device to connect to.
        debug_thread: A Thread object for running the debug loop.
        stop_debug: A threading.Event object used to stop the debug thread.
    """

    cast_device: Optional[pychromecast.Chromecast] = None
    browser: Optional[pychromecast.CastBrowser] = None
    debug_thread: Optional[Thread] = None
    last_known_status = 'IDLE'
    current_video: Optional[ParseResult] = None
    state: State

    def __init__(self, chromecast_name: str):
        """
        Initializes a new Caster object.

        Args:
            chromecast_name: The friendly name of the Chromecast device to connect to.
        """

        if not chromecast_name:
            raise ValueError("`chromecast_name` cannot be empty")
        self.chromecast_name = chromecast_name

        self.state = State.init_state()
        self.stop_debug = threading.Event()

    def __enter__(self):
        """
        Enters the 'with' block and returns the Caster object.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the 'with' block and stops the discovery process.
        """
        if self.browser:
            self.browser.stop_discovery()

        self.state.save_state()
        self.stop_debug_thread()

    def connect(self):
        """
        Discovers and connects to the Chromecast device.
        """
        SpinnerUtil.start()
        self.cast_device = self._get_chromecast_device()
        self.cast_device.wait()
        self.cast_device.media_controller.block_until_active(10)
        self.set_volume(self.state.volume)
        SpinnerUtil.stop()

        self.print_device_info()

    def set_volume(self, volume: float):
        """
        Sets the volume level of the Chromecast device.

        Args:
            volume: A float representing the volume level 0-100.
        """
        self.state.volume = volume
        self.cast_device.socket_client.receiver_controller.send_message(
            {'type': "SET_VOLUME", "volume": {"level": volume/100}})

    def skip(self, seconds: float):
        """
        Fast forward or rewind X amount of seconds
        """
        self.seek(self.cast_device.media_controller.status.current_time+seconds)

    def seek(self, seconds: float):
        """
        Seek the current media to a specific location.
        """

        self.cast_device.media_controller.seek(seconds)

    def set_playback_rate(self, playback_rate: float = None):
        """
        Sets the playback rate of the media on the Chromecast device.

        Args:
            playback_rate: A float representing the playback rate.
        """

        if playback_rate:
            self.state.play_rate = playback_rate
        else:
            playback_rate = 1

        self.cast_device.media_controller.send_message({
            'type': "SET_PLAYBACK_RATE",
            "playbackRate": playback_rate,
            'mediaSessionId': self.cast_device.media_controller.status.media_session_id})

    def play(self, video: ParseResult = None):
        """
        Plays a media on the Chromecast device.

        Args:
            url: A string representing the URL of the media.
        """
        if video:
            self.current_video = video
        else:
            video = self.current_video

        m_c = self.cast_device.media_controller

        # _TODO: play around with quick play in order to try different renderers
# app_display_name:
# 'Web Video Caster'
# app_id:
# 'AD229957'
        m_c.play_media(video.url, video.mime_type, title=video.title,
                       thumb=video.thumbnail_url,
                       current_time=0,
                       media_info={
                           'playbackRate': self.state.play_rate,
                           'volume': {'level': self.state.volume/100}})

        m_c.block_until_active(15)

        if video.is_live:
            self.set_playback_rate()  # always play live at x1
        else:
            self.set_playback_rate(self.state.play_rate)

    def now_playing(self, video: ParseResult = None) -> str:
        '''
        Print what's playing now
        '''

        if not video:
            video = ParseResult(
                url=self.cast_device.media_controller.status.content_id,
                title=self.cast_device.status.status_text,
                mime_type='',
                thumbnail_url='https://i.imgur.com/a0hazzA.png')

        title = StringUtils.escape_markdown(video.title)
        # device_info = StringUtils.escape_markdown(f'{self.cast_device.name}, {self.cast_device.model_name}')
        play_rate = StringUtils.escape_markdown(self.state.play_rate)
        volume = StringUtils.escape_markdown(self.state.volume)
        # thumbnail_url = StringUtils.escape_markdown(video.thumbnail_url)
        # video_url = StringUtils.escape_markdown(video.url)
        duration = StringUtils.escape_markdown(StringUtils.seconds_to_timestamp(video.duration))
        links = str.join(', ',  [f'[{title}]({StringUtils.escape_markdown(link)})' for title, link in video.links])

        return f"""
__*{title}*__

🔊: *{volume}%* 🐢: *x{play_rate}* ⏳: `{duration}`

{links}
"""

    def discover_chromecast_devices(self) -> list[pychromecast.CastBrowser]:
        '''
        Discovers all Chromecast devices
        '''
        chromecasts, self.browser = pychromecast.discover_chromecasts()
        return chromecasts

    def _get_chromecast_device(self) -> pychromecast.Chromecast:
        """
        Discovers the Chromecast device with the specified friendly name.

        Raises:
            ValueError: If there are no Chromecast devices on the network.

        Returns:
            A Chromecast object representing the discovered device.
        """
        chromecasts, self.browser = pychromecast.get_listed_chromecasts(
            friendly_names=[self.chromecast_name])

        if not chromecasts:
            raise RuntimeError(f'No Chromecast device `{self.chromecast_name}` on the network')

        return chromecasts[0]

    def print_device_info(self):
        """
        Prints debug info about the Chromecast device.

        Args:
            device: A Chromecast object representing the connected device.
        """

        mc_status = self.cast_device.media_controller.status

        # update state with current video time
        if mc_status.title and mc_status.current_time:
            self.state.history[mc_status.title] = mc_status.current_time

        content = mc_status.content_id
        if content:
            content = StringUtils.make_link(content, StringUtils.shorten_long_string(content))

        progress_bar = StringUtils.progress_bar(
            mc_status.current_time,
            mc_status.duration)

        print(
            f'''
    Device: {self.cast_device.name}, {self.cast_device.model_name}
    Status: {self.cast_device.status.display_name} ({self.cast_device.status.status_text}) @{self.cast_device.status.volume_level:.0%}
    Player State: {mc_status.player_state}\tx{mc_status.playback_rate}
    Content: {content}
    {progress_bar}''')

    def start_debug_thread(self):
        """
        Starts the debug thread.
        """
        self.stop_debug.clear()
        self.debug_thread = threading.Thread(target=self.debug_loop)
        self.debug_thread.start()

    def stop_debug_thread(self):
        """
        Stops the debug thread.
        """
        self.stop_debug.set()
        if self.debug_thread is not None:
            self.debug_thread.join()
        self.debug_thread = None

    def debug_loop(self):
        """
        Main loop of the debug thread.
        """
        while not self.stop_debug.is_set():
            # only update status when not idling, otherwise it restarts the renderer app
            # _TODO: switch to status update callbacks
            if (self.cast_device.media_controller.status.player_state not in ['UNKNOWN', 'IDLE']):
                self.cast_device.media_controller.update_status()
                time.sleep(1)

            lines_of_text = 6
            # Move cursor up N lines
            sys.stdout.write(f'\033[{lines_of_text}A')
            # Clear the old text before overwriting
            for _ in range(lines_of_text):
                sys.stdout.write('\033[K')
                sys.stdout.write('\n')
            sys.stdout.write(f'\033[{lines_of_text}A')

            self.print_device_info()
            time.sleep(9)
