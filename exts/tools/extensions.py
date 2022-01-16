from disnake.ext.commands import Cog, Context, command, is_owner

from core import Dispy, logger


class Extensions(Cog, name="extension"):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    # TODO
    # Extension load/unload/reload PRIVATE
    # Documents command
    # Suggest command
    # Database
    # Bot managing (leave_guild, echo (Advanced), Blacklist) PRIVATE
    # Remind command
    # Music (Caching)
    # Warn command

    # Additional
    # Eval command (Safe eval (SnekBox))
    # Website

    @command(name="reload", aliases=["r"])
    @is_owner()
    async def extension_reload(self, ctx: Context, *, ext: str = None):
        if ext:
            logger.info('Don')
        else:
            for cog in self.bot.bot_extensions:
                logger.debug(f"Reloading: {cog}")
                self.bot.reload_extension(cog)


def setup(bot: Dispy) -> None:
    """ Load the Extensions cog """
    bot.add_cog(Extensions(bot))
