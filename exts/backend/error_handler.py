from typing import Any

from disnake import HTTPException, Forbidden
from disnake.ext.commands import (
    Context,
    Cog,
    CommandNotFound,
    CheckFailure
)

from core import Dispy, logger

class ErrorHandler(Cog, name="error_handler"):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    @Cog.listener('on_command')
    async def delete_command(self, ctx: Context) -> None:
        try:
            await ctx.message.delete()
        except Forbidden:
            debug.info("Did not have permission to remove the command")

    @Cog.listener('on_command_error')
    async def err_handler(self, ctx: Context, error: Any) -> None:
        # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        # Get original error instead of a global Invoke error
        error = getattr(error, 'original', error)

        # Standard debug to log to catch unkown errors
        logger.debug(type(error))

        if isinstance(error, CommandNotFound):
            logger.debug(f"{ctx.author} this command does not exist")
        elif isinstance(error, HTTPException):
            error.text = error.text.replace("\n", " ")
            logger.warn(f"HTTPException: {error.text}")
        elif isinstance(error, CheckFailure):
            logger.debug(f"Check failed for {ctx.author} most likely has no permission to execute this")
        else:
            logger.error(error)

def setup(bot: Dispy) -> None:
    """ Load the ErrorHandler cog """
    bot.add_cog(ErrorHandler(bot))
