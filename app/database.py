from typing import List, Tuple, Any

import aiosqlite
from aiogram.dispatcher import FSMContext


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_name)

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def start(self):
        async with self.conn.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS accounts('
                                 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                                 'cart_id TEXT,'
                                 'tg_id TEXT)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS items('
                                 'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                 'type TEXT,'
                                 'name TEXT,'
                                 'desc TEXT,'
                                 'price TEXT,'
                                 'photo TEXT)')
            await self.conn.commit()

    async def get_items_by_type(self, item_type: str) -> List[Tuple[Any, ...]]:
        async with self.conn.cursor() as cursor:
            await cursor.execute('SELECT * FROM items WHERE type = ?', (item_type,))
            items = await cursor.fetchall()
        return items

    async def add_user(self, user_tg_id: str):
        async with self.conn.cursor() as cursor:
            await cursor.execute('SELECT * FROM accounts WHERE tg_id = ?', (user_tg_id,))
            user = await cursor.fetchone()
            if not user:
                await cursor.execute('INSERT INTO accounts (tg_id) VALUES (?)', (user_tg_id,))
            await self.conn.commit()

    async def cmd_add_item(self, state: FSMContext):
        async with self.conn.cursor() as cursor:
            async with state.proxy() as data:
                await cursor.execute('INSERT INTO items (type, name, desc, price, photo) VALUES (?, ?, ?, ?, ?)',
                                     (data['type'], data['name'], data['desc'], data['price'], data['photo']))
                await self.conn.commit()
