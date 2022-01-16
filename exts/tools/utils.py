from disnake.ext.commands import Cog, Context, command, is_owner

from core import Dispy, logger


class Utils(Cog, name="utils"):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context):
        return ctx.author.id in self.bot.owner_ids

    @command(name="edit_bot_name")
    async def edit_bot_name(self, ctx: Context, *, name: str = None):
        await ctx.bot.user.edit(username=name)


def setup(bot: Dispy) -> None:
    """ Load the Utils cog """
    bot.add_cog(Utils(bot))
