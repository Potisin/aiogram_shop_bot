from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add('Каталог').add('Корзина').add('Контакты')

main_markup_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ панель')

admin_markup = ReplyKeyboardMarkup()
admin_markup.add('Добавить товар').add('Удалить товар').add('Сделать рассылку')

catalog_markup = InlineKeyboardMarkup(row_width=2)
catalog_buttons = (
    InlineKeyboardButton('Футболки', callback_data='t-shirts'),
    InlineKeyboardButton('Шорты', callback_data='shorts'),
    InlineKeyboardButton('Кроссовки', callback_data='sneakers'))
catalog_markup.add(*catalog_buttons)

cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_markup.add('Отмена')

add_to_order_markup = InlineKeyboardMarkup()
add_to_order_markup.add(InlineKeyboardButton('Добавить в корзину', callback_data='add_to_order'))
