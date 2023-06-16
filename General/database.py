import aiosqlite
from asyncio import AbstractEventLoop


class Connector:
    __slots__ = ("db_name", "pool", "loop")

    def __init__(self, loop: AbstractEventLoop, db_name: str):
        self.db_name = db_name
        self.loop = loop

    async def create_pool(self):
        return await aiosqlite.connect(database="General/databases/" + self.db_name)

    async def __aenter__(self):
        self.pool = await self.create_pool()
        return self.pool

    async def __aexit__(self, *args):
        await self.pool.close()


class DB:
    __slots__ = ('db_name', 'db', 'loop')

    def __init__(self, db_name: str, loop: AbstractEventLoop):
        self.db_name = db_name
        self.loop = loop
        self.db = Connector(loop, self.db_name)

    async def create_tables(self):
        async with self.db as db:
            # await db.execute("""CREATE TABLE IF NOT EXISTS "users"(
            #                     _id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            #                     balance REAL NOT NULL,
            #                     username STRING,
            #                     date_reg DATETIME NOT NULL,
            #                     last_activity DATETIME)""")

            pass


