import disnake
import asyncio
import datetime
import aiohttp

from disnake.ext import commands

class DCBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.launch_time = datetime.datetime.now()
        self.http_session = session = aiohttp.ClientSession(
            headers={'User-Agent': 'python-requests/2.20.0'}
        )

    @classmethod
    def create(cls) -> "DCBot":
        """Create and return an instance of a Bot."""
        loop = asyncio.get_event_loop()

        intents = disnake.Intents.all()
        intents.presences = False
        intents.dm_typing = False
        intents.dm_reactions = False
        intents.invites = False
        intents.webhooks = False
        intents.integrations = False

        return cls(
            command_prefix=commands.when_mentioned_or('!'),
            loop=loop,
            activity=disnake.Game(name=f"Commands: !help"),
            case_insensitive=True,
            max_messages=10_000,
            allowed_mentions=disnake.AllowedMentions(
                everyone=False,
                roles=False,
                users=True,
                replied_user=True
            ),
            test_guilds=[832595290174914571],
            intents=intents,
        )

    def load_extensions(self) -> None:
        """Load all enabled extensions."""
        # Must be done here to avoid a circular import.
        from utils.extensions import EXTENSIONS

        extensions = set(EXTENSIONS)  # Create a mutable copy.
        #if not constants.HelpChannels.enable:
        #    extensions.remove("bot.exts.help_channels")

        for extension in extensions:
            self.load_extension(extension)

    async def on_ready(self) -> None:
        print('Ready!')
