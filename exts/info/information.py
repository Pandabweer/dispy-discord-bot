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
    MEDIUM_COLOR,
    SUCCESS_COLOR
    )


class GeneralInfo(Cog, name='general-info'):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    @staticmethod
    def get_char_info(char: str) -> Tuple[str, str]:
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
            char_list, raw_list = zip(*(self.get_char_info(c) for c in characters))

            embed.set_author(name="Character info:")
            embed.description = '\n'.join(char_list)
            embed.colour = SUCCESS_COLOR

        return await inter.send(embed=embed, ephemeral=hidden)

    @slash_command(name="ping")
    async def server_response_delay(
        self, inter: ApplicationCommandInteraction,
        hidden: bool = True
        ) -> Message:
        """ Gets different measures of latency within the bot """

        panda_happy = "https://emoji.discord.st/emojis/44f1c6c0-eb10-420b-b6c8-73d02da0bcbe.png"
        panda_displeased = "https://emoji.discord.st/emojis/PandaEr.png"
        panda_crying = "https://emoji.discord.st/emojis/5d693019-3c03-43a6-b1f6-1351fd52841d.png"

        discord_ping = round(self.bot.latency * 1000)
        database_ping = 100 # To be implemented

        overall_ping = round((discord_ping + database_ping) / 2)

        embed = Embed()

        if overall_ping < 200:
            icon = panda_happy
            embed.colour = SUCCESS_COLOR
        elif 200 < overall_ping < 400:
            icon = panda_displeased
            embed.colour = MEDIUM_COLOR
        else:
            icon = panda_crying
            embed.colour = ERROR_COLOR

        embed.set_author(name=f"Overall ping: {overall_ping} ms", icon_url=icon)

        embed.add_field(name="Discord", value=f"{discord_ping} ms", inline=False)
        embed.add_field(name="Database", value=f"{database_ping} ms", inline=False)

        return await inter.send(embed=embed, ephemeral=hidden)


def setup(bot: Dispy) -> None:
    """ Load the GeneralInfo cog """
    bot.add_cog(GeneralInfo(bot))
