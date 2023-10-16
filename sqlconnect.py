import aiosqlite3


async def setup_db():
    async with aiosqlite3.connect("SCList.db") as db:
        async with db.cursor() as cursor:
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
                SELECT * FROM MatchedAdress ORDER BY Block_number DESC LIMIT 1
                ''')
            result = await cursor.fetchone()
            return result[0] if result is not None else None


async def set_matched_adress(block_number, time, hashcode, source, destination):
    async with aiosqlite3.connect("SCList.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('''
                INSERT OR IGNORE INTO MatchedAdress (Block_number, Time, Hash, Source, Destination) VALUES (?, ?, ?, ?, ?)
                ''', (block_number, time, hashcode, source, destination))
            await db.commit()
