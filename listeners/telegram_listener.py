

from typing import Callable

from telebot import TeleBot, types

from listeners.abstract_listener import AbstractListener, MessageResult

OPTIONS = {
    'play_rate': {
        'buttons': ['0.75', '1', '1.25', '1.5', '1.75', '2'],
        'message': "Choose playback rate 🐢-🚶‍♂️-🏃‍♂️",
        'callback_message': "Playback rate is set to {}"
    },
    'volume': {
        'buttons': ['0', '10', '25', '50', '75', '90', '100'],
        'message': "Choose volume 🔇-🔈-🔉-🔊",
        'callback_message': "Play rate is set to {}"
    },
    'seek': {
        'buttons': ['-5', '-10', '-15', '-30', '+5', '+10', '+15', '+30'],
        'message': "⏪ Rewind or Fast Forward ⏩ (seconds):",
        'callback_message': "Seek {} seconds"
    },
    'replay': {
        'message': '🔁 Replay',
        'callback_message': "Replaying the media"
    },
    'close': {
        'message': '❌ Close',
        'callback_message': "Dialog is closed"
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
        Handle message that was sent back to the listener
        '''
        markup = types.InlineKeyboardMarkup(row_width=3)
        buttons = []
        if message.options:
            buttons += [self._add_button(f'🧭 {option}', option) for option in message.options]

        buttons.append(self._add_button(
            OPTIONS['replay']['message'],
            f'rp {message.video.original_url}', 'replay'))
        markup.add(*buttons)
        self.bot.send_message(message.extra.chat.id,
                              message.text,
                              reply_to_message_id=message.extra.id,
                              reply_markup=markup,
                              parse_mode="MarkdownV2",
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

            message = call.data
            option = None
            if ';' in message:
                option, message, *_ = message.split(';')

            if option and option == 'close':
                parent_message = [int(item) for item in message.split(':')]
                self.bot.delete_message(*parent_message)
                # self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
                self.bot.delete_message(call.message.chat.id, call.message.message_id)
            else:
                handler(self, MessageResult(message, call.message))

            if option:
                callback_message = OPTIONS[option]['callback_message'].format(message)
            else:
                callback_message = message

            self.bot.answer_callback_query(call.id, text=callback_message)

        @ self.bot.message_handler(func=self._commands_filter)
        def message_commands(message: types.Message):
            for command, option in OPTIONS.items():
                if message.text[1:].startswith(command):
                    markup = types.InlineKeyboardMarkup(row_width=4)
                    buttons = [types.InlineKeyboardButton(
                        button,
                        callback_data=f'{command};{button}'
                    ) for button in option['buttons']]
                    markup.add(*buttons)

                    # add close button with information about trigger message
                    markup.row(types.InlineKeyboardButton(
                        OPTIONS['close']['message'],
                        callback_data=f'close;{message.chat.id}:{message.message_id}'
                    ))

                    self.bot.send_message(
                        message.chat.id, option['message'],
                        reply_markup=markup
                    )
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

    def _add_button(self, label: str, message: str, command: str = None) -> types.InlineKeyboardButton:
        if command:
            data = f"{command};{message}"[:64]
        else:
            data = message

        return types.InlineKeyboardButton(
            text=label,
            callback_data=data)
