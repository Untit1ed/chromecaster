
import sys
import threading
import time
from threading import Thread
from typing import Optional

import pychromecast

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

    def __init__(self, chromecast_name):
        """
        Initializes a new Caster object.

        Args:
            chromecast_name: The friendly name of the Chromecast device to connect to.
        """
        self.chromecast_name = chromecast_name
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

        self.stop_debug_thread()

    def connect(self):
        """
        Discovers and connects to the Chromecast device.
        """
        SpinnerUtil.start()
        self.cast_device = self._get_chromecast_device()
        self.cast_device.wait()
        self.cast_device.media_controller.block_until_active(10)
        SpinnerUtil.stop()

        self.print_device_info(self.cast_device)

    def set_volume(self, volume: float):
        """
        Sets the volume level of the Chromecast device.

        Args:
            volume: A float representing the volume level.
        """
        self.cast_device.socket_client.receiver_controller.send_message(
            {'type': "SET_VOLUME", "volume": {"level": volume}})

    def set_playback_rate(self, playback_rate: float):
        """
        Sets the playback rate of the media on the Chromecast device.

        Args:
            playback_rate: A float representing the playback rate.
        """
        self.cast_device.media_controller.send_message({
            'type': "SET_PLAYBACK_RATE",
            "playbackRate": playback_rate,
            'mediaSessionId': self.cast_device.media_controller.status.media_session_id})

    def play(self, video: ParseResult):
        """
        Plays a media on the Chromecast device.

        Args:
            url: A string representing the URL of the media.
        """

        m_c = self.cast_device.media_controller

        # if mc.status.content_id:
        #    url = mc.status.content_id

        m_c.play_media(video.url, video.mime_type, title=video.title, thumb=video.thumbnail_url)
        m_c.block_until_active()

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
            raise RuntimeError('No Chromecast devices on the network')

        return chromecasts[0]

    def print_device_info(self, device: pychromecast.Chromecast):
        """
        Prints debug info about the Chromecast device.

        Args:
            device: A Chromecast object representing the connected device.
        """

        mc_status = device.media_controller.status

        content = mc_status.content_id
        if content:
            content = StringUtils.make_link(content, StringUtils.shorten_long_string(content))

        progress_bar = StringUtils.progress_bar(
            mc_status.current_time,
            mc_status.duration)

        print(
            f'''
    Device: {device.name}, {device.model_name}
    Status: {device.status.display_name} ({device.status.status_text}) @{device.status.volume_level:.0%}
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
            self.cast_device.media_controller.update_status()

            lines_of_text = 6
            # Move cursor up N lines
            sys.stdout.write(f'\033[{lines_of_text}A')
            # Clear the old text before overwriting
            for _ in range(lines_of_text):
                sys.stdout.write('\033[K')
                sys.stdout.write('\n')
            sys.stdout.write(f'\033[{lines_of_text}A')

            self.print_device_info(self.cast_device)
            time.sleep(10)
