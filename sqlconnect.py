import aiosqlite3


# create db

async def setup_db():
    async with aiosqlite3.connect("SCList.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS LastProcessedBlock (
                    Block_number INTEGER UNIQUE ON CONFLICT IGNORE NOT NULL
                    )
            ''')
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS MatchedAdress (
                    Block_number INTEGER PRIMARY KEY UNIQUE ON CONFLICT IGNORE NOT NULL,
                    Time TEXT NOT NULL,
                    Hash TEXT UNIQUE NOT NULL,
                    Source TEXT NOT NULL,
                    Destination TEXT NOT NULL
                )
            ''')
            await db.commit()


async def get_last_block():
    async with aiosqlite3.connect("SCList.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('''
                SELECT Block_number FROM LastProcessedBlock
                ''')
            result = await cursor.fetchone()
            return result[0] if result is not None else None


async def set_last_block(block_number):
    async with aiosqlite3.connect("SCList.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('''
                INSERT INTO LastProcessedBlock (Block_number) VALUES (?)
                ''', (block_number,))
            await db.commit()


async def set_matched_adress(block_number, time, hashcode, source, destination):
    async with aiosqlite3.connect("SCList.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('''
                INSERT INTO MatchedAdress (Block_number, Time, Hash, Source, Destination) VALUES (?, ?, ?, ?, ?)
                ''', (block_number, time, hashcode, source, destination))
            await db.commit()
