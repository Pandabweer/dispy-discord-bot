from typing import Any

from disnake.ext.commands import (
    Context,
    Cog,
    CommandNotFound
)

from core import Dispy, logger

class ErrorHandler(Cog, name="error_handler"):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    @Cog.listener('on_command')
    async def w(self, ctx: Context) -> None:
        await ctx.message.delete()

    @Cog.listener('on_command_error')
    async def err_hanlder(self, ctx: Context, error: Any) -> None:
        # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, CommandNotFound):
            logger.warn(f"{ctx.author.name} this command does not exist")
        else:
            logger.error(error)

def setup(bot: Dispy) -> None:
    """ Load the ErrorHandler cog """
    bot.add_cog(ErrorHandler(bot))
