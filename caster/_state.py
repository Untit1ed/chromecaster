from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Final

import dacite

FILE_LOC: Final[str] = 'settings.json'

@dataclass
class State:
    '''
    Represents caster's state
    '''
    play_rate: float = 1
    volume: float = 100
    history: dict[str, float] = None

    def to_json(self) -> str:
        '''
        Serializes class to JSON string
        '''
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def init_state() -> State:
        '''
        Populate state from file
        '''
        with open(FILE_LOC, 'r', encoding='utf-8') as file:
            settings = file.read()
            json_object = json.loads(settings)

            state = dacite.from_dict(
                data_class=State,
                data=json_object
            )

            return state

    def save_state(self) -> None:
        '''
        Save state in a file
        '''
        with open(FILE_LOC, 'w', encoding='utf-8') as file:
            file.write(self.to_json())
