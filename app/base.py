from aiogram import types, Dispatcher

from app import BotCommand
from app.database import Database
from app.keyboards import main_markup, main_markup_admin
from config import ADMIN_ID


class BaseCommand(BotCommand):
    def __init__(self, dp: Dispatcher, db: Database):
        super().__init__(dp)
        self.db = db

    def register_command(self):
        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await self.db.add_user(message.from_user.id)
            await message.answer_sticker('CAACAgIAAxkBAANDZIrYrc2sGVZhGzkkxU8WWI3dz4MAAnUZAAKOqpFIZWbadXVVKLYvBA')
            await message.answer('hello',
                                 reply_markup=main_markup if message.from_user.id != int(
                                     ADMIN_ID) else main_markup_admin)

        @self.dp.message_handler(text='Корзина')
        async def give_trash(message: types.Message):
            await message.answer('Корзина пуста')

        @self.dp.message_handler(text='Контакты')
        async def give_contacts(message: types.Message):
            await message.answer('Обращайтесь сюда')

        @self.dp.message_handler()
        async def other(message: types.Message):
            await message.answer('Я тебя не понимаю')




