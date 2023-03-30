
from typing import ItemsView

from listeners import ntfy_listener, telegram_listener
from listeners.abstract_listener import AbstractListener


def get_listeners(config:dict) -> list[AbstractListener]:
    '''
    Gets a list of available listeners
    '''
    return [
        # ntfy_listener.NTFYListener(config),
        # TODO: figure out python async future call blocking
        telegram_listener.TelegramListener(config)
    ]
