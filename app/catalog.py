from aiogram import types, Dispatcher

from app import BotCommand
from app.database import Database
from app.keyboards import catalog_markup, add_to_order_markup


class CatalogCommand(BotCommand):
    def __init__(self, dp: Dispatcher, db: Database):
        super().__init__(dp)
        self.db = db

    def register_command(self):
        @self.dp.message_handler(text='Каталог')
        async def give_catalog(message: types.Message):
            await message.answer('Выберите тип товара', reply_markup=catalog_markup)

        @self.dp.callback_query_handler()
        async def callback_markup(call: types.CallbackQuery):
            item_type = call.data
            items = await self.db.get_items_by_type(item_type)

            for item in items:
                await call.message.answer_photo(item[5], caption=f'Название {item[2]}\n'
                                                                 f'Описание: {item[3]}\n'
                                                                 f'Цена {item[4]}', reply_markup=add_to_order_markup)


