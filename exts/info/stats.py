from disnake.ext import commands

class Stats(commands.Cog, name='stats'):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter):
        await inter.response.send_message(f'pong', ephemeral=True)

    @commands.command(name="ping")
    async def ping_prefix(self, ctx):
        await ctx.send('pong')

def setup(bot: commands.Bot) -> None:
    """Load the stats cog."""
    bot.add_cog(Stats(bot))
