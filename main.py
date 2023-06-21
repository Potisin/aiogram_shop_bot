import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.admin import AdminCommand
from app.base import BaseCommand
from app.catalog import CatalogCommand
from app.database import Database
from config import TG_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(TG_BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
db = Database('tg_db')


async def on_startup(_):
    await db.connect()
    await db.start()
    logging.warning('Bot started')


async def on_shutdown(_):
    await db.close()
    logging.warning('Bot has been stopped')


@dp.message_handler(state='*', commands='Отмена')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())



AdminCommand(dp, db).register_command()
CatalogCommand(dp, db).register_command()
BaseCommand(dp, db).register_command()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
