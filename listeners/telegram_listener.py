

from typing import Callable

import telebot

from listeners.abstract_listener import AbstractListener, MessageResult


class TelegramListener(AbstractListener):
    '''
    Telegram bot listener
    '''

    bot: telebot.TeleBot

    def __init__(self, config: dict) -> None:
        self.bot = telebot.TeleBot(config['TELEGRAM_BOT_TOKEN'])

    def send(self, message) -> None:
        '''
        Send message back to the listener
        '''
        self.bot.reply_to(message.extra, "Got it")

    async def start(self, handler: Callable[[AbstractListener, MessageResult], None]) -> None:
        '''
        Starts listening
        '''

        print('TelegramListener is listening ...')

        @self.bot.message_handler(func=lambda msg: True)
        def echo_all(message):
            handler(self, MessageResult(message.text, message))

        self.bot.infinity_polling()
