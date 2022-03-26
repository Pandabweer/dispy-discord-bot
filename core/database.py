import asyncio
import asyncpg

from datetime import datetime
from typing import Union

from core.constants import config
from core.log import logger


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
            logger.debug("""
                There already is a connection.
                Use "new_connection=True" kwarg to make a new connection
                """)
        elif not self.con or new_connection:
            if new_connection:
                logger.debug('Establishing new connection...')
                self.con.close()

            try:
                logger.debug('Connecting to PostgreSQL...')
                connection = await asyncpg.connect(
                    host=self.host,
                    user=self.user,
                    database=self.name,
                    password=self.password,
                    port=self.port
                    )
            except asyncpg.exceptions.InvalidCatalogNameError:
                logger.debug(f"I could not find a database named: {self.database}")
            except asyncpg.exceptions.InvalidPasswordError:
                logger.critical("Invalid PostrgeSQL password or username")
                exit("Invalid PostrgeSQL password or username.\nExiting...")
            except ConnectionRefusedError:
                logger.critical("I could not connect to PostgreSQL")
                exit("""
                    I could not connect to PostgreSQL,
                    use the config to input your credentials.\nExiting...
                    """)
            else:
                logger.debug('Connection established')

        self.con = connection or self.con
        return connection or self.con

    async def close(self) -> None:
        self.con.close()

    @property
    def raw(self) -> asyncpg.connection.Connection:
        return self.con

    @property
    async def ping(self) -> int:
        past = datetime.now()
        await self.con.fetchrow("SELECT * FROM guilds LIMIT 1")

        return int((datetime.now() - past).microseconds / 1000)
