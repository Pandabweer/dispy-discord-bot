import asyncio
import asyncpg

from datetime import datetime
from typing import Union


class Guild:
    def __init__(self, record: asyncpg.Record) -> None:
        self.id = record[0]
        self.prefix = record[1]


class Database:
    """ Postgre database class """
    def __init__(
        self,
        host: str,
        user: str,
        database: str,
        password: str,
        port: int,
        *args,
        **kwargs
    ) -> None:
        self.host = host
        self.user = user
        self.database = database
        self.password = password
        self.port = port

        self.con = None

        # Connection
        asyncio.get_event_loop().run_until_complete(self.connect())

    async def connect(
        self,
        *args,
        connection=None,
        new_connection=False,
        **kwargs
    ) -> asyncpg.connection.Connection:
        if self.con:
            print("""
                There already is a connection.
                Use "new_connection=True" kwarg to make a new connection
            """)
        elif not self.con or new_connection:
            if new_connection:
                print('Establashing new connection...')
                self.con.close()

            try:
                print('Connecting to PostgreSQL...')
                connection = await asyncpg.connect(
                    host=self.host,
                    user=self.user,
                    database=self.database,
                    password=self.password,
                    port=self.port
                )
            except asyncpg.exceptions.InvalidCatalogNameError:
                print(f"I could not find a database named: {self.database}")
            except asyncpg.exceptions.InvalidPasswordError:
                exit("Invalid PostrgeSQL password or username.\nExiting...")
            except ConnectionRefusedError:
                exit("""
                    I could not connect to PostgreSQL,
                    use the config to input your cridentials.\nExiting...
                """)
            else:
                print('Connection established')

        self.con = connection or self.con
        return connection or self.con

    async def close(self):
        self.con.close()

    @property
    async def ping(self):
        past = datetime.now()
        await self.con.fetchrow("SELECT * FROM guilds LIMIT 1")

        return int((datetime.now() - past).microseconds / 1000)

    @property
    async def guild_amount(self):
        return len(await self.con.fetchrow("SELECT guildid FROM guilds"))

    async def get_guild(self, guild_id: Union[int, str]) -> Guild:
        return Guild(
            await self.con.fetchrow(
                """
                SELECT
                        guildid,
                        hentai_channel,
                        prefix
                    FROM guilds
                    WHERE guildid = $1
                """,
                str(guild_id)
            )
        )
