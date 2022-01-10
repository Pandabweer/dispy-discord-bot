import disnake
import asyncio
import aiohttp

from datetime import datetime

from disnake.ext import commands
from core.constants import config
from core.log import logger


class Dispy(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.launch_time = datetime.now()
        self.http_session = aiohttp.ClientSession(
            headers={'User-Agent': 'python-requests/2.20.0'}
        )

    @classmethod
    def create(cls) -> "Dispy":
        """Create and return an instance of a Bot."""

        return cls(
            loop=asyncio.get_event_loop(),
            activity=disnake.Game(name=config.bot.status),
            case_insensitive=True,
            max_messages=10_000,
            allowed_mentions=disnake.AllowedMentions(
                everyone=False,
                roles=False,
                users=True,
                replied_user=True
            ),
            test_guilds=[832595290174914571],
            owner_ids=[169790484594556928],
            intents=disnake.Intents.all()
        )

    def load_extensions(self) -> None:
        """Load all enabled extensions."""
        logger.info(f"Loading extensions")

        # Must be done here to avoid a circular import.
        from utils.extensions import EXTENSIONS

        extensions = set(EXTENSIONS)  # Create a mutable copy.

        for extension in extensions:
            logger.debug(f"Loading extension {extension}")
            self.load_extension(extension)

    async def on_ready(self) -> None:
        logger.info(f"Connect to Discord and ready to roll")
        logger.debug(f"Start-up time: {round((datetime.now() - self.launch_time).microseconds / 1000)}ms")
