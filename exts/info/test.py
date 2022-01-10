from disnake import ApplicationCommandInteraction, Message, Member
from disnake.ext.commands import AutoShardedBot, Cog, slash_command

from core import logger


class Test(Cog, name='test'):
    def __init__(self, bot: AutoShardedBot) -> None:
        self.bot = bot

    @Cog.listener('on_message_delete')
    async def yes(self, message: Message) -> None:
        logger.warn(f'{message.author} deleted message: {message.content}')
        return


def setup(bot: AutoShardedBot) -> None:
    """ Load the fun cog """
    bot.add_cog(Test(bot))
