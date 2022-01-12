import random
import unicodedata
import re

from typing import Tuple

from disnake import ApplicationCommandInteraction, Message, Embed, Member
from disnake.ext import commands
from disnake.utils import escape_markdown
from disnake.ext.commands import AutoShardedBot, Cog, slash_command

from utils import time_now_format
from core import (
    Dispy,
    logger,
    NEGATIVE_REPLIES,
    ERROR_COLOR,
    SUCCESS_COLOR
    )


class GeneralInfo(Cog, name='general-info'):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot
        
    def get_info(self, char: str) -> Tuple[str, str]:
        digit = f"{ord(char):x}"
        if len(digit) <= 4:
            u_code = f"\\u{digit:>04}"
        else:
            u_code = f"\\U{digit:>08}"

        url = f"https://www.compart.com/en/unicode/U+{digit:>04}"
        name = f"[{unicodedata.name(char, '')}]({url})"
        info = f"`{u_code.ljust(10)}`: {name} - {escape_markdown(char)}"
        return info, u_code

    @slash_command(name="charinfo")
    async def character_info(
        self, inter: ApplicationCommandInteraction,
        characters: str,
        hidden: bool = True
        ) -> Message:
        """ Shows you information on up to 50 unicode characters """

        embed = Embed(colour=ERROR_COLOR)

        if re.match(r"<(a?):(\w+):(\d+)>", characters):
            embed.description = "A custom emoji was found. Please remove it and try again."
        elif len(characters) > 50:
            embed.description = f"Too many characters ({len(characters)}/50)"
        else:
            char_list, raw_list = zip(*(self.get_info(c) for c in characters))

            embed.set_author(name="Character info:")
            embed.description = '\n'.join(char_list)
            embed.colour = SUCCESS_COLOR

        return await inter.send(embed=embed, ephemeral=hidden)


def setup(bot: Dispy) -> None:
    """ Load the GeneralInfo cog """
    bot.add_cog(GeneralInfo(bot))
