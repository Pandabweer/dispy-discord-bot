from disnake.ext.commands import Cog, Context, command, is_owner

from core import Dispy, logger
from utils.test import F95zone


class Utils(Cog, name="utils"):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot
        self.request = F95zone()

    async def cog_check(self, ctx: Context):
        return ctx.author.id in self.bot.owner_ids

    @command(name="edit_bot_name")
    async def edit_bot_name(self, ctx: Context, *, name: str = None):
        await ctx.bot.user.edit(username=name)

    @command(name="test")
    async def tst(self, ctx: Context):
        r = await self.bot.pg.raw.fetchrow("SELECT * FROM guilds LIMIT 1")

        await self.request("https://f95zone.to/threads/accidental-woman-v0-99-thaumx.4280/")

        await ctx.send(self.request.game_version)


def setup(bot: Dispy) -> None:
    """ Load the Utils cog """
    bot.add_cog(Utils(bot))
