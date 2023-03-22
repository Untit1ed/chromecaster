

import asyncio
from typing import Callable

import ntfpy
from ntfpy.types.message import NTFYMessage

from listeners.abstract_listener import AbstractListener


class NTFYListener(AbstractListener):
    '''
    NTFY Listener
    '''

    def __init__(self, config) -> None:
        server = ntfpy.NTFYServer("https://ntfy.sh")
        self.client = ntfpy.NTFYClient(server, config.NTFY_CHANNEL)

    def send(self, message: str) -> None:
        '''
        Sends message
        '''
        self.client.send(message)

    def start(self, handler: Callable[[str], None]) -> None:
        '''
        Starts listening
        '''

        def _callback(message: NTFYMessage) -> None:
            handler(message.message)

        asyncio.run(self.client.subscribe(_callback))
