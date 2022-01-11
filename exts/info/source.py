import inspect
from typing import Optional

from disnake import ApplicationCommandInteraction, Message, Embed
from disnake.ext.commands import Cog, slash_command

from core import (
    Dispy,
    logger,
    NEGATIVE_REPLIES,
    ERROR_COLOR,
    SUCCESS_COLOR
)


class BotSource(Cog, name="source_bot"):
    """ Displays information about the bot's source code """
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    @slash_command(name="source", guild_ids=[561662622827806721, 926115595307614249])
    async def source_command(
        self, inter: ApplicationCommandInteraction, *,
        source_item: str = None,
        private: bool = True
    ) -> Message:
        """ Display information and a GitHub link to the source code of a command """

        if not source_item:
            embed = Embed(title="Dispy's GitHub repository", color=SUCCESS_COLOR)
            embed.add_field(name="Repository", value=f"[Go to GitHub](https://github.com/Pandabweer/dispy-discord-bot)")
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/54767698?v=4")
            return await inter.response.send_message(embed=embed, ephemeral=private)

        return await inter.response.send_message("In progress", ephemeral=private)


def setup(bot: Dispy) -> None:
    """ Load the PyPi cog """
    bot.add_cog(BotSource(bot))
