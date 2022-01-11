from disnake import Message
from disnake.ext.commands import AutoShardedBot, Cog

from core import Dispy, logger


class Test(Cog, name='test'):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    @Cog.listener('on_message_delete')
    async def yes(self, message: Message) -> None:
        logger.warn(f'{message.author} deleted message: {message.content}')
        return


def setup(bot: Dispy) -> None:
    """ Load the fun cog """
    bot.add_cog(Test(bot))
