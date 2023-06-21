from aiogram import Dispatcher


class BotCommand:

    def __init__(self, dp: Dispatcher):
        self.dp = dp

    def register_command(self):
        raise NotImplementedError
