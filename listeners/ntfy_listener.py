

from typing import Callable

import ntfpy
from ntfpy.types.message import NTFYMessage

from listeners.abstract_listener import AbstractListener, MessageResult


class NTFYListener(AbstractListener):
    '''
    NTFY Listener
    '''

    def __init__(self, config: dict) -> None:
        server = ntfpy.NTFYServer("https://ntfy.sh")
        self.client = ntfpy.NTFYClient(server, config['NTFY_CHANNEL'])

    def send(self, message: MessageResult) -> None:
        '''
        Sends message
        '''
        self.client.send(message.message)

    async def start(self, handler: Callable[[AbstractListener, MessageResult], None]) -> None:
        '''
        Starts listening
        '''

        def _callback(message: NTFYMessage) -> None:
            handler(message.message, self)

        await self.client.subscribe(_callback)
