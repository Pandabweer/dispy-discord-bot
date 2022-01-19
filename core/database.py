import asyncio
import asyncpg

from datetime import datetime
from typing import Union

from core.constants import config


class Database:
    """ Postgre database class """
    def __init__(self) -> None:
        self.host = config.db.host
        self.user = config.db.user
        self.name = config.db.name
        self.password = config.db.password
        self.port = config.db.port

        self.con = None

        # Connection
        asyncio.get_event_loop().run_until_complete(self.connect())

    async def connect(
        self,
        connection=None,
        new_connection=False
    ) -> asyncpg.connection.Connection:
        if self.con:
            print("""
                There already is a connection.
                Use "new_connection=True" kwarg to make a new connection
            """)
        elif not self.con or new_connection:
            if new_connection:
                print('Establishing new connection...')
                self.con.close()

            try:
                print('Connecting to PostgreSQL...')
                connection = await asyncpg.connect(
                    host=self.host,
                    user=self.user,
                    database=self.name,
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
                    use the config to input your credentials.\nExiting...
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
