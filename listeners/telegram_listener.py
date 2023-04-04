

from typing import Callable

from telebot import TeleBot, types

from listeners.abstract_listener import AbstractListener, MessageResult


OPTIONS = {
    'play_rate': {
        'buttons': ['0.75', '1', '1.25', '1.5', '1.75', '2'],
        'message': "Choose play rate"
    },
    'volume': {
        'buttons': ['0', '10', '25', '50', '75', '90', '100'],
        'message': "Choose volume"
    },
    'seek': {
        'buttons': ['-5', '-10', '-15', '-30', '+5', '+10', '+15', '+30'],
        'message': "FF/Rewind seconds:"
    }
}


class TelegramListener(AbstractListener):
    '''
    Telegram bot listener
    '''

    bot: TeleBot

    def __init__(self, config: dict) -> None:
        self.bot = TeleBot(config['TELEGRAM_BOT_TOKEN'])

    def send(self, message: MessageResult) -> None:
        '''
        Send message back to the listener
        '''
        if message.options:
            markup = types.InlineKeyboardMarkup(row_width=3)

            buttons = [types.InlineKeyboardButton(option, callback_data=option) for option in message.options]
            markup.add(*buttons)

            self.bot.send_message(message.extra.chat.id, message.text, reply_markup=markup,
                                  parse_mode="Markdown", disable_web_page_preview=True)
        else:
            self.bot.reply_to(message.extra,
                              text=message.text,
                              parse_mode="Markdown",
                              disable_web_page_preview=True)

    async def start(self, handler: Callable[[AbstractListener, MessageResult], None]) -> None:
        '''
        Starts listening
        '''

        print('TelegramListener is listening ...')

        ########################
        # Message Endpoints
        ########################

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_all(call: types.CallbackQuery):
            '''
            Handles button callbacks
            '''
            handler(self, MessageResult(call.data, call.message))
            # TODO: move this into handler's callback
            #self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            self.bot.answer_callback_query(call.id, text="Callback query processed!")
            #self.bot.delete_message(call.message.chat.id, call.message.message_id)

        @ self.bot.message_handler(func=self._commands_filter)
        def message_commands(message: types.Message):
            for command, option in OPTIONS.items():
                if message.text[1:].startswith(command):
                    markup = types.InlineKeyboardMarkup(row_width=4)
                    buttons = [types.InlineKeyboardButton(button, callback_data=button) for button in option['buttons']]
                    markup.add(*buttons)

                    self.bot.send_message(message.chat.id, option['message'], reply_markup=markup)
                    break

        @ self.bot.message_handler(func=lambda msg: True)
        def message_all(message: types.Message):
            '''
            Handles user messages to the telegram bot that weren't handled previously
            '''
            handler(self, MessageResult(message.text, message))

        self.bot.infinity_polling()

    def _commands_filter(self, message: types.Message) -> bool:
        if not message.text.startswith('/'):
            return False

        commands = list(OPTIONS.keys())
        command = message.text.split()[0][1:].lower()
        return command in commands
