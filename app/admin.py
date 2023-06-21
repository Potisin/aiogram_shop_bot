from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app import BotCommand
from app.database import Database
from app.keyboards import admin_markup, catalog_markup, cancel_markup
from config import ADMIN_ID


class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


class AdminCommand(BotCommand):
    def __init__(self, dp: Dispatcher, db: Database):
        super().__init__(dp)
        self.db = db

    def register_command(self):

        @self.dp.message_handler(text='Админ панель')
        async def admin_panel(message: types.Message):
            if message.from_user.id == int(ADMIN_ID):
                await message.answer('Админ панель', reply_markup=admin_markup)
            else:
                await message.answer('Я тебя не понимаю')

        @self.dp.message_handler(text='Добавить товар')
        async def add_item_choose_type(message: types.Message):
            if message.from_user.id == int(ADMIN_ID):
                await NewOrder.type.set()
                await message.answer('Выберите тип товара', reply_markup=catalog_markup)
            else:
                await message.answer('Я тебя не понимаю')

        @self.dp.callback_query_handler(state=NewOrder.type)
        async def callback_add_item_type(call: types.CallbackQuery, state: FSMContext):
            async with state.proxy() as data:
                data['type'] = call.data
                await call.message.answer('Напишите название товара', reply_markup=cancel_markup)
                await NewOrder.next()

        @self.dp.message_handler(state=NewOrder.name)
        async def add_item_name(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['name'] = message.text
                await message.answer('Напишите описание товара')
                await NewOrder.next()

        @self.dp.message_handler(state=NewOrder.desc)
        async def add_item_desc(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['desc'] = message.text
                await message.answer('Укажите цену товара')
                await NewOrder.next()

        @self.dp.message_handler(state=NewOrder.price)
        async def add_item_price(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['price'] = message.text
                await message.answer('Пришлите фотографию товара')
                await NewOrder.next()

        @self.dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
        async def add_item_photo_check(message: types.Message):
            await message.answer('Это не фотография!')

        @self.dp.message_handler(content_types=['photo'], state=NewOrder.photo)
        async def add_item_photo(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            await self.db.cmd_add_item(state)
            await message.answer('Товар успешно создан', reply_markup=admin_markup)
            await state.finish()

