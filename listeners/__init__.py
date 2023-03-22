
from listeners import ntfy_listener
from listeners.abstract_listener import AbstractListener


def get_listeners(config) -> list[AbstractListener]:
    '''
    Gets a list of available listeners
    '''
    return [ntfy_listener.NTFYListener(config)]
