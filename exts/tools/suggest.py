import asyncio

from disnake import ApplicationCommandInteraction, Message, Embed
from disnake.ext.commands import Cog, slash_command

from core import Dispy, MEDIUM_COLOR
from utils import member_get_or_fetch


class Suggest(Cog, name="suggest"):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    @slash_command(name="suggest")
    async def send_suggestion(
        self, inter: ApplicationCommandInteraction,
        suggestion: str
        ) -> Message:
        """ Suggest something to the bot owner bugs, features or tips """

        # Future plans is to redirect this to the website for better UI
        # Hence the seperate Cog

        for owner_id in self.bot.owner_ids:
            owner = await member_get_or_fetch(inter.guild, owner_id)

            embed = Embed(color=MEDIUM_COLOR, description=suggestion)
            embed.set_author(name=inter.author, icon_url=inter.author.avatar.url)

            await owner.send(embed=embed)

        return await inter.send("Thanks for your suggestion!", ephemeral=True)

def setup(bot: Dispy) -> None:
    """ Load the Suggest cog """
    bot.add_cog(Suggest(bot))
